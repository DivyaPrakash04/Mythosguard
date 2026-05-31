import asyncio
from orchestrator import Orchestrator
import os


def test_end_to_end_patch_and_verify(tmp_path):
    # Use a temp copy of the sample vulnerable file to avoid modifying repo files
    project_root = os.path.dirname(os.path.dirname(__file__))
    sample = os.path.join(project_root, "sample_vulnerable_code", "vuln.py")
    tmpdir = tmp_path / "demo"
    tmpdir.mkdir()
    # copy sample into temp dir structure
    import shutil

    sample_dst_dir = tmpdir / "sample_vulnerable_code"
    sample_dst_dir.mkdir()
    sample_dst = sample_dst_dir / "vuln.py"
    shutil.copy2(sample, sample_dst)

    orch = Orchestrator(str(tmpdir))

    # Run a single round
    log = asyncio.get_event_loop().run_until_complete(orch.run_round(1))

    assert log["verdict"]["count"] >= 1
    assert log["patch"] is not None
    assert "diff" in log["patch"] and log["patch"]["diff"]
    assert log["verification"]["passed"] is True
