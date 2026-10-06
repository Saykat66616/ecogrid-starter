"""Run the end-to-end demo on any operating system:  python run_demo.py"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for folder in ("services", "libs"):
    sys.path.insert(0, str(ROOT / folder))
sys.path.insert(0, str(ROOT))

from composition.demo import run  # noqa: E402

if __name__ == "__main__":
    run()
