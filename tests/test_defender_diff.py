import asyncio
from defender import Defender
import tempfile
from pathlib import Path


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_defender_generates_unified_diff_for_eval(tmp_path):
    p = tmp_path / "vuln.py"
    content = "def compute(user_input):\n    return eval(user_input)\n"
    p.write_text(content, encoding="utf-8")

    finding = {"type": "eval", "line": 2, "line_text": "    return eval(user_input)", "file_path": str(p)}
    patch = run(Defender().generate_patch(finding))

    assert "diff" in patch and patch["diff"].strip() != ""
    diff = patch["diff"]
    assert "--- a/" in diff and "+++ b/" in diff
    assert "-    return eval(user_input)" in diff
    assert ("+    return ast.literal_eval(user_input)" in diff) or ("ast.literal_eval" in diff)


def test_defender_handles_missing_file_path():
    finding = {"type": "exec", "line": 1, "line_text": "exec(code)", "file_path": None}
    patch = asyncio.get_event_loop().run_until_complete(Defender().generate_patch(finding))
    assert "diff" in patch
    # fallback should include 'original' or 'patched' markers
    assert ("original" in patch["diff"]) or ("patched" in patch["diff"])


def test_defender_removes_hardcoded_password(tmp_path):
    p = tmp_path / "vuln.py"
    content = "password = \"hunter2\"\n"
    p.write_text(content, encoding="utf-8")

    finding = {"type": "hardcoded_password", "line": 1, "line_text": "password = \"hunter2\"", "file_path": str(p)}
    patch = run(Defender().generate_patch(finding))
    assert patch["action"] == "remove_hardcoded_password"
    assert "password = None" in patch["diff"]
    assert "--- a/" in patch["diff"] and "+++ b/" in patch["diff"]
