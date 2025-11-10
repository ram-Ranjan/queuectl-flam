import datetime
from queuectl.database import connect

def list_dlq():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dlq")
    rows = cur.fetchall()
    conn.close()
    return rows

def retry_dlq(job_id):
    con = connect()
    cursr = con.cursor()
    cursr.execute("SELECT * FROM dlq WHERE id=?", (job_id,))
    job = cursr.fetchone()
    if not job:
        print(f"No job {job_id} in DLQ.")
        con.close()
        return

    new_id = f"{job[0]}_retry_{datetime.datetime.utcnow().isoformat()}"    
    cursr.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?)",
                (new_id, job[1], "pending", 0, 3,
                 datetime.datetime.utcnow().isoformat(), datetime.datetime.utcnow().isoformat()))
    cursr.execute("DELETE FROM dlq WHERE id=?", (job_id,))
    con.commit()
    con.close()
    print(f"Re-enqueued {job_id} as {new_id}")
