from __future__ import annotations

import shutil
import subprocess
import sys
from os import getenv
from pathlib import Path
from typing import Optional, no_type_check

from dotenv import load_dotenv

load_dotenv()


@no_type_check
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


@no_type_check
def main() -> None:
    token = getenv("PIPY_TOKEN")
    print(f"PIPY_TOKEN: {token}")
    if not token:
        raise RuntimeError("Environment variable 'PIPY_TOKEN' not set")

    # 1. Remove old builds
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("> Removed dist/")

    # 2. Build the package
    run_cmd("python -m build")

    # 3. Upload to PyPI
    run_cmd(f"twine upload dist/* -u __token__ -p {token}", capture=True)


if __name__ == "__main__":
    main()
