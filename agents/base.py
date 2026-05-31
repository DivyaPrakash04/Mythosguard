from __future__ import annotations
from typing import Any

class Agent:
    """Minimal agent base class."""
    async def act(self, state: dict) -> Any:
        raise NotImplementedError()
