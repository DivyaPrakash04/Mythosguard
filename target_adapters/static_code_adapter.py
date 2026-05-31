from __future__ import annotations
from typing import List, Dict
import re

class Finding(dict):
    pass

class StaticCodeAdapter:
    """Very small static analyzer that finds insecure patterns in a file."""
    PATTERNS = {
        "eval": re.compile(r"\beval\s*\(") ,
        "exec": re.compile(r"\bexec\s*\(") ,
        "hardcoded_password": re.compile(r"password\s*=\s*[\'\"]\w+[\'\"]"),
    }

    def analyze(self, file_path: str) -> List[Finding]:
        findings = []
        with open(file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                for key, rx in self.PATTERNS.items():
                    if rx.search(line):
                        findings.append({
                            "type": key,
                            "line": i,
                            "line_text": line.strip(),
                            "file_path": file_path,
                        })
        return findings
