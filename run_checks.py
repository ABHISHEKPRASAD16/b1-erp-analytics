"""Run every data-quality check and write a Markdown report.

Usage:
    python run_checks.py            # report to reports/dq_report.md
    python run_checks.py --strict   # exit with code 1 if any error-level check finds rows
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from erp.build import CHECKS_DIR, ROOT, build


def read_meta(sql: str) -> dict[str, str]:
    meta = {}
    for line in sql.splitlines():
        if line.startswith("-- ") and ":" in line:
            key, value = line[3:].split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


def run_checks(conn) -> list[dict]:
    results = []
    for path in sorted(CHECKS_DIR.glob("*.sql")):
        sql = path.read_text(encoding="utf-8")
        meta = read_meta(sql)
        cur = conn.execute(sql)
        rows = cur.fetchall()
        results.append({
            "name": path.stem,
            "severity": meta.get("severity", "error"),
            "description": meta.get("description", ""),
            "columns": [c[0] for c in cur.description],
            "rows": [tuple(r) for r in rows],
        })
    return results


def to_markdown(results: list[dict]) -> str:
    out = ["# Data quality report", "",
           "| Check | Severity | Rows found | What it looks for |", "|---|---|---:|---|"]
    for r in results:
        out.append(f"| `{r['name']}` | {r['severity']} | {len(r['rows'])} | {r['description']} |")
    for r in results:
        if not r["rows"]:
            continue
        out += ["", f"## {r['name']}", "", r["description"], "",
                "| " + " | ".join(r["columns"]) + " |",
                "|" + "---|" * len(r["columns"])]
        out += ["| " + " | ".join("" if v is None else str(v) for v in row) + " |" for row in r["rows"][:20]]
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ERP data-quality checks")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--out", default=str(ROOT / "reports" / "dq_report.md"))
    args = parser.parse_args()

    results = run_checks(build())
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(to_markdown(results), encoding="utf-8")

    for r in results:
        print(f"{r['severity']:<8} {len(r['rows']):>3}  {r['name']}")
    print(f"Report written to {args.out}")

    failed = any(r["rows"] and r["severity"] == "error" for r in results)
    return 1 if (args.strict and failed) else 0


if __name__ == "__main__":
    sys.exit(main())
