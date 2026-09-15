from pathlib import Path


def test_required_bootstrap_files_exist():
    for path in ["README.md", "pyproject.toml", "scripts/preflight.sh"]:
        assert Path(path).exists(), path
