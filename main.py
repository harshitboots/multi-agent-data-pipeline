import typer
import json
import os
from rich.console import Console
from rich.panel import Panel
from src.pipeline import run_pipeline, run_pipeline_mongo

app = typer.Typer()
console = Console()

@app.command()
def run(
    input: str = typer.Argument(..., help="Path to your CSV file"),
    output: str = typer.Option(None, "--output", "-o", help="Save results to JSON file")
):
    """
    Multi-Agent Data Pipeline — 5 AI agents that process your CSV autonomously.
    
    Example:
        python main.py demo/sample_data.csv
        python main.py demo/sample_data.csv --output results.json
    """
    
    if not os.path.exists(input):
        console.print(f"[red]Error: File not found — {input}[/red]")
        raise typer.Exit(1)

    if not input.endswith(".csv"):
        console.print(f"[red]Error: File must be a CSV — {input}[/red]")
        raise typer.Exit(1)

    result = run_pipeline(input)

    if output:
        with open(output, "w") as f:
            json.dump(result.model_dump(), f, indent=2)
        console.print(f"[green]→ Results saved to {output}[/green]")

@app.command("run-mongo")
def run_mongo(
    uri: str = typer.Option(..., "--uri", help="MongoDB connection URI (e.g. mongodb://localhost:27017)"),
    database: str = typer.Option(..., "--database", "-d", help="Database name"),
    collection: str = typer.Option(..., "--collection", "-c", help="Collection name"),
    limit: int = typer.Option(1000, "--limit", "-l", help="Max documents to fetch"),
    output: str = typer.Option(None, "--output", "-o", help="Save results to JSON file"),
):
    """
    Run the pipeline on a MongoDB collection.

    Example:
        python main.py run-mongo --uri mongodb://localhost:27017 --database mydb --collection orders
    """
    result = run_pipeline_mongo(uri, database, collection, limit)

    if output:
        import json
        with open(output, "w") as f:
            json.dump(result.model_dump(), f, indent=2)
        console.print(f"[green]→ Results saved to {output}[/green]")


if __name__ == "__main__":
    app()