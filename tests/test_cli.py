"""Behavior checks for the writing-pattern scanner."""

import json
import subprocess
import sys
from pathlib import Path

from detect_slop import collect_files


class TestCollectFiles:
    def test_single_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("hello")
        result = collect_files([str(f)])
        assert len(result) == 1
        assert result[0] == f

    def test_directory_finds_text_files(self, tmp_path):
        (tmp_path / "a.md").write_text("hello")
        (tmp_path / "b.txt").write_text("world")
        (tmp_path / "c.png").write_bytes(b"\x89PNG")  # not text
        result = collect_files([str(tmp_path)])
        extensions = {r.suffix for r in result}
        assert ".md" in extensions
        assert ".txt" in extensions
        assert ".png" not in extensions

    def test_skips_git_dir(self, tmp_path):
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("bare = false")
        (tmp_path / "readme.md").write_text("hello")
        result = collect_files([str(tmp_path)])
        paths_str = [str(r) for r in result]
        assert not any(".git" in p for p in paths_str)

    def test_skips_node_modules(self, tmp_path):
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {}")
        (tmp_path / "app.js").write_text("console.log('hi')")
        result = collect_files([str(tmp_path)])
        assert len(result) == 1
        assert result[0].name == "app.js"

    def test_nonexistent_path_skipped(self, tmp_path, capsys):
        result = collect_files([str(tmp_path / "nope")])
        assert len(result) == 0
        assert "warning" in capsys.readouterr().err

    def test_nested_directories(self, tmp_path):
        sub = tmp_path / "src" / "components"
        sub.mkdir(parents=True)
        (sub / "button.tsx").write_text("export const Button = () => {}")
        (tmp_path / "readme.md").write_text("hello")
        result = collect_files([str(tmp_path)])
        assert len(result) == 2


# ---------------------------------------------------------------------------
# CLI (subprocess tests)
# ---------------------------------------------------------------------------

SCRIPT = str(Path(__file__).resolve().parent.parent / "scripts" / "detect_slop.py")


class TestCLI:
    def test_stdin_clean_exit_0(self):
        result = subprocess.run(
            [sys.executable, SCRIPT, "-"],
            input="The bridge took three years to build and cost twice the estimate overall.",
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "No slop detected" in result.stdout

    def test_stdin_sloppy_exit_1(self):
        text = (
            "In today's rapidly evolving digital landscape, organizations are "
            "leveraging cutting-edge AI to enhance operational efficiency. "
            "This groundbreaking shift serves as a testament to innovation. "
            "Let's delve into the multifaceted implications of this pivotal change."
        )
        result = subprocess.run(
            [sys.executable, SCRIPT, "-"],
            input=text,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1

    def test_file_argument(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "The building serves as a community center for the neighborhood. "
            "It is a testament to the community's dedication and commitment. "
            "The meticulous design showcases the intricate interplay of form and function."
        )
        result = subprocess.run(
            [sys.executable, SCRIPT, str(f)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "serves as" in result.stdout or "testament" in result.stdout

    def test_directory_argument(self, tmp_path):
        (tmp_path / "clean.md").write_text("The team shipped the feature on Friday. It works well so far.")
        (tmp_path / "sloppy.md").write_text(
            "This groundbreaking initiative is a testament to the team's meticulous approach. "
            "The intricate tapestry of solutions leverages robust paradigms and holistic synergy. "
            "Let's delve into the multifaceted implications of this pivotal transformation."
        )
        result = subprocess.run(
            [sys.executable, SCRIPT, str(tmp_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "sloppy.md" in result.stdout

    def test_json_output(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "The restaurant boasts a diverse array of dishes and a rich tapestry of flavors. "
            "It's worth noting that experts argue the menu is truly unique and exceptional."
        )
        json_file = tmp_path / "report.json"
        subprocess.run(
            [sys.executable, SCRIPT, "--json", str(json_file), str(f)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert json_file.exists()
        data = json.loads(json_file.read_text())
        assert len(data) == 1
        assert data[0]["word_count"] > 0
        assert data[0]["slop_score"] > 0
        assert len(data[0]["findings"]) > 0

    def test_threshold_filters(self, tmp_path):
        f = tmp_path / "mild.md"
        f.write_text(
            "The city boasts a lively arts scene that attracts visitors from across the region. "
            "Local restaurants serve dishes made with ingredients sourced from nearby farms."
        )
        # With very high threshold, should exit 0
        result = subprocess.run(
            [sys.executable, SCRIPT, "--threshold", "99", str(f)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_no_text_files_exit_2(self, tmp_path):
        (tmp_path / "image.png").write_bytes(b"\x89PNG")
        result = subprocess.run(
            [sys.executable, SCRIPT, str(tmp_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2
        assert "No text files" in result.stderr

    def test_verbose_shows_low_severity(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text(
            "Additionally, the team has expanded its product line. "
            "The new products include several interesting items for sale. "
            "Customers have responded well to the changes so far this year."
        )
        verbose = subprocess.run(
            [sys.executable, SCRIPT, "-v", str(f)],
            check=False,
            capture_output=True,
            text=True,
        )
        quiet = subprocess.run(
            [sys.executable, SCRIPT, str(f)],
            check=False,
            capture_output=True,
            text=True,
        )
        # Verbose output should be longer (includes low-severity findings)
        assert len(verbose.stdout) >= len(quiet.stdout)
