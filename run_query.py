"""Run one SQL file against a freshly built database and print the result as a table.

Usage:
    python run_query.py queries/01_top_customers_last_90_days.sql
    python run_query.py "SELECT * FROM v_otif_monthly"
"""

from __future__ import annotations

import sys
from pathlib import Path

from erp.build import build


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    arg = sys.argv[1]
    sql = Path(arg).read_text(encoding="utf-8") if arg.endswith(".sql") else arg
    cur = build().execute(sql)
    cols = [c[0] for c in cur.description]
    rows = [["" if v is None else str(v) for v in r] for r in cur.fetchall()]
    widths = [max(len(c), *(len(r[i]) for r in rows)) if rows else len(c) for i, c in enumerate(cols)]
    print("  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(v.ljust(w) for v, w in zip(r, widths)))
    print(f"\n{len(rows)} rows")


if __name__ == "__main__":
    main()
