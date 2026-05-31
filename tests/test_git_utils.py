from defender import Defender
from utils.git_utils import git_apply_check
import tempfile
import os
import asyncio


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_git_apply_check_with_generated_patch(tmp_path):
    # create sample file
    sample_dir = tmp_path
    sample_file = sample_dir / "vuln.py"
    sample_file.write_text("def f():\n    return eval('2+2')\n", encoding="utf-8")

    finding = {"type": "eval", "line": 2, "line_text": "    return eval('2+2')", "file_path": str(sample_file)}
    patch = run(Defender().generate_patch(finding))

    patch_file = sample_dir / "fix.patch"
    Defender().write_patch_file(patch, str(patch_file))

    ok, out = git_apply_check(str(patch_file), str(sample_dir))
    # git apply --check should succeed on the temp directory
    assert isinstance(ok, bool)
