import asyncio
import io
import re
import contextlib
from pathlib import Path

from orchestrator import Orchestrator


def make_orchestrator():
    repo_root = Path(__file__).resolve().parents[1]
    return Orchestrator(str(repo_root))


def test_renderers_produce_same_semantics():
    orch = make_orchestrator()
    log = asyncio.get_event_loop().run_until_complete(orch.run_round(1, dry_run=True))

    # Import dashboard and capture Rich output
    import ui.console_dashboard as cd
    from rich.console import Console

    old_console = cd.console
    cd.console = Console(record=True, force_terminal=True)
    with cd.console.capture() as cap:
        cd.render_round_summary(log)
    rich_out = cap.get()
    cd.console = old_console

    # Capture plain output
    plain_buf = io.StringIO()
    with contextlib.redirect_stdout(plain_buf):
        cd.render_plain(log)
    plain_out = plain_buf.getvalue()

    # Basic checks: strategy appears in both
    assert str(log.get("strategy")) in rich_out
    assert str(log.get("strategy")) in plain_out

    # Check findings mentions: vulnerable filename appears in both outputs
    fname = "vuln.py"
    assert fname in rich_out
    assert fname in plain_out

    # Extract verification booleans from both outputs
    def extract_bool(text, key):
        # Allow for ANSI escapes and spacing between key and boolean
        m = re.search(rf"{key}[\s\S]{{0,100}}?(True|False)", text, re.IGNORECASE)
        if m:
            return m.group(1) == "True"
        return None

    rich_passed = extract_bool(rich_out, "passed")
    plain_passed = extract_bool(plain_out, "passed")
    assert rich_passed == plain_passed

    rich_git = extract_bool(rich_out, "git_check_ok")
    plain_git = extract_bool(plain_out, "git_check_ok")
    assert rich_git == plain_git
