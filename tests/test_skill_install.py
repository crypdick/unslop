"""Exercise the detector after copying only the standalone skill directory."""

import shutil
import subprocess
import sys
from pathlib import Path


def test_standalone_skill_detector_from_unrelated_directory(tmp_path):
    source = Path(__file__).resolve().parents[1] / "skills" / "unslop"
    installed = tmp_path / "installed" / "unslop"
    shutil.copytree(source, installed)
    target = tmp_path / "writing"
    target.mkdir()
    (target / "draft.md").write_text("The bridge took three years to build and cost twice the estimate.")
    result = subprocess.run(
        [sys.executable, str(installed / "scripts" / "detect_slop.py"), "draft.md"],
        cwd=target,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "No slop detected" in result.stdout


def test_skill_bundle_contains_regular_synchronized_modules():
    root = Path(__file__).resolve().parents[1]
    for name in ("detect_slop.py", "slop_patterns.py", "slop_scanner.py", "slop_reports.py"):
        bundled = root / "skills" / "unslop" / "scripts" / name
        assert not bundled.is_symlink(), "GitHub ZIP installers cannot install external symlinks"
        assert bundled.read_bytes() == (root / "scripts" / name).read_bytes()
