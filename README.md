# B1 ERP Analytics

SQL analytics and data-quality checks on an ERP database modelled on the **SAP Business One** table structure: order to cash, procure to pay, stock, and the problems that show up in real ERP data.

Everything runs locally on SQLite with synthetic, seeded data. No SAP licence or installation needed.

> This is a personal learning and portfolio project. The data is generated, not taken from any company. Table and column names follow public SAP Business One conventions; the project is not affiliated with SAP.

## What it covers

**Document flow.** Sales orders → deliveries → A/R invoices, and purchase orders → goods receipts → A/P invoices, linked line by line through `BaseType` / `BaseEntry` / `BaseLine`, the way B1 links documents.

**Analysis views** (`sql/views/`)

| View | Answers |
|---|---|
| `v_o2c_flow` | Where is each sales order line: delivered, invoiced, or still open? |
| `v_p2p_flow` | Same for purchase order lines |
| `v_open_sales_orders` | Backlog with open value and days overdue |
| `v_otif_monthly` | On-time-in-full delivery rate per month |
| `v_revenue_by_customer` | Net revenue per customer, ranked |
| `v_stock_below_min` | Items below minimum stock, counting committed and incoming quantities |

**Data-quality checks** (`sql/checks/`). The generator plants known problems, and each check has to find exactly those:

| Check | Severity | Finds |
|---|---|---|
| `dq_duplicate_business_partners` | error | Customers created twice with the same VAT number |
| `dq_orphan_base_lines` | error | Document lines pointing to a source line that doesn't exist |
| `dq_header_line_mismatch` | error | Invoices whose header total doesn't match their lines |
| `dq_negative_stock` | error | Negative on-hand stock |
| `dq_frozen_partner_documents` | error | Orders posted to a blocked customer |
| `dq_invoices_without_base` | warning | Invoices posted without a delivery |

**Business queries** (`queries/`): top customers, overdue orders with no delivery, shipped-but-not-billed, slow movers, order-to-invoice lead time, revenue mix by item group, supplier on-time rate. Each notes the T-SQL equivalent where the syntax differs.

## Run it

Python 3.10+ only; the database uses the built-in `sqlite3`.

```bash
pip install -r requirements.txt     # pytest, for the tests

python -m erp.build                 # build erp.db (open it in DBeaver or DB Browser for SQLite)
python run_checks.py                # run the checks, write reports/dq_report.md
python run_query.py queries/02_orders_not_delivered.sql
python run_query.py "SELECT * FROM v_otif_monthly"
pytest -q
```

CI runs the tests and the checks on every push and uploads the data-quality report.

## Project layout

```
erp/
  schema.sql          B1-style tables: OCRD, OITM, OWHS, OITW, ORDR/RDR1, ODLN/DLN1, OINV/INV1, OPOR/POR1, OPDN/PDN1, OPCH/PCH1
  generate_data.py    seeded synthetic data, with planted data-quality problems
  build.py            builds the database and creates the views
sql/views/            analysis layer
sql/checks/           data-quality checks (severity and description in the header comment)
queries/              business questions
run_checks.py         check runner and Markdown report
run_query.py          run any SQL file or statement
tests/                consistency tests and check expectations
docs/data_model.md    document flow, link fields, SQLite vs T-SQL
```

## Notes on the model

- `DocEntry` is the internal key used in joins; `DocNum` is the number users see.
- Stock "available" = on hand − committed to sales orders + on order from suppliers, excluding the quarantine warehouse.
- The analysis date is fixed in `REF_DATE` (15 Oct 2026) so every run gives the same numbers.

See [docs/data_model.md](docs/data_model.md) for the document flow diagram and the SQLite-to-T-SQL mapping.
