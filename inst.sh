#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMPLETION_DIR="${COMPLETION_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions}"
COMPLETION_SOURCE="${SCRIPT_DIR}/completions/dass"

cd "$SCRIPT_DIR"

if [[ ! -f "dass.yaml" ]]; then
	echo "dass.yaml not found in ${SCRIPT_DIR}"
	exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
	echo "python3 is required but was not found in PATH."
	exit 1
fi

if [[ ! -f "$COMPLETION_SOURCE" ]]; then
	echo "Bash completion not found at $COMPLETION_SOURCE"
	exit 1
fi

install_completion() {
	echo "Installing Bash completion to ${COMPLETION_DIR}"
	if mkdir -p "$COMPLETION_DIR" 2>/dev/null && [[ -w "$COMPLETION_DIR" ]]; then
		install -v -m 644 "$COMPLETION_SOURCE" "${COMPLETION_DIR}/dass"
	elif command -v sudo >/dev/null 2>&1; then
		sudo mkdir -p "$COMPLETION_DIR"
		sudo install -v -m 644 "$COMPLETION_SOURCE" "${COMPLETION_DIR}/dass"
	else
		echo "No write access to ${COMPLETION_DIR} and sudo is not available."
		exit 1
	fi
}

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

install_completion

echo "Running build integration import"
which gb && gb -I dass.yaml -a

echo "Install and integration import complete."
echo "If pipx is unavailable or undesired, fallback install is: make install (user-local by default) or ./build.sh"
