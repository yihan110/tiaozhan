"""允许 `python -m md_sorter ...` 直接调用 CLI。"""

from .cli import main

raise SystemExit(main())
