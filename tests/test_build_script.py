from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_skip_install_preserves_built_binary() -> None:
    script = (REPO_ROOT / "build.sh").read_text(encoding="utf-8")

    cleanup = script.split('echo "Cleaning build artifacts"', maxsplit=1)[1]
    skip_branch, install_branch = cleanup.split("else", maxsplit=1)
    assert "rm -rf ./dist" not in skip_branch
    assert "rm -rf ./dist" in install_branch