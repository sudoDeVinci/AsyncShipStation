#!/usr/bin/env python3
"""Build and upload a package to PyPI.

This script:
1. Cleans the ``dist`` directory.
2. Builds a source distribution and a wheel.
3. Uploads the distribution to PyPI using a token stored in the ``PIPY_TOKEN`` environment variable.
"""

from __future__ import annotations

import subprocess
import sys
from os import getenv
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def run_cmd(
    cmd: str, *, cwd: Optional[Path] = None, capture: bool = False
) -> subprocess.CompletedProcess:
    """Run a shell command and optionally capture its output."""
    print(f"> {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
    )
    if capture:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    return result


def main() -> None:
    token = getenv("PIPY_TOKEN")
    if not token:
        raise RuntimeError("Environment variable 'PIPY_TOKEN' not set")

    # 1. Remove old builds
    run_cmd("rm -rf dist")

    # 2. Build the package
    run_cmd("python3 -m build")

    # 3. Upload to PyPI
    run_cmd(f"twine upload dist/* -u __token__ -p {token}", capture=True)


if __name__ == "__main__":
    main()
