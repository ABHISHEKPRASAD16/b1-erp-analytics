"""Build the SQLite database: schema, synthetic data, then the analysis views."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from erp.generate_data import generate

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "erp" / "schema.sql"
VIEWS_DIR = ROOT / "sql" / "views"
CHECKS_DIR = ROOT / "sql" / "checks"


def build(db_path: str | Path = ":memory:") -> sqlite3.Connection:
    if db_path != ":memory:":
        Path(db_path).unlink(missing_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))

    for table, rows in generate().items():
        if not rows:
            continue
        cols = list(rows[0])
        conn.executemany(
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
            [tuple(r[c] for c in cols) for r in rows],
        )

    for view in sorted(VIEWS_DIR.glob("*.sql")):
        conn.executescript(view.read_text(encoding="utf-8"))
    conn.commit()
    return conn


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="erp.db", help="output SQLite file (default: erp.db)")
    args = parser.parse_args()
    conn = build(args.db)
    for table in ("OCRD", "OITM", "ORDR", "RDR1", "ODLN", "OINV", "OPOR", "OPDN", "OPCH"):
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:<5} {n:>5} rows")
    print(f"Database written to {args.db}")


if __name__ == "__main__":
    main()
