import subprocess, time, datetime
from queuectl.database import connect
from queuectl.config import load_config
from queuectl.logger import get_logger

def run_job(job):
    cfg = load_config()
    con = connect()
    cursr = con.cursor()
    job_id, command, state, attempts, max_retries, created_at, updated_at = job
    logger = get_logger(job_id)

    try:
        cursr.execute("UPDATE jobs SET state='processing', updated_at=? WHERE id=?",
                    (datetime.datetime.utcnow().isoformat(), job_id))
        con.commit()
        logger.info(f"Started job: {command}")

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:
            cursr.execute("UPDATE jobs SET state='completed', updated_at=? WHERE id=?",
                        (datetime.datetime.utcnow().isoformat(), job_id))
            logger.info(f"✅ Completed successfully. Output: {output}")
            print(f"✅ {job_id} -> Completed")
        else:
            raise Exception(f"Exit code {result.returncode}, Error: {error}")

    except Exception as e:
        attempts += 1
        logger.error(f"Job failed: {e}")
        if attempts < max_retries:
            delay = cfg["backoff_base"] ** attempts
            logger.warning(f"Retrying in {delay}s... [Attempt {attempts}/{max_retries}]")
            print(f"⚠️ {job_id} failed. Retrying in {delay}s...")
            time.sleep(delay)
            cursr.execute("UPDATE jobs SET attempts=?, state='pending', updated_at=? WHERE id=?",
                        (attempts, datetime.datetime.utcnow().isoformat(), job_id))
        else:
            logger.critical(f"Job permanently failed — moved to DLQ.")
            print(f"❌ {job_id} moved to DLQ.")
            cursr.execute("DELETE FROM jobs WHERE id=?", (job_id,))
            cursr.execute("INSERT INTO dlq VALUES (?,?,?,?)",
                        (job_id, command, str(e), datetime.datetime.utcnow().isoformat()))
        con.commit()
    finally:
        con.close()
        logger.info("Job execution finished.")
