import typer
from rich import print
from database import init_db


app = typer.Typer(help="QueueCTL - Background Job Queue CLI")

@app.command()
def version():
    print("QueueCTL v0.1")
    
@app.command()
def init():
    """Initialize the database."""
    init_db()


if __name__ == "__main__":
    app()
    