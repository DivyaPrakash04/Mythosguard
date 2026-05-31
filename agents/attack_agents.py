from __future__ import annotations
from .base import Agent
import os
from typing import Dict, Optional

class SourceCodeAttackAgent(Agent):
    """Detects and points to likely vulnerable files/lines in repository."""
    def __init__(self, repo_root: str, provider: str = "mock", mock_llm: Optional[object] = None):
        self.repo_root = repo_root
        self.provider = provider
        self.mock_llm = mock_llm

    async def act(self, state: Dict) -> Dict:
        # For demo, scan sample_vulnerable_code/vuln.py for patterns
        target_file = os.path.join(self.repo_root, "sample_vulnerable_code", "vuln.py")
        
        # If using mock provider, generate attack prompt using MockLLM
        attack_prompt = None
        if self.provider == "mock" and self.mock_llm:
            prompt = f"Generate an attack to test vulnerabilities in {target_file}"
            response = await self.mock_llm.call_model(prompt, provider="mock")
            attack_prompt = response["text"]
        
        return {
            "target_file": target_file, 
            "note": "scan for insecure patterns",
            "attack_prompt": attack_prompt,
            "provider": self.provider
        }
