from defender import Defender
import tempfile
from pathlib import Path


def test_write_patch_file_creates_file(tmp_path):
    d = Defender()
    patch = {"diff": "--- a/foo\n+++ b/foo\n"}
    out = tmp_path / "fix.patch"
    d.write_patch_file(patch, str(out))
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "--- a/foo" in content
