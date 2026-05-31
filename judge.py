from __future__ import annotations
from typing import List, Dict

class Verdict(Dict):
    pass

class Judge:
    async def evaluate(self, findings: List[Dict]) -> Verdict:
        success = len(findings) > 0
        vuln_types = list({f["type"] for f in findings})
        return {"success": success, "types": vuln_types, "count": len(findings)}
