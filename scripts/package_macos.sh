#!/bin/sh
set -eu

# Build the arm64 PyInstaller executable and wrap it in a Finder-openable app.
# The script must run on macOS because PyInstaller does not cross-compile macOS
# binaries from the hosted Linux CNB runners. A custom CNB Mac runner is needed
# before this script can be called directly by the CNB release pipeline.

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST_DIR=${DIST_DIR:-"$ROOT_DIR/dist"}
PYTHON=${PYTHON:-python3}
APP_DIR="$DIST_DIR/CSV Splitter.app"
RAW_BINARY="$DIST_DIR/CSV_Splitter"
ZIP_PATH="$DIST_DIR/CSV_Splitter_macos.zip"

if [ "$(uname -s)" != "Darwin" ]; then
    echo "This script must run on macOS." >&2
    exit 1
fi

command -v ditto >/dev/null 2>&1 || {
    echo "The macOS ditto command is required." >&2
    exit 1
}

# Keep build outputs out of source control and remove only this build's known
# paths so a retry cannot leave a stale app or archive in the release folder.
rm -rf "$APP_DIR" "$ZIP_PATH" "$RAW_BINARY"

"$PYTHON" -m PyInstaller \
    --clean \
    --noupx \
    --noconsole \
    --noconfirm \
    --onefile \
    --windowed \
    --name CSV_Splitter \
    --icon "$ROOT_DIR/app_icon.icns" \
    --add-data "$ROOT_DIR/app_icon.icns:." \
    "$ROOT_DIR/csv-splitter.py"

test -f "$RAW_BINARY"
mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources"

# A downloaded bare executable commonly loses its executable bit. The app
# bundle restores it and gives Finder a standard launch target.
cp "$RAW_BINARY" "$APP_DIR/Contents/MacOS/CSV_Splitter"
chmod 755 "$APP_DIR/Contents/MacOS/CSV_Splitter"
cp "$ROOT_DIR/packaging/macos/Info.plist" "$APP_DIR/Contents/Info.plist"
cp "$ROOT_DIR/app_icon.icns" "$APP_DIR/Contents/Resources/app_icon.icns"

# ditto preserves the app bundle layout and executable mode in the archive.
ditto -c -k --sequesterRsrc --keepParent "$APP_DIR" "$ZIP_PATH"
test -f "$ZIP_PATH"

echo "Created $ZIP_PATH"
