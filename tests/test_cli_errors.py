from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "dass.py"


def run_dass(tmp_path: Path, *args: str, stdin_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=tmp_path,
        input=stdin_text,
        capture_output=True,
        text=True,
        check=False,
    )


def test_add_document_conflict_returns_error(tmp_path: Path) -> None:
    existing = tmp_path / "010First.txt"
    existing.write_text("already here\n", encoding="utf-8")

    result = run_dass(tmp_path, "add", "10", "First")

    assert result.returncode == 1
    assert "File already exists" in result.stdout
    assert existing.read_text(encoding="utf-8") == "already here\n"


def test_add_chapter_conflict_returns_error(tmp_path: Path) -> None:
    existing = tmp_path / "010Chapter"
    existing.mkdir()

    result = run_dass(tmp_path, "add", "10", "Chapter", "-c")

    assert result.returncode == 1
    assert "Directory already exists" in result.stdout


def test_rename_conflict_keeps_original_file(tmp_path: Path) -> None:
    original = tmp_path / "010Old.txt"
    original.write_text("old\n", encoding="utf-8")
    target = tmp_path / "020Taken.txt"
    target.write_text("taken\n", encoding="utf-8")

    result = run_dass(tmp_path, "rename", "10", "20", "Taken", "-d", ".")

    assert result.returncode == 1
    assert "File already exists" in result.stdout
    assert original.exists()
    assert target.exists()


def test_compile_no_overwrite_preserves_existing_output(tmp_path: Path) -> None:
    chapter = tmp_path / "010Chapter"
    chapter.mkdir()
    (chapter / "010Alpha.txt").write_text("alpha\n", encoding="utf-8")

    existing_output = tmp_path / "book.text"
    existing_output.write_text("do not overwrite\n", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "-d", ".", "book", "-n")

    assert result.returncode == 1
    assert "--no_overwrite is set" in result.stdout
    assert existing_output.read_text(encoding="utf-8") == "do not overwrite\n"


def test_compile_load_missing_file_reports_error(tmp_path: Path) -> None:
    result = run_dass(tmp_path, "compile", "-l", "missing.yaml")

    assert result.returncode == 1
    assert "File not found: missing.yaml" in result.stdout


def test_compile_load_empty_file_reports_error(tmp_path: Path) -> None:
    (tmp_path / "empty.yaml").write_text("", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "-l", "empty.yaml")

    assert result.returncode == 1
    assert "No settings found in file: empty.yaml" in result.stdout
    assert "Traceback" not in result.stderr


def test_compile_missing_directory_preserves_existing_output(tmp_path: Path) -> None:
    existing_output = tmp_path / "book.text"
    existing_output.write_text("keep me\n", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "-d", "missing", "book")

    assert result.returncode == 1
    assert "Directory not found: missing" in result.stdout
    assert existing_output.read_text(encoding="utf-8") == "keep me\n"


def test_compile_no_overwrite_ignores_unrequested_outputs(tmp_path: Path) -> None:
    (tmp_path / "010Alpha.txt").write_text("alpha\n", encoding="utf-8")
    (tmp_path / "book.md").write_text("unrelated\n", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "book", "--no_overwrite")

    assert result.returncode == 0
    assert (tmp_path / "book.text").exists()
    assert (tmp_path / "book.md").read_text(encoding="utf-8") == "unrelated\n"


def test_rename_missing_document_returns_error(tmp_path: Path) -> None:
    result = run_dass(tmp_path, "rename", "10", "20", "Missing")

    assert result.returncode == 1
    assert "No document or directory found with number 010" in result.stdout
