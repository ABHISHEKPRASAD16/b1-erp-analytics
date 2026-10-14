"""Generate synthetic ERP data in the SAP Business One table layout.

The data is seeded, so every run produces the same database. A small number of
data-quality problems are injected on purpose, so the checks in sql/checks/
have something real to find. INJECTED documents exactly what was planted.
"""

from __future__ import annotations

import random
from collections import defaultdict
from datetime import date, timedelta

SEED = 42
REF_DATE = date(2026, 10, 15)
VAT_RATE = 0.19

# B1 object types used in BaseType
OBJ_ORDER, OBJ_DELIVERY, OBJ_AR_INVOICE = 17, 15, 13
OBJ_PO, OBJ_GRPO, OBJ_AP_INVOICE = 22, 20, 18
NO_BASE = -1

SLOW_MOVERS = {"I00024", "I00025"}
SLOW_MOVERS_UNTIL = date(2026, 6, 30)

# What the generator plants, and how many rows each check should return.
INJECTED = {
    "dq_duplicate_business_partners": 2,   # 2 customers created twice with the same VAT number
    "dq_orphan_base_lines": 3,             # 3 delivery lines pointing to a sales order that doesn't exist
    "dq_header_line_mismatch": 2,          # 2 A/R invoices whose header total doesn't match the lines
    "dq_negative_stock": 1,                # 1 item/warehouse with negative on-hand stock
    "dq_frozen_partner_documents": 2,      # 2 sales orders posted to a blocked customer
    "dq_invoices_without_base": 5,         # 5 A/R invoices created without a delivery (warning)
}

CITIES = [("DE", "Düsseldorf"), ("DE", "Köln"), ("DE", "Hilden"), ("DE", "Essen"), ("DE", "Dortmund"),
          ("DE", "Stuttgart"), ("DE", "München"), ("NL", "Eindhoven"), ("FR", "Lyon"), ("PL", "Wrocław")]
NAME_A = ["Rhein", "Ruhr", "Nord", "Süd", "Alpen", "Weser", "Main", "Elbe", "Hansa", "Mosel"]
NAME_B = ["Fahrzeugtechnik", "Maschinenbau", "Antriebstechnik", "Klebetechnik", "Anlagenbau",
          "Präzisionsteile", "Industriebau", "Elektronik"]
NAME_C = ["GmbH", "AG", "GmbH & Co. KG", "SE"]

ITEMS = [
    ("Adhesives", "2K Epoxy Adhesive 50 ml", "EA", 18.40),
    ("Adhesives", "2K Epoxy Adhesive 400 ml", "EA", 61.00),
    ("Adhesives", "Structural Acrylic 400 ml", "EA", 54.20),
    ("Adhesives", "Polyurethane Adhesive 600 ml", "EA", 39.90),
    ("Adhesives", "Rubber-to-Metal Bonding Agent 1 L", "L", 72.50),
    ("Adhesives", "Rubber-to-Metal Bonding Agent 5 L", "L", 330.00),
    ("Coatings", "Primer Coat 1 L", "L", 28.30),
    ("Coatings", "Primer Coat 20 L", "L", 495.00),
    ("Coatings", "Protective Topcoat 1 L", "L", 33.10),
    ("Coatings", "Anti-Friction Coating 5 L", "L", 210.00),
    ("Vibration Control", "Elastomer Mount M8", "EA", 6.20),
    ("Vibration Control", "Elastomer Mount M10", "EA", 7.80),
    ("Vibration Control", "Engine Mount Assembly", "EA", 44.00),
    ("Vibration Control", "Cab Mount Kit", "EA", 118.00),
    ("Vibration Control", "Isolator Pad 100x100", "EA", 9.40),
    ("Thermal", "Thermal Gap Pad 1 mm", "EA", 3.10),
    ("Thermal", "Thermal Gap Pad 2 mm", "EA", 3.90),
    ("Thermal", "Thermal Gap Filler 50 ml", "EA", 24.50),
    ("Thermal", "Thermal Grease 1 kg", "KG", 96.00),
    ("Thermal", "Potting Compound 2 kg", "KG", 128.00),
    ("Packaging", "Dispensing Gun 400 ml", "EA", 22.00),
    ("Packaging", "Static Mixer Nozzle (50 pcs)", "EA", 31.00),
    ("Packaging", "Cartridge Holder", "EA", 11.50),
    ("Packaging", "Pail Lid 20 L", "EA", 4.20),
    ("Packaging", "Drum Pump", "EA", 145.00),
]

WAREHOUSES = [("01", "Main Warehouse"), ("02", "Production"), ("03", "Quarantine")]


def _d(x: date) -> str:
    return x.isoformat()


def generate() -> dict[str, list[dict]]:
    rnd = random.Random(SEED)
    t: dict[str, list[dict]] = defaultdict(list)
    t["REF_DATE"].append({"RefDate": _d(REF_DATE)})

    # ---------- Business partners ----------
    customers = []
    for i in range(1, 41):
        country, city = rnd.choice(CITIES)
        code = f"C{10000 + i}"
        t["OCRD"].append({
            "CardCode": code,
            "CardName": f"{rnd.choice(NAME_A)} {rnd.choice(NAME_B)} {rnd.choice(NAME_C)}",
            "CardType": "C", "LicTradNum": f"{country}{rnd.randint(100000000, 999999999)}",
            "Country": country, "City": city, "frozenFor": "N", "frozenFrom": None,
            "CreateDate": _d(date(2024, 1, 1) + timedelta(days=rnd.randint(0, 600))),
        })
        customers.append(code)

    # C10040 is blocked from 1 July 2026; it is excluded from normal order generation.
    blocked = "C10040"
    for bp in t["OCRD"]:
        if bp["CardCode"] == blocked:
            bp["frozenFor"], bp["frozenFrom"] = "Y", "2026-07-01"
    customers.remove(blocked)

    # Injected: two customers created a second time under a new code, same VAT number.
    for new_code, original in (("C10041", "C10007"), ("C10042", "C10019")):
        src = next(bp for bp in t["OCRD"] if bp["CardCode"] == original)
        t["OCRD"].append({**src, "CardCode": new_code, "CardName": src["CardName"].upper(),
                          "CreateDate": "2026-03-12"})
        customers.append(new_code)

    suppliers = []
    for i in range(1, 11):
        country, city = rnd.choice(CITIES)
        code = f"S{20000 + i}"
        t["OCRD"].append({
            "CardCode": code, "CardName": f"{rnd.choice(NAME_A)} Rohstoffe {rnd.choice(NAME_C)}",
            "CardType": "S", "LicTradNum": f"{country}{rnd.randint(100000000, 999999999)}",
            "Country": country, "City": city, "frozenFor": "N", "frozenFrom": None,
            "CreateDate": _d(date(2023, 6, 1) + timedelta(days=rnd.randint(0, 400))),
        })
        suppliers.append(code)

    # ---------- Items and warehouses ----------
    items = {}
    for i, (group, name, uom, cost) in enumerate(ITEMS, start=1):
        code = f"I{i:05d}"
        items[code] = cost
        t["OITM"].append({"ItemCode": code, "ItemName": name, "ItmsGrpNam": group, "InvntryUom": uom,
                          "MinLevel": float(rnd.choice([50, 100, 150, 200, 300])), "AvgPrice": cost})
    for whs, name in WAREHOUSES:
        t["OWHS"].append({"WhsCode": whs, "WhsName": name})

    # ---------- Sales: order -> delivery -> A/R invoice ----------
    entries = defaultdict(int)

    def new_doc(table: str, card: str, doc_date: date, due: date, base_num: int) -> dict:
        entries[table] += 1
        doc = {"DocEntry": entries[table], "DocNum": base_num + entries[table], "CardCode": card,
               "DocDate": _d(doc_date), "DocDueDate": _d(due), "DocStatus": "O", "CANCELED": "N",
               "VatSum": 0.0, "DocTotal": 0.0, "DocCur": "EUR"}
        t[table].append(doc)
        return doc

    def add_line(table: str, doc: dict, line_num: int, item: str, qty: float, price: float,
                 base_type: int = NO_BASE, base_entry=None, base_line=None, whs: str = "01") -> dict:
        line = {"DocEntry": doc["DocEntry"], "LineNum": line_num, "ItemCode": item, "Quantity": qty,
                "OpenQty": qty, "Price": price, "LineTotal": round(qty * price, 2), "WhsCode": whs,
                "LineStatus": "O", "BaseType": base_type, "BaseEntry": base_entry, "BaseLine": base_line}
        t[table].append(line)
        return line

    def close_totals(doc: dict, lines: list[dict]) -> None:
        net = round(sum(l["LineTotal"] for l in lines), 2)
        doc["VatSum"] = round(net * VAT_RATE, 2)
        doc["DocTotal"] = round(net + doc["VatSum"], 2)

    start = date(2026, 1, 5)
    span = (date(2026, 10, 10) - start).days

    def sales_order(card: str, order_date: date) -> tuple[dict, list[dict]]:
        due = order_date + timedelta(days=rnd.randint(7, 21))
        order = new_doc("ORDR", card, order_date, due, 100000)
        lines = []
        # Two packaging items stop selling after June, so the slow-mover query has results.
        pool = [i for i in items if order_date <= SLOW_MOVERS_UNTIL or i not in SLOW_MOVERS]
        for n, item in enumerate(rnd.sample(pool, rnd.randint(1, 4))):
            price = round(items[item] * rnd.uniform(1.25, 1.6), 2)
            lines.append(add_line("RDR1", order, n, item, float(rnd.randint(5, 200)), price))
        close_totals(order, lines)
        return order, lines

    deliveries: list[tuple[dict, list[dict]]] = []
    # B1 numbers documents as they are created, so generate orders in date order.
    for order_date in sorted(start + timedelta(days=rnd.randint(0, span)) for _ in range(300)):
        order, lines = sales_order(rnd.choice(customers), order_date)
        due = date.fromisoformat(order["DocDueDate"])

        if rnd.random() < 0.03:  # cancelled order
            order["CANCELED"], order["DocStatus"] = "Y", "C"
            for l in lines:
                l["OpenQty"], l["LineStatus"] = 0.0, "C"
            continue

        outcome = rnd.random()
        if outcome < 0.10:
            continue  # not delivered yet, stays open
        partial = outcome < 0.20
        deliv_date = max(order_date + timedelta(days=2), due + timedelta(days=rnd.randint(-8, 4)))
        if deliv_date > REF_DATE:
            continue

        delivery = new_doc("ODLN", order["CardCode"], deliv_date, deliv_date, 200000)
        dlines = []
        for l in lines:
            qty = float(max(1, int(l["Quantity"] * rnd.uniform(0.4, 0.8)))) if partial else l["Quantity"]
            dlines.append(add_line("DLN1", delivery, len(dlines), l["ItemCode"], qty, l["Price"],
                                   OBJ_ORDER, l["DocEntry"], l["LineNum"]))
            l["OpenQty"] = l["Quantity"] - qty
            l["LineStatus"] = "C" if l["OpenQty"] == 0 else "O"
        close_totals(delivery, dlines)
        if all(l["OpenQty"] == 0 for l in lines):
            order["DocStatus"] = "C"
        deliveries.append((delivery, dlines))

    # Injected: two orders for the blocked customer after it was blocked.
    for d in (date(2026, 8, 4), date(2026, 9, 17)):
        sales_order(blocked, d)

    # Injected: one delivery whose three lines point to sales order 99999, which doesn't exist.
    orphan = new_doc("ODLN", customers[0], date(2026, 9, 2), date(2026, 9, 2), 200000)
    olines = [add_line("DLN1", orphan, n, item, 10.0, round(items[item] * 1.4, 2), OBJ_ORDER, 99999, n)
              for n, item in enumerate(["I00003", "I00011", "I00017"])]
    close_totals(orphan, olines)

    # A/R invoices from deliveries
    for delivery, dlines in deliveries:
        ddate = date.fromisoformat(delivery["DocDate"])
        if ddate > REF_DATE - timedelta(days=2) or rnd.random() < 0.05:
            continue
        inv_date = min(REF_DATE, ddate + timedelta(days=rnd.randint(0, 3)))
        invoice = new_doc("OINV", delivery["CardCode"], inv_date, inv_date + timedelta(days=30), 300000)
        ilines = [add_line("INV1", invoice, n, l["ItemCode"], l["Quantity"], l["Price"],
                           OBJ_DELIVERY, l["DocEntry"], l["LineNum"]) for n, l in enumerate(dlines)]
        for l in dlines:
            l["OpenQty"], l["LineStatus"] = 0.0, "C"
        delivery["DocStatus"] = "C"
        close_totals(invoice, ilines)

    # Injected: five invoices posted directly, without a delivery.
    for _ in range(5):
        inv_date = start + timedelta(days=rnd.randint(30, span))
        invoice = new_doc("OINV", rnd.choice(customers), inv_date, inv_date + timedelta(days=30), 300000)
        item = rnd.choice(list(items))
        ilines = [add_line("INV1", invoice, 0, item, float(rnd.randint(5, 40)), round(items[item] * 1.4, 2))]
        close_totals(invoice, ilines)

    # Injected: two invoice headers changed after posting, so they no longer match their lines.
    for inv in (t["OINV"][10], t["OINV"][45]):
        inv["DocTotal"] = round(inv["DocTotal"] + 100.0, 2)

    # ---------- Purchasing: PO -> goods receipt PO -> A/P invoice ----------
    for po_date in sorted(start + timedelta(days=rnd.randint(0, span)) for _ in range(80)):
        due = po_date + timedelta(days=rnd.randint(10, 30))
        po = new_doc("OPOR", rnd.choice(suppliers), po_date, due, 400000)
        plines = [add_line("POR1", po, n, item, float(rnd.randint(50, 500)), items[item])
                  for n, item in enumerate(rnd.sample(list(items), rnd.randint(1, 3)))]
        close_totals(po, plines)

        gr_date = due + timedelta(days=rnd.randint(-5, 8))
        if rnd.random() < 0.15 or gr_date > REF_DATE:
            continue
        grpo = new_doc("OPDN", po["CardCode"], gr_date, gr_date, 500000)
        glines = [add_line("PDN1", grpo, n, l["ItemCode"], l["Quantity"], l["Price"],
                           OBJ_PO, l["DocEntry"], l["LineNum"]) for n, l in enumerate(plines)]
        for l in plines:
            l["OpenQty"], l["LineStatus"] = 0.0, "C"
        po["DocStatus"] = "C"
        close_totals(grpo, glines)

        if rnd.random() < 0.10:
            continue
        ap_date = min(REF_DATE, gr_date + timedelta(days=rnd.randint(1, 10)))
        ap = new_doc("OPCH", po["CardCode"], ap_date, ap_date + timedelta(days=45), 600000)
        alines = [add_line("PCH1", ap, n, l["ItemCode"], l["Quantity"], l["Price"],
                           OBJ_GRPO, l["DocEntry"], l["LineNum"]) for n, l in enumerate(glines)]
        for l in glines:
            l["OpenQty"], l["LineStatus"] = 0.0, "C"
        grpo["DocStatus"] = "C"
        close_totals(ap, alines)

    # ---------- Stock ----------
    committed = defaultdict(float)
    for l in t["RDR1"]:
        committed[l["ItemCode"]] += l["OpenQty"]
    on_order = defaultdict(float)
    for l in t["POR1"]:
        on_order[l["ItemCode"]] += l["OpenQty"]

    for item in items:
        for whs, _ in WAREHOUSES:
            on_hand = float(rnd.randint(0, 40)) if whs == "03" else float(rnd.randint(0, 350))
            t["OITW"].append({"ItemCode": item, "WhsCode": whs, "OnHand": on_hand,
                              "IsCommited": committed[item] if whs == "01" else 0.0,
                              "OnOrder": on_order[item] if whs == "01" else 0.0})
    # Injected: negative stock (an issue posted before the receipt).
    next(r for r in t["OITW"] if r["ItemCode"] == "I00013" and r["WhsCode"] == "02")["OnHand"] = -12.0

    return dict(t)
