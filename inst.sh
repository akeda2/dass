#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

if [[ ! -f "dass.yaml" ]]; then
	echo "dass.yaml not found in ${SCRIPT_DIR}"
	exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
	echo "python3 is required but was not found in PATH."
	exit 1
fi

echo "Checking for pipx"
if ! command -v pipx >/dev/null 2>&1; then
	echo "pipx not found. Installing with python3 -m pip --user pipx"
	python3 -m pip install --user --upgrade pipx

	# pipx is typically installed to ~/.local/bin for user installs.
	export PATH="$HOME/.local/bin:$PATH"

	if ! command -v pipx >/dev/null 2>&1; then
		echo "pipx installation completed but pipx is not on PATH."
		echo "Try adding ~/.local/bin to PATH and run again."
		exit 1
	fi
fi

echo "Ensuring pipx path"
pipx ensurepath >/dev/null

echo "Installing dass with pipx"
pipx install --force "$SCRIPT_DIR"

echo "Running build integration import"
which gb && gb -I dass.yaml -a

echo "Install and integration import complete."
echo "If pipx is unavailable or undesired, fallback install is: make install (user-local by default) or ./build.sh"
