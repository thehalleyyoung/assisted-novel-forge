#!/usr/bin/env python3
import sys
from pathlib import Path
r=Path(sys.argv[1]); raise SystemExit(0 if (r/'plot/outline.md').exists() else 1)
