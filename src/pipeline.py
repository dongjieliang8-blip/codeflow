"""Pipeline orchestrator — wires 4 agents together with structured data passing."""

import json
import time
from dataclasses import dataclass, field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.llm.client import LLMClient, LLMConfig
from src.agents import scanner, architect, executor, reviewer
from src.utils import collect_source_files, format_files_for_prompt

console = Console()


@dataclass
class PipelineResult:
    scanner_report: dict = field(default_factory=dict)
    architect_plan: dict = field(default_factory=dict)
    executor_output: dict = field(default_factory=dict)
    reviewer_report: dict = field(default_factory=dict)
    token_usage: dict = field(default_factory=dict)
    elapsed_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    @property
    def verdict(self) -> str:
        return self.reviewer_report.get("overall_verdict", "unknown")


class Pipeline:
    """CodeFlow pipeline: Scanner → Architect → Executor → Reviewer."""

    def __init__(self, config: LLMConfig | None = None):
        self.client = LLMClient(config)
        self.result = PipelineResult()

    def run(self, target_dir: str, dry_run: bool = False) -> PipelineResult:
        """Execute the full 4-agent pipeline on a target directory."""
        t0 = time.time()

        # Stage 1: Scan
        console.print(Panel.fit("[bold blue]STAGE 1/4: Scanner Agent[/] — auditing codebase", border_style="blue"))
        files = collect_source_files(target_dir)
        if not files:
            self.result.errors.append("No source files found in target directory")
            return self.result
        source_text = format_files_for_prompt(files)
        self.result.scanner_report = scanner.run(source_text, self.client)
        self._print_scanner_summary()

        if dry_run:
            self.result.elapsed_seconds = time.time() - t0
            return self.result

        # Stage 2: Architect
        console.print(Panel.fit("[bold yellow]STAGE 2/4: Architect Agent[/] — designing refactoring plan", border_style="yellow"))
        self.result.architect_plan = architect.run(self.result.scanner_report, self.client)
        self._print_architect_summary()

        # Stage 3: Executor
        console.print(Panel.fit("[bold green]STAGE 3/4: Executor Agent[/] — generating code changes", border_style="green"))
        self.result.executor_output = executor.run(
            self.result.architect_plan,
            source_text,
            self.client,
        )
        self._print_executor_summary()

        # Stage 4: Reviewer
        console.print(Panel.fit("[bold red]STAGE 4/4: Reviewer Agent[/] — validating changes", border_style="red"))
        self.result.reviewer_report = reviewer.run(
            self.result.executor_output,
            self.result.scanner_report,
            self.client,
        )
        self._print_reviewer_summary()

        self.result.elapsed_seconds = time.time() - t0
        self._print_final_summary()
        return self.result

    def _print_scanner_summary(self):
        r = self.result.scanner_report
        m = r.get("metrics", {})
        table = Table(title="Scanner Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        for key in ["total_files", "total_lines", "critical_issues", "high_issues", "medium_issues", "low_issues"]:
            table.add_row(key.replace("_", " ").title(), str(m.get(key, "?")))
        console.print(table)
        if r.get("summary"):
            console.print(f"[dim]{r['summary']}[/dim]")

    def _print_architect_summary(self):
        p = self.result.architect_plan
        batches = p.get("batches", [])
        console.print(f"[yellow]Strategy:[/] {p.get('strategy', 'N/A')}")
        console.print(f"[yellow]Batches planned:[/] {len(batches)}")
        for b in batches:
            console.print(f"  • [bold]{b.get('priority', '?')}[/] {b.get('title', 'Untitled')}")

    def _print_executor_summary(self):
        e = self.result.executor_output
        batches = e.get("batches_executed", [])
        total_changes = sum(len(b.get("changes", [])) for b in batches)
        console.print(f"[green]Batches executed:[/] {len(batches)}")
        console.print(f"[green]Total file changes:[/] {total_changes}")

    def _print_reviewer_summary(self):
        r = self.result.reviewer_report
        console.print(f"[red]Verdict:[/] [bold]{r.get('overall_verdict', 'unknown').upper()}[/]")
        if r.get("final_recommendation"):
            console.print(f"[dim]{r['final_recommendation']}[/dim]")

    def _print_final_summary(self):
        console.print()
        console.print(Panel.fit(
            f"[bold]Pipeline Complete[/]\n"
            f"Time: {self.result.elapsed_seconds:.1f}s\n"
            f"Verdict: {self.verdict.upper()}\n"
            f"Errors: {len(self.result.errors)}",
            border_style="green" if self.result.success else "red"
        ))

    def save_report(self, path: str):
        """Save the full pipeline result as JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "scanner_report": self.result.scanner_report,
                "architect_plan": self.result.architect_plan,
                "executor_output": self.result.executor_output,
                "reviewer_report": self.result.reviewer_report,
                "elapsed_seconds": self.result.elapsed_seconds,
                "errors": self.result.errors,
            }, f, ensure_ascii=False, indent=2)
        console.print(f"[green]Report saved to {path}[/]")
