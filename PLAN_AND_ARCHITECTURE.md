# Mythosguard — Plan & Architecture

Purpose
- Short: blueprint for a provider-agnostic multi-agent red/blue-team arena with self-healing guardrails.
- Use: canonical reference for implementation, demos, and any LLM provider swap.

Tech Stack (recommended for hackathon)
- Python 3.11
- asyncio for concurrency
- pydantic for typed schemas
- httpx for LLM/provider HTTP adapters
- rich for console dashboard
- python-dotenv for secrets
- pytest for quick tests

High-level Components
- Orchestrator: controls round loop, sequencing, persistence
- Strategy Planner: selects attack categories and updates weights
- Attack Agents: generate attack prompts (roleplay, injection, emotional)
- Target Model: wrapper around LLM + local mock with guardrails
- Judge Agent: evaluates target responses (success/fail, vuln type)
- Defender Agent: generates structured guardrail patches
- Verifier Agent: replays attacks against patched guardrails
- Dashboard / Logger: prints round logs and persists to JSONL

Architecture (text)

Planner -> Attack Agent -> Target Model -> Judge -> (if success) Defender -> Verifier -> Planner

Core Interfaces (minimal)
- Agent (base): `async def act(self, state) -> ActionResult`
- Judge: `async def evaluate(response) -> Verdict` (structured)
- Defender: `async def generate_patch(vuln, context) -> Patch` (structured)
- TargetModel Adapter: `async def call_model(prompt, provider, timeout)`

Guardrail / Patch Schema (pydantic)
```
Patch:
 - id: str
 - matcher: str  # regex or intent label
 - action: str   # e.g., "block", "rewrite", "deny" 
 - created_by: str
 - timestamp: iso
```

Round Log Schema (JSON)
```
{
  "round": int,
  "strategy": str,
  "prompt": str,
  "response": str,
  "verdict": {"success": bool, "type": str, "score": float},
  "patch": Patch | null,
  "verification": {"passed": bool, "notes": str},
  "weights": {category: float}
}
```

Provider Agnostic Notes
- Implement a single `call_model(prompt, *, provider="mock|openai|ollama|together", **kwargs)` adapter.
- `MockLLM` must be deterministic (seedable) for reproducible demos.
- Use timeouts and `asyncio.wait_for` to avoid blocking rounds.

Defaults & Termination
- `max_rounds = 10`
- `early_stop_if_no_vulns_for = 3`
- `initial_weights = {"roleplay":0.33, "injection":0.33, "emotional":0.34}`

Acceptance Criteria (4-hour MVP)
- End-to-end loop runs for `N` rounds with mock LLM
- At least one attack succeeds and produces a patch
- Verifier confirms the patch prevents the same attack
- Console dashboard prints round-by-round logs; JSONL persisted

Developer Workflow
- Start with `MockLLM` and a single attack category
- Add Judge + Defender + Verifier
- Swap to real LLM provider only after core flow works

Files to create next
- `agents/base.py`, `agents/attack_agents.py`, `planner.py`, `orchestrator.py`, `target_model.py`, `dashboard.py`, `demo.py`, `requirements.txt`

-- End of Plan & Architecture
