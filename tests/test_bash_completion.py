from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETION = REPO_ROOT / "completions" / "dass"


def complete(tmp_path: Path, *words: str) -> list[str]:
    quoted_words = " ".join(shlex.quote(word) for word in words)
    command = f"""
source {shlex.quote(str(COMPLETION))}
COMP_WORDS=({quoted_words})
COMP_CWORD=$((${{#COMP_WORDS[@]}} - 1))
_dass
printf '%s\n' "${{COMPREPLY[@]}}"
"""
    result = subprocess.run(
        ["bash", "-c", command],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


def test_completes_commands(tmp_path: Path) -> None:
    assert "compile" in complete(tmp_path, "dass", "co")


def test_completes_compile_options_for_alias(tmp_path: Path) -> None:
    completions = complete(tmp_path, "dass", "c", "--")

    assert "--markdown" in completions
    assert "--no_overwrite" in completions


def test_completes_directories_and_yaml_files(tmp_path: Path) -> None:
    (tmp_path / "chapters").mkdir()
    (tmp_path / "book.yaml").touch()
    (tmp_path / "notes.txt").touch()

    assert "chapters" in complete(tmp_path, "dass", "compile", "--directory", "ch")
    load_completions = complete(tmp_path, "dass", "compile", "--load", "b")
    assert "book.yaml" in load_completions
    assert "notes.txt" not in load_completions


def test_installers_install_completion_file() -> None:
    for script_name in ("build.sh", "inst.sh"):
        script = (REPO_ROOT / script_name).read_text(encoding="utf-8")
        assert "COMPLETION_DIR" in script
        assert "COMPLETION_SOURCE" in script
        assert "install_completion" in script