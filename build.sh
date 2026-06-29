#!/usr/bin/env bash

set -euo pipefail

# Set DEBUG=1 to enable shell tracing.
[[ "${DEBUG:-0}" == "1" ]] && set -x

APPNAME="dass"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
SKIP_INSTALL="${SKIP_INSTALL:-0}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
	echo "python3 is required but was not found in PATH."
	exit 1
fi

if [[ ! -f requirements.txt ]]; then
	echo "requirements.txt not found in $SCRIPT_DIR"
	exit 1
fi

if [[ ! -f "${APPNAME}.py" ]]; then
	echo "${APPNAME}.py not found in $SCRIPT_DIR"
	exit 1
fi

if command -v dpkg >/dev/null 2>&1; then
	echo "Checking for python3-venv package"
	if ! dpkg -l | grep -q '^ii  python3-venv'; then
		echo "Warning: python3-venv package not detected by dpkg."
	fi
fi

echo "Checking for venv module"
python3 -m venv --help >/dev/null 2>&1 || { echo "Python venv module is unavailable."; exit 1; }

echo "Creating or reusing a virtual environment"
if [[ ! -d venv ]]; then
	python3 -m venv venv
fi

echo "Activating the virtual environment"
# shellcheck disable=SC1091
source venv/bin/activate

if ! python -m pip --version >/dev/null 2>&1; then
	echo "pip is missing in the virtual environment. Attempting bootstrap with ensurepip."
	python -m ensurepip --upgrade >/dev/null 2>&1 || {
		echo "Failed to bootstrap pip in venv. Install python3-pip or ensurepip support."
		exit 1
	}
fi

echo "Installing dependencies"
python -m pip install -r requirements.txt

echo "Running PyInstaller"
python -m PyInstaller --onefile "${APPNAME}.py" --clean --noupx

if [[ "$SKIP_INSTALL" == "1" ]]; then
	echo "SKIP_INSTALL=1 set, skipping install step. Built binary at dist/${APPNAME}"
else
	echo "Installing to ${INSTALL_DIR}"
	if [[ -w "$INSTALL_DIR" ]]; then
		install -v -m 755 "dist/${APPNAME}" "${INSTALL_DIR}/${APPNAME}"
	elif command -v sudo >/dev/null 2>&1; then
		sudo install -v -m 755 "dist/${APPNAME}" "${INSTALL_DIR}/${APPNAME}"
	else
		echo "No write access to ${INSTALL_DIR} and sudo is not available."
		exit 1
	fi
fi

deactivate

echo "Cleaning build artifacts"
rm -rf ./dist ./build ./*.spec ./*.pyc ./*.log

if [[ "$SKIP_INSTALL" == "1" ]]; then
	echo "Build complete."
else
	echo "Build complete. Installed to ${INSTALL_DIR}/${APPNAME}"
fi
