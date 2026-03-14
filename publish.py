#!/usr/bin/env python3
"""Build and publish EchoRev to PyPI.

Usage:
    python publish.py          # Build only
    python publish.py test     # Build + upload to TestPyPI
    python publish.py release  # Build + upload to PyPI
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
VERSION_FILE = ROOT / "echorev" / "__init__.py"


def run(cmd, **kwargs):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, **kwargs)
    if result.returncode != 0:
        print(f"FAILED (exit {result.returncode})")
        sys.exit(result.returncode)
    return result


def ensure_tools():
    for pkg in ("build", "twine"):
        try:
            __import__(pkg)
        except ImportError:
            print(f"Installing {pkg}...")
            run(f"{sys.executable} -m pip install {pkg}")


def clean():
    for d in (DIST, ROOT / "build", ROOT / "echorev.egg-info"):
        if d.exists():
            print(f"Removing {d}")
            shutil.rmtree(d)


def get_version() -> str:
    content = VERSION_FILE.read_text(encoding="utf-8")
    m = re.search(r"__version__\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", content)
    if not m:
        print("ERROR: cannot parse version from __init__.py")
        sys.exit(1)
    return m.group(1)


def bump_version() -> str:
    """Bump patch version and return new version."""
    content = VERSION_FILE.read_text(encoding="utf-8")
    m = re.search(r"(__version__\s*=\s*['\"](\d+\.\d+\.)(\d+)['\"])", content)
    if not m:
        print("ERROR: cannot parse version")
        sys.exit(1)
    old_v = m.group(2) + m.group(3)
    new_v = m.group(2) + str(int(m.group(3)) + 1)
    VERSION_FILE.write_text(
        content.replace(m.group(1), f'__version__ = "{new_v}"'),
        encoding="utf-8",
    )
    print(f"Version: {old_v} -> {new_v}")
    return new_v


def build():
    clean()
    run(f"{sys.executable} -m build")
    wheels = list(DIST.glob("*.whl"))
    tarballs = list(DIST.glob("*.tar.gz"))
    print(f"\nBuilt: {[f.name for f in wheels + tarballs]}")


def check():
    run(f"{sys.executable} -m twine check dist/*")


def upload(repository=None):
    cmd = f"{sys.executable} -m twine upload"
    if repository:
        cmd += f" --repository {repository}"
    cmd += " dist/*"
    run(cmd)


def main():
    ensure_tools()

    action = sys.argv[1] if len(sys.argv) > 1 else "build"

    if action == "build":
        build()
        check()
        print(f"\nBuild complete (version {get_version()}). To upload run:")
        print("  python publish.py test      # TestPyPI")
        print("  python publish.py release   # PyPI")

    elif action == "bump":
        new_v = bump_version()
        print(f"\nVersion bumped to {new_v}")

    elif action == "test":
        bump_version()
        build()
        check()
        print("\nUploading to TestPyPI...")
        upload("testpypi")
        print("\nDone! Install with:")
        print("  pip install --index-url https://test.pypi.org/simple/ echorev")

    elif action == "release":
        bump_version()
        build()
        check()
        print("\nUploading to PyPI...")
        upload()
        print("\nDone! Install with:")
        print("  pip install echorev")

    else:
        print(f"Unknown action: {action}")
        print("Usage: python publish.py [build|bump|test|release]")
        sys.exit(1)


if __name__ == "__main__":
    main()