from __future__ import annotations
import asyncio
from agents.attack_agents import SourceCodeAttackAgent
from target_adapters.static_code_adapter import StaticCodeAdapter
from judge import Judge
from defender import Defender
from verifier import Verifier
from planner import Planner
from providers.mock import MockLLM
from datetime import datetime, timezone
import json
import os
import wandb
os.environ["WANDB_API_KEY"] = "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"

# Optional W&B import — fails gracefully if wandb is not installed or not configured
try:
    import wandb
    _WANDB_AVAILABLE = True
except ImportError:
    _WANDB_AVAILABLE = False

class Orchestrator:
    def __init__(
        self,
        repo_root: str,
        log_path: str = "logs/rounds.jsonl",
        provider: str = "mock",
        provider_seed: int = 42,
        use_wandb: bool = False,
        wandb_project: str = "mythosguard-arena",
        wandb_run_name: str | None = None,
    ):
        self.repo_root = repo_root
        self.provider = provider
        self.provider_seed = provider_seed
        self.attack_agent = SourceCodeAttackAgent(
            repo_root, provider=provider,
            mock_llm=MockLLM(seed=provider_seed) if provider == "mock" else None
        )
        self.adapter = StaticCodeAdapter()
        self.judge = Judge()
        self.defender = Defender()
        self.verifier = Verifier()
        self.planner = Planner()

        self.log_path = log_path

        # Initialise W&B run
        self._wandb_run = None
        if use_wandb and _WANDB_AVAILABLE:
            try:
                self._wandb_run = wandb.init(
                    project=wandb_project,
                    name=wandb_run_name or f"arena-seed{provider_seed}",
                    config={
                        "provider": provider,
                        "provider_seed": provider_seed,
                        "initial_weights": dict(self.planner.weights),
                    },
                    reinit=True,
                )
                print(f"[W&B] Experiment tracking active -> {self._wandb_run.url}")
            except Exception as exc:
                print(f"[W&B] Could not initialise run ({exc}). Continuing without tracking.")
                self._wandb_run = None
        elif use_wandb and not _WANDB_AVAILABLE:
            print("[W&B] wandb not installed. Run `pip install wandb` to enable tracking.")

    async def run_round(self, round_no: int, dry_run: bool = False):
        strategy = self.planner.choose()
        attack_info = await self.attack_agent.act({})
        target_file = attack_info["target_file"]
        attack_prompt = attack_info.get("attack_prompt")

        findings = self.adapter.analyze(target_file)
        verdict = await self.judge.evaluate(findings)

        patch = None
        verification = {"passed": None}
        if verdict.get("success"):
            finding = findings[0]
            patch = await self.defender.generate_patch(finding)
            verification = await self.verifier.verify(target_file, patch, verify_only=dry_run)

        log = {
            "round": round_no,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "strategy": strategy,
            "target_file": target_file,
            "attack_prompt": attack_prompt,
            "findings": findings,
            "verdict": verdict,
            "patch": patch,
            "verification": verification,
            "weights": self.planner.weights,
        }

        # Persist to JSONL
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")

        # Log structured metrics to W&B
        if self._wandb_run is not None:
            try:
                vuln_count = verdict.get("count", 0)
                metrics = {
                    "round": round_no,
                    "strategy": strategy,
                    "vulnerabilities_found": vuln_count,
                    "attack_succeeded": int(verdict.get("success", False)),
                    "patch_generated": int(patch is not None),
                    "patch_verified": int(bool(verification.get("passed"))),
                    "git_check_ok": int(bool(verification.get("git_check_ok"))),
                    "remaining_findings": len(verification.get("post_findings", [])),
                }
                # Log each strategy weight as a named metric
                for strategy_key, weight_val in self.planner.weights.items():
                    metrics[f"weight/{strategy_key}"] = weight_val

                # Log vulnerability type breakdown as binary flags
                for vtype in verdict.get("types", []):
                    metrics[f"vuln_type/{vtype}"] = 1

                wandb.log(metrics, step=round_no)
            except Exception as exc:
                print(f"[W&B] Logging error on round {round_no}: {exc}")

        # Update planner weights
        self.planner.update(strategy, verdict.get("success"))
        return log

    def finish(self):
        """Call after all rounds complete to finalise the W&B run."""
        if self._wandb_run is not None:
            try:
                # Log final summary of weight evolution
                for strategy_key, weight_val in self.planner.weights.items():
                    wandb.run.summary[f"final_weight/{strategy_key}"] = weight_val
                self._wandb_run.finish()
                print(f"[W&B] Run finalised -> {self._wandb_run.url}")
            except Exception as exc:
                print(f"[W&B] Could not finish run: {exc}")
