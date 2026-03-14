#!/bin/bash
# Build and publish EchoRev to PyPI

set -e

echo "Cleaning old builds..."
rm -rf dist/ build/ *.egg-info echorev/*.egg-info

echo "Building package..."
python3 -m build

echo "Uploading to PyPI..."
python3 -m twine upload dist/*

echo "Done!"