import datetime
from queuectl.database import connect

def enqueue(job):
    con = connect()
    cursr = con.cursor()
    now = datetime.datetime.utcnow().isoformat()
    job["created_at"] = now
    job["updated_at"] = now
    job.setdefault("state", "pending")
    job.setdefault("attempts", 0)
    job.setdefault("max_retries", 3)
    cursr.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?)",
                (job["id"], job["command"], job["state"], job["attempts"],
                 job["max_retries"], job["created_at"], job["updated_at"]))
    con.commit()
    con.close()

def list_jobs(state=None):
    conn = connect()
    cur = conn.cursor()
    if state:
        cur.execute("SELECT * FROM jobs WHERE state=?", (state,))
    else:
        cur.execute("SELECT * FROM jobs")
    rows = cur.fetchall()
    conn.close()
    return rows
