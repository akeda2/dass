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


def test_help_works(tmp_path: Path) -> None:
    result = run_dass(tmp_path, "--help")
    assert result.returncode == 0
    assert "subcommands" in result.stdout


def test_missing_subcommand_returns_2(tmp_path: Path) -> None:
    result = run_dass(tmp_path)
    assert result.returncode == 2


def test_add_document_creates_file(tmp_path: Path) -> None:
    result = run_dass(tmp_path, "add", "10", "First")
    assert result.returncode == 0
    assert (tmp_path / "010First.txt").exists()


def test_add_chapter_creates_directory(tmp_path: Path) -> None:
    result = run_dass(tmp_path, "add", "20", "Chapter", "-c")
    assert result.returncode == 0
    assert (tmp_path / "020Chapter").is_dir()


def test_rename_document_changes_prefix_and_title(tmp_path: Path) -> None:
    old_file = tmp_path / "010Old.txt"
    old_file.write_text("hello", encoding="utf-8")

    result = run_dass(tmp_path, "rename", "10", "30", "New", "-d", ".")
    assert result.returncode == 0
    assert not old_file.exists()
    assert (tmp_path / "030New.txt").exists()


def test_rename_nested_directory_uses_discovered_parent(tmp_path: Path) -> None:
    parent = tmp_path / "010Outer"
    old_directory = parent / "020Inner"
    old_directory.mkdir(parents=True)

    result = run_dass(tmp_path, "rename", "20", "30", "Renamed", "-d", ".")

    assert result.returncode == 0
    assert not old_directory.exists()
    assert (parent / "030Renamed").is_dir()


def test_compile_save_prompts_once_and_reuses_output_name(tmp_path: Path) -> None:
    (tmp_path / "010Alpha.txt").write_text("alpha\n", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "--save", stdin_text="book\nMy Title\n")

    assert result.returncode == 0
    assert result.stdout.count("Output name:") == 1
    assert (tmp_path / "book.yaml").exists()
    assert (tmp_path / "book.text").exists()


def test_compile_generates_expected_outputs(tmp_path: Path) -> None:
    chapter = tmp_path / "010Chapter"
    chapter.mkdir()
    (chapter / "010Alpha.txt").write_text("alpha\n", encoding="utf-8")
    (chapter / "020Beta.txt").write_text("beta\n", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "-d", ".", "book", "-m", "-w", "-t", "My Title")
    assert result.returncode == 0

    output_text = (tmp_path / "book.text").read_text(encoding="utf-8-sig")
    output_md = (tmp_path / "book.md").read_text(encoding="utf-8-sig")
    output_html = (tmp_path / "book.html").read_text(encoding="utf-8-sig")

    assert "My Title" in output_text
    assert "Alpha" in output_text
    assert "Beta" in output_text
    assert output_text.find("Alpha") < output_text.find("Beta")

    assert "# My Title" in output_md
    assert "### Alpha" in output_md
    assert "### Beta" in output_md
    assert "<h1>My Title</h1>" in output_html


def test_compile_disable_bom_writes_plain_utf8(tmp_path: Path) -> None:
    (tmp_path / "010Alpha.txt").write_text("alpha\n", encoding="utf-8")

    result = run_dass(tmp_path, "compile", "book", "--disable_bom")

    assert result.returncode == 0
    assert not (tmp_path / "book.text").read_bytes().startswith(b"\xef\xbb\xbf")


def test_compile_absolute_directory_uses_local_chapter_name(tmp_path: Path) -> None:
    source = tmp_path / "source"
    chapter = source / "010Chapter"
    chapter.mkdir(parents=True)
    (chapter / "010Alpha.txt").write_text("alpha\n", encoding="utf-8")
    output_directory = tmp_path / "output"
    output_directory.mkdir()

    result = run_dass(output_directory, "compile", "-d", str(source), "book", "-m")

    assert result.returncode == 0
    output_markdown = (output_directory / "book.md").read_text(encoding="utf-8-sig")
    assert "## Chapter" in output_markdown
    assert str(source) not in output_markdown


def test_clean_removes_outputs_but_keeps_readme(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("keep\n", encoding="utf-8")
    (tmp_path / "book.text").write_text("x\n", encoding="utf-8")
    (tmp_path / "book.md").write_text("x\n", encoding="utf-8")
    (tmp_path / "book.html").write_text("x\n", encoding="utf-8")

    result = run_dass(tmp_path, "clean")
    assert result.returncode == 0

    assert (tmp_path / "README.md").exists()
    assert not (tmp_path / "book.text").exists()
    assert not (tmp_path / "book.md").exists()
    assert not (tmp_path / "book.html").exists()
