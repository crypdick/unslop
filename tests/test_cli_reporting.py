"""Exercise terminal output and file errors through the CLI entry point."""

import io
import sys
from pathlib import Path

import pytest
from detect_slop import main


def test_unreadable_file_warns_and_continues(tmp_path, monkeypatch, capsys):
    unreadable = tmp_path / "unreadable.md"
    readable = tmp_path / "readable.md"
    unreadable.touch()
    readable.write_text("The bridge took three years to build and cost twice the estimate overall.")
    read_text = Path.read_text

    def read_or_fail(path: Path, *_args: object, **_kwargs: object) -> str:
        if path == unreadable:
            raise PermissionError("permission denied")
        return read_text(path, encoding="utf-8")

    monkeypatch.setattr(Path, "read_text", read_or_fail)
    monkeypatch.setattr(sys, "argv", ["detect_slop.py", str(unreadable), str(readable)])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
    output = capsys.readouterr()
    assert f"warning: skipping {unreadable}: permission denied" in output.err
    assert "No slop detected" in output.out


@pytest.mark.parametrize("no_color", [False, True])
def test_terminal_color_can_be_disabled(monkeypatch, no_color):
    output = io.StringIO()
    monkeypatch.setattr(output, "isatty", lambda: True)
    monkeypatch.setattr(sys, "stdout", output)
    monkeypatch.setattr(
        sys, "stdin", io.StringIO("This project is a testament to the hard work of the team.")
    )
    monkeypatch.setattr(sys, "argv", ["detect_slop.py", "-"] + (["--no-color"] if no_color else []))
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    assert "significance inflation" in output.getvalue()
    assert ("\033[91m" in output.getvalue()) is not no_color


def test_summary_ranks_and_limits_worst_offenders(tmp_path, monkeypatch, capsys):
    paths = []
    for index in range(6):
        path = tmp_path / f"sample-{index}.md"
        path.write_text("This project is a testament to the hard work of the team. " + "plain " * index * 10)
        paths.append(str(path))
    monkeypatch.setattr(sys, "argv", ["detect_slop.py", *reversed(paths)])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    summary = capsys.readouterr().out.split("Worst offenders:\n")[1]
    assert len(summary.splitlines()) == 5
    assert [line.split()[-1] for line in summary.splitlines()] == paths[:5]
