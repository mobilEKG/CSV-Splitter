#!/bin/sh
set -eu

# Build an x86_64 Linux package on a Debian 12 glibc baseline. The baseline is
# deliberate: building on a newer distribution can make the executable fail
# on older Linux systems because glibc is not backward compatible.
# ZIP is deliberate too: direct downloads commonly lose the executable mode.

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST_DIR=${DIST_DIR:-"$ROOT_DIR/dist"}
PYTHON=${PYTHON:-python3}
RAW_BINARY="$DIST_DIR/CSV_Splitter_linux"
ZIP_PATH="$DIST_DIR/CSV_Splitter_linux.zip"

if [ "$(uname -s)" != "Linux" ] || [ "$(uname -m)" != "x86_64" ]; then
    echo "This script must run on x86_64 Linux." >&2
    exit 1
fi

command -v zip >/dev/null 2>&1 || {
    echo "The zip command is required." >&2
    exit 1
}

# Remove only this build's known outputs so a retry cannot publish stale files.
rm -f "$RAW_BINARY" "$ZIP_PATH"

"$PYTHON" -m PyInstaller \
    --clean \
    --noupx \
    --noconsole \
    --noconfirm \
    --onefile \
    --windowed \
    --name CSV_Splitter_linux \
    --icon "$ROOT_DIR/app_icon.ico" \
    --add-data "$ROOT_DIR/app_icon.icns:." \
    "$ROOT_DIR/csv-splitter.py"

test -f "$RAW_BINARY"
chmod 755 "$RAW_BINARY"

# Store the mode in the archive so users can run the extracted file directly.
(cd "$DIST_DIR" && zip -9 CSV_Splitter_linux.zip CSV_Splitter_linux)
rm -f "$RAW_BINARY"
test -f "$ZIP_PATH"

echo "Created $ZIP_PATH"
