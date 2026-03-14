#!/bin/bash
# Build package only (no upload to PyPI)

set -e

echo "Cleaning old builds..."
rm -rf dist/ build/ *.egg-info echorev/*.egg-info

echo "Building package..."
python3 -m build

echo "Build complete. Files in dist/"
ls -la dist/