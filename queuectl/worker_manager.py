import time, threading
from queuectl.database import connect
from queuectl.executor import run_job

stop_flag = False

def worker_loop(worker_id):
    while not stop_flag:
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM jobs WHERE state='pending' LIMIT 1")
            job = cur.fetchone()
            conn.close()

            if job:
                print(f"Worker-{worker_id} running job {job[0]}")
                run_job(job)
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Worker-{worker_id} error: {e}")
            time.sleep(1)  # Back off before retry
def start_workers(count=1):
    global stop_flag
    threads = []
    for i in range(count):
        t = threading.Thread(target=worker_loop, args=(i,))
        t.start()
        threads.append(t)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        print("Stopping workers...")
        for t in threads:
            t.join()
