import asyncio
import argparse
import os

from orchestrator import Orchestrator

console_dashboard = None
try:
    import ui.console_dashboard as console_dashboard
except Exception:
    console_dashboard = None


async def main(dry_run: bool, provider: str, provider_seed: int, use_wandb: bool, wandb_project: str):
    repo_root = os.path.dirname(__file__)
    orch = Orchestrator(
        repo_root,
        provider=provider,
        provider_seed=provider_seed,
        use_wandb=use_wandb,
        wandb_project=wandb_project,
    )
    rounds = 3
    for r in range(1, rounds + 1):
        log = await orch.run_round(r, dry_run=dry_run)

        use_rich = False
        if console_dashboard is not None:
            try:
                use_rich = (
                    getattr(console_dashboard, "console", None) is not None
                    and console_dashboard.console.is_terminal
                )
            except Exception:
                use_rich = False

        if use_rich:
            console_dashboard.render_round_summary(log)
        elif console_dashboard is not None and hasattr(console_dashboard, "render_plain"):
            console_dashboard.render_plain(log)
        else:
            print(f"=== Strategy: {log['strategy']} ===")
            print("Findings:")
            for f in log["findings"]:
                print(f"  - {f.get('file_path')}:{f.get('line')} {f.get('type')} -> {f.get('line_text')}")
            print("\nPatch:")
            if log.get("patch"):
                print(log["patch"].get("diff"))
            else:
                print("  No patch generated")
            print("\nVerification:")
            for k, v in log["verification"].items():
                print(f"  - {k}: {v}")
            print()

    # Finalise W&B run (writes summaries and closes the experiment)
    orch.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Do not apply patches; only simulate verification")
    parser.add_argument("--no-rich", action="store_true",
                        help="Disable Rich console output; use plain text")
    parser.add_argument("--provider", default="mock", choices=["mock"],
                        help="LLM provider to use (currently only mock is supported)")
    parser.add_argument("--provider-seed", type=int, default=42,
                        help="Seed for deterministic mock responses")
    parser.add_argument("--clean", action="store_true",
                        help="Clear old logs before running new test")
    parser.add_argument("--wandb", action="store_true",
                        help="Enable Weights & Biases experiment tracking")
    parser.add_argument("--wandb-project", default="mythosguard-arena",
                        help="W&B project name (default: mythosguard-arena)")
    args = parser.parse_args()

    if args.clean:
        log_path = "logs/rounds.jsonl"
        if os.path.exists(log_path):
            os.remove(log_path)
            print(f"Cleared old logs: {log_path}")

    asyncio.run(main(
        dry_run=args.dry_run,
        provider=args.provider,
        provider_seed=args.provider_seed,
        use_wandb=args.wandb,
        wandb_project=args.wandb_project,
    ))
