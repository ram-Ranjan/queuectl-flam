import typer, json
from rich import print
from queuectl.database import init_db, connect
from queuectl.job_manager import enqueue, list_jobs
from queuectl.worker_manager import start_workers
from queuectl.config import load_config, save_config
from queuectl.dlq_manager import list_dlq, retry_dlq

app = typer.Typer(help="QueueCTL - Background Job Queue CLI")

@app.command()
def init():
    try:
        init_db()
        print("[green]Database initialized successfully![/green]")
    except Exception as e:
        print(f"[red]Failed to initialize database: {e}[/red]")
        raise typer.Exit(code=1)
@app.command()
def enqueue_job(job_json: str):
    job = json.loads(job_json)
    enqueue(job)
    print(f"[cyan]Enqueued job:[/cyan] {job['id']}")

@app.command()
def worker_start(count: int = 1):
    print(f"[green]Starting {count} worker(s)...[/green]")
    start_workers(count)

@app.command()
def list_jobs_cmd(state: str = None):
    jobs = list_jobs(state)
    for j in jobs:
        print(j)
@app.command()
def dlq_list():
    rows = list_dlq()
    if not rows:
        print("[green]DLQ is empty.[/green]")
        return
    for r in rows:
        print(r)

@app.command()
def dlq_retry(job_id: str):
    retry_dlq(job_id)

@app.command()
def config(key: str = None, value: str = None):
    cfg = load_config()
    if key and value:
        cfg[key] = int(value) if value.isdigit() else value
        save_config(cfg)
        print(f"Updated {key} = {cfg[key]}")
    else:
        print(cfg)

@app.command()
def status():
    conn = connect()
    cur = conn.cursor()
    states = ["pending", "processing", "completed"]
    print("\nQueue Status")
    for s in states:
        cur.execute("SELECT COUNT(*) FROM jobs WHERE state=?", (s,))
        print(f"{s}: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM dlq")
    print(f"dead: {cur.fetchone()[0]}")
    conn.close()

if __name__ == "__main__":
    app()
