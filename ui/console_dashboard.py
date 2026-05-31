from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.columns import Columns


console = Console()


def render_round_summary(log: dict) -> None:
    """Render a concise console dashboard for a single orchestrator round.

    Shows strategy, findings, unified diff (if any) and verification results.
    """
    strategy = log.get("strategy", "(unknown)")
    findings = log.get("findings", []) or []
    patch = log.get("patch")
    verification = log.get("verification", {})

    # Strategy panel
    strategy_panel = Panel(f"[bold cyan]{strategy}[/bold cyan]", title="Strategy")

    # Findings table
    f_table = Table(title="Findings", show_lines=False)
    f_table.add_column("File", style="magenta")
    f_table.add_column("Line", style="green")
    f_table.add_column("Type", style="red")
    f_table.add_column("Snippet", overflow="fold")
    if findings:
        for f in findings:
            f_table.add_row(str(f.get("file_path") or f.get("file") or "-"),
                            str(f.get("line") or "-"),
                            str(f.get("type") or "-"),
                            str(f.get("line_text") or f.get("snippet") or "-"))
    else:
        f_table.add_row("-", "-", "-", "No findings")

    # Patch diff panel
    if patch and patch.get("diff"):
        diff_text = patch.get("diff")
        syntax = Syntax(diff_text, "diff", theme="monokai", word_wrap=False)
        patch_panel = Panel(syntax, title="Patch (unified diff)")
    else:
        patch_panel = Panel("No patch generated", title="Patch")

    # Verification table
    v_table = Table(title="Verification")
    v_table.add_column("Key", style="yellow")
    v_table.add_column("Value", style="white")
    if verification:
        for k in ("passed", "git_check_ok", "applied_via_git"):
            if k in verification:
                v_table.add_row(k, str(verification.get(k)))
        # include any other keys
        for k, v in verification.items():
            if k in ("passed", "git_check_ok", "applied_via_git"):
                continue
            v_table.add_row(k, str(v))
    else:
        v_table.add_row("status", "not run")

    # Compose columns
    console.print(Columns([strategy_panel, v_table]))
    console.print(f_table)
    console.print(patch_panel)


def render_plain(log: dict) -> None:
    """Plain-text fallback renderer for non-TTY or CI environments."""
    strategy = log.get("strategy", "(unknown)")
    findings = log.get("findings", []) or []
    patch = log.get("patch")
    verification = log.get("verification", {})

    print(f"=== Strategy: {strategy} ===")
    print("Findings:")
    if findings:
        for f in findings:
            print(f" - {f.get('file_path') or f.get('file') or '-'}:{f.get('line') or '-'} {f.get('type') or '-'} -> {f.get('line_text') or f.get('snippet') or ''}")
    else:
        print(" - No findings")

    print("\nPatch:")
    if patch and patch.get('diff'):
        print(patch.get('diff'))
    else:
        print(" No patch generated")

    print("\nVerification:")
    if verification:
        for k, v in verification.items():
            print(f" - {k}: {v}")
    else:
        print(" - not run")
