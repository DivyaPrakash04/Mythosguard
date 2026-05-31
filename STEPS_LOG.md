# Mythosguard — Steps Log

This file records actions performed during development for reproducibility and judging context.

2026-05-31 00:00 UTC — Created repository notes and plan
- Created `PLAN_AND_ARCHITECTURE.md` with MVP, schemas, and next-file list.

2026-05-31 00:05 UTC — Created scaffolding files
- Created `STEPS_LOG.md` (this file) and `README.md` (initial stub).

Next actions (in order)
- Scaffold Python files and `requirements.txt`.
- Implement `MockLLM` and orchestrator core loop.
- Implement attack/judge/defender/verifier agents.
- Add demo runner and sample logs (JSONL).

-- End Log

2026-05-31 00:10 UTC — Add monitoring & logging instructions
- Always append each development action or file edit as a new timestamped line in this file.
- Token monitoring: assume a default context budget of 8192 tokens unless you specify otherwise. I will estimate token usage by counting characters in messages/code and converting using a rough ratio (4 chars ≈ 1 token). I will warn you when estimated usage reaches 85% of the budget. If you have a different budget, tell me and I'll use that.

-- End Update

2026-05-31 00:20 UTC — Clarified target scope for agents
- Default prototype target: the contained `target_model` (LLM behavior/jailbreak testing) using `MockLLM` for reproducible demos.
- Extension options documented: web apps (HTTP endpoints), online APIs, local source code (static analysis), binaries/services (sandboxed fuzzing), and CI artifacts. Each requires a `TargetAdapter` that exposes `async def call(target_input)` and enforces sandboxing and consent.
- Tools / libraries to integrate when extending:
	- Web app testing: `httpx`, Selenium / Playwright (end-to-end), OWASP ZAP (scanning, optional)
	- Static code analysis: `semgrep`, `bandit`, `pylint` (for Python), custom AST checks
	- Binary/fuzz testing: AFL / honggfuzz (advanced, not required for hackathon)
	- CI/Repo analysis: GitHub API + shallow clone + `semgrep` rules
	- Infrastructure/API: use rate-limited `httpx` and strict timeouts

- Safety & legality: only run attacks against controlled/test targets. Do NOT run automated attacks against third-party systems without explicit permission. Record scope in `STEPS_LOG.md` for audits.

-- End Update
2026-05-31 00:35 UTC — Scaffolded source-code demo files
 - Added `requirements.txt`, `agents/` base and attack agent, `target_adapters/static_code_adapter.py`, `judge.py`, `defender.py`, `verifier.py`, `planner.py`, `orchestrator.py`, `demo.py`, and `sample_vulnerable_code/vuln.py`.
 - Demo: run `python demo.py` to execute 3 rounds against the sample vulnerable file. Logs are persisted to `logs/rounds.jsonl`.

2026-05-31 00:40 UTC — Note: D: drive preference
- User requested the project and artifacts remain on D: drive due to limited C: space. All files created use relative paths so artifacts (e.g., `logs/rounds.jsonl`, temp dirs) will be placed under the project root on D:. Added `.env.example` with optional `BASE_DIR` to override if needed.

2026-05-31 00:50 UTC — Improved Defender to emit unified diffs
- Updated `target_adapters/static_code_adapter.py` to include `file_path` in findings and replaced `defender.generate_patch` to build a unified diff using `difflib.unified_diff`. Patch objects now include a `diff` field containing the unified diff text.

2026-05-31 00:55 UTC — Verifier now applies unified diffs
- Replaced naive line-replace in `verifier.verify()` with an `apply_unified_diff()` helper that parses and applies unified diffs produced by Defender. Verifier now writes the patched file and re-runs the static analyzer to confirm vulnerability removal.

2026-05-31 01:05 UTC — Added unit tests
- Added `tests/test_diff_apply.py` to validate `apply_unified_diff()` behavior.
- Added `tests/test_end_to_end_patch_verify.py` to run a single orchestrator round on a temp copy of `sample_vulnerable_code/vuln.py` and assert patch + verify flow.
- Attempted to run `pip install -r requirements.txt` here but the environment prevented running terminal pip commands. To run tests locally, see instructions below.

2026-05-31 01:15 UTC — Added Defender diff unit tests
- Added `tests/test_defender_diff.py` with cases for `eval` replacement, missing `file_path` fallback, and hardcoded password patching. These tests exercise `Defender.generate_patch()` diff formatting and edge handling.

2026-05-31 01:25 UTC — Add git-apply integration
- Added `Defender.write_patch_file(patch, out_path)` to persist diffs as patch files.
- Updated `verifier.verify()` to attempt `git apply --check` and `git apply` in the temp directory; it falls back to the internal `apply_unified_diff()` if `git` is not available or the check fails. Verification result now includes `git_check_ok` and `applied_via_git` flags.

2026-05-31 01:40 UTC — Added git helper and tests
- Added `utils/git_utils.py` with `git_apply_check()` to run `git apply --check` and return result/output.
- Added `tests/test_git_utils.py` which generates a patch via `Defender` and verifies `git_apply_check()` runs without error on a temp directory.

2026-05-31 20:00 UTC — Implemented Deterministic MockLLM adapter
- Created `providers/mock.py` with `MockLLM` class for reproducible demos without external API dependencies
- MockLLM uses prompt hashing for deterministic responses based on prompt content and seed
- Supports multiple response categories (roleplay, injection, emotional, default) with predefined templates
- Updated `orchestrator.py` to accept `provider` and `provider_seed` parameters
- Updated `agents/attack_agents.py` to use MockLLM for generating attack prompts
- Updated `demo.py` with `--provider` (currently only "mock") and `--provider-seed` flags
- Attack prompts are now logged in `logs/rounds.jsonl` for audit trail
- Verified deterministic behavior: same prompts produce consistent responses






