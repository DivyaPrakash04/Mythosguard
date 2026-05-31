from __future__ import annotations
from target_adapters.static_code_adapter import StaticCodeAdapter
import shutil
import tempfile
import os
from typing import List
import subprocess


def apply_unified_diff(orig_lines: List[str], diff_text: str) -> List[str]:
    """Apply a simple unified diff (as produced by difflib.unified_diff) to orig_lines.

    This implementation supports basic hunks with context lines (' '), removals ('-'),
    and additions ('+'). It is intentionally small and suitable for single-file, single-hunk diffs produced by Defender.
    """
    if not diff_text:
        return orig_lines

    lines = diff_text.splitlines()
    hunks = []
    cur_hunk = None
    for ln in lines:
        if ln.startswith('@@'):
            if cur_hunk is not None:
                hunks.append(cur_hunk)
            parts = ln.split()
            old_range = parts[1].lstrip('-')
            if ',' in old_range:
                old_start, old_count = old_range.split(',')
            else:
                old_start, old_count = old_range, '1'
            cur_hunk = {"old_start": int(old_start), "old_count": int(old_count), "lines": []}
        elif cur_hunk is not None:
            cur_hunk["lines"].append(ln)
    if cur_hunk is not None:
        hunks.append(cur_hunk)

    result = []
    orig_idx = 0
    for h in hunks:
        start = h["old_start"] - 1
        result.extend(orig_lines[orig_idx:start])
        j = start
        for hl in h["lines"]:
            if not hl:
                continue
            code = hl[1:]
            if hl.startswith(' '):
                if j < len(orig_lines):
                    result.append(orig_lines[j])
                else:
                    result.append(code + "\n")
                j += 1
            elif hl.startswith('-'):
                j += 1
            elif hl.startswith('+'):
                result.append(code + "\n")
            else:
                if j < len(orig_lines):
                    result.append(orig_lines[j])
                    j += 1
        orig_idx = j
    result.extend(orig_lines[orig_idx:])
    return result


class Verifier:
    async def verify(self, orig_path: str, patch: dict, verify_only: bool = False) -> dict:
        """Verify a patch.

        If `verify_only` is True, run `git apply --check` and simulate applying the diff in memory
        (use `apply_unified_diff`) to determine post-findings, but do not alter any files.
        Otherwise, attempt to `git apply` in a temp dir; fall back to applying the diff in-memory.
        """
        tmpdir = tempfile.mkdtemp()
        dst = os.path.join(tmpdir, os.path.basename(orig_path))
        shutil.copy2(orig_path, dst)

        # Read original
        with open(dst, "r", encoding="utf-8") as f:
            orig_lines = f.readlines()

        diff_text = patch.get("diff")
        applied_via_git = False
        git_check_ok = False
        new_lines = orig_lines.copy()

        if diff_text:
            patch_file = os.path.join(tmpdir, "fix.patch")
            with open(patch_file, "w", encoding="utf-8") as pf:
                pf.write(diff_text)

            # try git apply --check
            try:
                res = subprocess.run(["git", "apply", "--check", patch_file], cwd=tmpdir, capture_output=True)
                git_check_ok = (res.returncode == 0)
            except Exception:
                git_check_ok = False

            if verify_only:
                # simulate applying the diff in-memory for verification results
                new_lines = apply_unified_diff(orig_lines, diff_text)
            else:
                if git_check_ok:
                    try:
                        subprocess.run(["git", "apply", patch_file], cwd=tmpdir, check=True, capture_output=True)
                        applied_via_git = True
                        # read patched file
                        with open(dst, "r", encoding="utf-8") as f:
                            new_lines = f.readlines()
                    except Exception:
                        applied_via_git = False
                        new_lines = apply_unified_diff(orig_lines, diff_text)
                else:
                    new_lines = apply_unified_diff(orig_lines, diff_text)
        else:
            # fallback to single-line replacement
            line_idx = patch.get("line") - 1 if patch.get("line") else None
            if line_idx is not None and 0 <= line_idx < len(new_lines):
                new_lines[line_idx] = patch.get("new_code") + "\n"

        # For verification, analyze the simulated/new content at `dst` path
        if applied_via_git:
            analyze_path = dst
        else:
            # write new_lines to dst for analysis (temporary, does not affect repo)
            with open(dst, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            analyze_path = dst

        adapter = StaticCodeAdapter()
        findings = adapter.analyze(analyze_path)
        passed = all(f["type"] != patch.get("matcher") for f in findings)

        # cleanup
        shutil.rmtree(tmpdir)
        return {"passed": passed, "post_findings": findings, "git_check_ok": git_check_ok, "applied_via_git": applied_via_git}
