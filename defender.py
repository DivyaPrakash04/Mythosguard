from __future__ import annotations
from typing import Dict
import uuid
import datetime
import difflib
import os


def _now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


class Patch(Dict):
    pass


class Defender:
    async def generate_patch(self, finding: Dict) -> Patch:
        """Generate a structured patch including a unified diff for the finding.

        The finding must include `file_path`, `line`, and `line_text`.
        """
        typ = finding.get("type")
        line_text = finding.get("line_text", "")
        file_path = finding.get("file_path")

        if typ == "eval":
            new_code = line_text.replace("eval", "ast.literal_eval")
            action = "replace_eval_with_literal_eval"
        elif typ == "exec":
            new_code = "# removed exec usage for safety"
            action = "comment_out_exec"
        elif typ == "hardcoded_password":
            # replace the assigned value with None and a comment
            new_code = "password = None  # removed hardcoded password"
            action = "remove_hardcoded_password"
        else:
            new_code = "# patched"
            action = "generic_patch"

        # build unified diff
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                orig_lines = f.readlines()
        except Exception:
            orig_lines = [line_text + "\n"]

        idx = finding.get("line") - 1 if finding.get("line") else None
        new_lines = orig_lines.copy()
        if idx is not None and 0 <= idx < len(new_lines):
            orig_line = orig_lines[idx]
            indentation = orig_line[:-len(orig_line.lstrip())]
            new_lines[idx] = indentation + new_code + "\n"
        else:
            # append as fallback
            new_lines.append(new_code + "\n")

        # prefer repo-relative paths for git-style diffs
        if file_path:
            try:
                rel = os.path.relpath(file_path)
            except Exception:
                rel = file_path
            fromfile = f"a/{rel}"
            tofile = f"b/{rel}"
        else:
            fromfile = "original"
            tofile = "patched"
        diff_lines = list(difflib.unified_diff(orig_lines, new_lines, fromfile=fromfile, tofile=tofile, lineterm=""))
        diff_text = "\n".join(diff_lines)

        return {
            "id": str(uuid.uuid4()),
            "matcher": typ,
            "action": action,
            "new_code": new_code,
            "created_by": "Defender",
            "timestamp": _now_iso(),
            "line": finding.get("line"),
            "file_path": file_path,
            "diff": diff_text,
        }

    def write_patch_file(self, patch: Patch, out_path: str) -> None:
        """Write the patch's diff text to `out_path`.

        This makes it easy to run `git apply` on the produced patch.
        """
        diff_text = patch.get("diff", "") or ""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(diff_text)
