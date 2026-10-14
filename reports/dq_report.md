# Data quality report

| Check | Severity | Rows found | What it looks for |
|---|---|---:|---|
| `dq_duplicate_business_partners` | error | 2 | Customers that exist more than once with the same VAT number |
| `dq_frozen_partner_documents` | error | 2 | Sales orders posted to a customer after the customer was blocked |
| `dq_header_line_mismatch` | error | 2 | A/R invoices whose header net total differs from the sum of their lines |
| `dq_invoices_without_base` | warning | 5 | A/R invoices posted without a delivery (allowed in B1, but worth reviewing) |
| `dq_negative_stock` | error | 1 | Items with negative on-hand stock in a warehouse |
| `dq_orphan_base_lines` | error | 3 | Document lines that point to a source line that does not exist |

## dq_duplicate_business_partners

Customers that exist more than once with the same VAT number

| LicTradNum | Records | CardCodes | Names |
|---|---|---|---|
| DE740389325 | 2 | C10019, C10042 | Nord Antriebstechnik SE | NORD ANTRIEBSTECHNIK SE |
| DE883543540 | 2 | C10007, C10041 | Weser Anlagenbau GmbH | WESER ANLAGENBAU GMBH |

## dq_frozen_partner_documents

Sales orders posted to a customer after the customer was blocked

| DocNum | CardCode | CardName | DocDate | frozenFrom |
|---|---|---|---|---|
| 100301 | C10040 | Alpen Elektronik AG | 2026-08-04 | 2026-07-01 |
| 100302 | C10040 | Alpen Elektronik AG | 2026-09-17 | 2026-07-01 |

## dq_header_line_mismatch

A/R invoices whose header net total differs from the sum of their lines

| DocNum | CardCode | HeaderNet | LinesNet | Difference |
|---|---|---|---|---|
| 300011 | C10016 | 49637.2 | 49537.2 | 100.0 |
| 300046 | C10018 | 36956.41 | 36856.41 | 100.0 |

## dq_invoices_without_base

A/R invoices posted without a delivery (allowed in B1, but worth reviewing)

| DocNum | CardCode | DocDate | DocTotal |
|---|---|---|---|
| 300253 | C10017 | 2026-03-02 | 2985.47 |
| 300254 | C10025 | 2026-02-25 | 6647.34 |
| 300255 | C10019 | 2026-04-08 | 203.59 |
| 300256 | C10034 | 2026-03-09 | 3298.68 |
| 300257 | C10023 | 2026-02-12 | 361.52 |

## dq_negative_stock

Items with negative on-hand stock in a warehouse

| ItemCode | ItemName | WhsCode | OnHand |
|---|---|---|---|
| I00013 | Engine Mount Assembly | 02 | -12.0 |

## dq_orphan_base_lines

Document lines that point to a source line that does not exist

| LineTable | DocEntry | LineNum | BaseType | BaseEntry | BaseLine |
|---|---|---|---|---|---|
| DLN1 | 259 | 0 | 17 | 99999 | 0 |
| DLN1 | 259 | 1 | 17 | 99999 | 1 |
| DLN1 | 259 | 2 | 17 | 99999 | 2 |
