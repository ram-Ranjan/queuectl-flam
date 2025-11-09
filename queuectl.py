import typer
from rich import print
from database import init_db


app = typer.Typer(help="QueueCTL - Background Job Queue CLI")


    
@app.command()
def init():
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise typer.Exit(code=1)
if __name__ == "__main__":
    app()
    