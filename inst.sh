#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BUILD_SCRIPT="${SCRIPT_DIR}/build.sh"

echo "inst.sh is deprecated. Running build.sh instead."

if [[ ! -f "$BUILD_SCRIPT" ]]; then
	echo "build.sh not found at ${BUILD_SCRIPT}"
	exit 1
fi

exec bash "$BUILD_SCRIPT" "$@"
