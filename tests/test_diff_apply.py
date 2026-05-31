from verifier import apply_unified_diff


def test_apply_unified_diff_simple_replace():
    orig = ["line1\n", "line2\n", "line3\n"]
    diff_text = (
        "@@ -1,3 +1,3 @@\n"
        " line1\n"
        "-line2\n"
        "+LINE2\n"
        " line3\n"
    )
    out = apply_unified_diff(orig, diff_text)
    assert "LINE2\n" in out
    assert "line2\n" not in out
