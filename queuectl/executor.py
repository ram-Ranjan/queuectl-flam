import subprocess, time, datetime
from queuectl.database import connect
from queuectl.config import load_config

def run_job(job):
    cfg = load_config()
    con = connect()
    cursr = con.cursor()
    job_id, command, state, attempts, max_retries, created_at, updated_at = job

    try:
        cursr.execute("UPDATE jobs SET state='processing', updated_at=? WHERE id=?",
                    (datetime.datetime.utcnow().isoformat(), job_id))
        con.commit()

        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=cfg.get("job_timeout", 300))        
        if result.returncode == 0:
            print(f"{job_id} -> Completed")
            cursr.execute("UPDATE jobs SET state='completed', updated_at=? WHERE id=?",
                        (datetime.datetime.utcnow().isoformat(), job_id))
        else:
            raise Exception(f"Exit code {result.returncode}")

    except Exception as e:
        attempts += 1
        if attempts <= max_retries:            
            delay = cfg["backoff_base"] ** attempts
            print(f"{job_id} failed. Retrying in {delay}s...")
            time.sleep(delay)
            cursr.execute("UPDATE jobs SET attempts=?, state='pending', updated_at=? WHERE id=?",
                        (attempts, datetime.datetime.utcnow().isoformat(), job_id))
        else:
            print(f"{job_id} moved to DLQ.")
            cursr.execute("DELETE FROM jobs WHERE id=?", (job_id,))
            cursr.execute("INSERT INTO dlq VALUES (?,?,?,?)",
                        (job_id, command, str(e), datetime.datetime.utcnow().isoformat()))
        con.commit()
    finally:
        con.close()
