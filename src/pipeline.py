import os
import pandas as pd
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from src.models import PipelineResult
from src.agents import cleaner, validator, transformer, anomaly, summariser
from src.connectors import mongodb

console = Console()

def load_csv(file_path: str) -> tuple[pd.DataFrame, str, int]:
    df = pd.read_csv(file_path)
    total_rows = len(df)
    preview = df.head(20).to_csv(index=False)
    return df, preview, total_rows

def load_mongodb(uri: str, database: str, collection: str, limit: int = 1000) -> tuple[pd.DataFrame, str, int]:
    df = mongodb.fetch_collection(uri, database, collection, limit)
    total_rows = len(df)
    preview = df.head(20).to_csv(index=False)
    return df, preview, total_rows

def run_pipeline(file_path: str) -> PipelineResult:
    file_name = os.path.basename(file_path)
    df, preview, total_rows = load_csv(file_path)
    return _run_pipeline_from_data(file_name, preview, total_rows)

def run_pipeline_mongo(uri: str, database: str, collection: str, limit: int = 1000) -> PipelineResult:
    df, preview, total_rows = load_mongodb(uri, database, collection, limit)
    return _run_pipeline_from_data(f"{database}.{collection}", preview, total_rows)

def _run_pipeline_from_data(source_label: str, preview: str, total_rows: int) -> PipelineResult:
    console.print(Panel.fit(
        f"[bold green]MULTI-AGENT DATA PIPELINE[/bold green]\n[dim]Processing: {source_label}[/dim]",
        border_style="green"
    ))
    console.print(f"\n[cyan]→ Loaded {total_rows} rows from {source_label}[/cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        task1 = progress.add_task("[green]Agent 1/5 — Cleaner...", total=None)
        cleaner_result = cleaner.run(preview, total_rows)
        progress.update(task1, description="[green]Agent 1/5 — Cleaner ✓")
        progress.stop_task(task1)

        task2 = progress.add_task("[blue]Agent 2/5 — Validator...", total=None)
        validator_result = validator.run(preview, total_rows)
        progress.update(task2, description="[blue]Agent 2/5 — Validator ✓")
        progress.stop_task(task2)

        task3 = progress.add_task("[yellow]Agent 3/5 — Transformer...", total=None)
        transformer_result = transformer.run(preview, total_rows)
        progress.update(task3, description="[yellow]Agent 3/5 — Transformer ✓")
        progress.stop_task(task3)

        task4 = progress.add_task("[red]Agent 4/5 — Anomaly Detector...", total=None)
        anomaly_result = anomaly.run(preview, total_rows)
        progress.update(task4, description="[red]Agent 4/5 — Anomaly Detector ✓")
        progress.stop_task(task4)

        context = f"""
        Cleaner found {len(cleaner_result.issues_fixed)} issues affecting {cleaner_result.rows_affected} rows.
        Validator score: {validator_result.completeness_score}% completeness, {len(validator_result.violations)} violations.
        Transformer applied {len(transformer_result.transformations_applied)} transformations.
        Anomaly detector found {anomaly_result.anomaly_count} anomalies with risk score {anomaly_result.anomaly_score}/10.
        """

        task5 = progress.add_task("[magenta]Agent 5/5 — Summariser...", total=None)
        summariser_result = summariser.run(preview, total_rows, context)
        progress.update(task5, description="[magenta]Agent 5/5 — Summariser ✓")
        progress.stop_task(task5)

    result = PipelineResult(
        file_name=source_label,
        total_rows=total_rows,
        cleaner=cleaner_result,
        validator=validator_result,
        transformer=transformer_result,
        anomaly=anomaly_result,
        summariser=summariser_result,
        status="complete"
    )

    _print_summary(result)
    return result

def _print_summary(result: PipelineResult):
    console.print("\n")
    table = Table(title="Pipeline Results", border_style="green")
    table.add_column("Agent", style="cyan")
    table.add_column("Result", style="white")

    table.add_row("Cleaner", f"{result.cleaner.rows_affected} rows fixed, {len(result.cleaner.issues_fixed)} issues")
    table.add_row("Validator", f"{result.validator.completeness_score}% complete, {len(result.validator.violations)} violations")
    table.add_row("Transformer", f"{result.transformer.rows_transformed} rows transformed, {len(result.transformer.new_columns)} new columns")
    table.add_row("Anomaly", f"{result.anomaly.anomaly_count} anomalies, risk score {result.anomaly.anomaly_score}/10")
    table.add_row("Summariser", f"{len(result.summariser.recommendations)} recommendations")

    console.print(table)
    console.print(f"\n[bold green]✓ Pipeline complete — {result.total_rows} rows processed[/bold green]\n")
