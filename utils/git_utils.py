from __future__ import annotations
import subprocess
from typing import Tuple


def git_apply_check(patch_path: str, cwd: str) -> Tuple[bool, str]:
    """Run `git apply --check` on `patch_path` in directory `cwd`.

    Returns (ok, output).
    """
    try:
        proc = subprocess.run(["git", "apply", "--check", patch_path], cwd=cwd, capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        return (proc.returncode == 0, out)
    except Exception as e:
        return (False, str(e))
