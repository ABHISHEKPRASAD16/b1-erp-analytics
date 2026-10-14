"""Tests: the data is consistent, the views make sense, and each check finds what was planted."""

import pytest

from erp.build import build
from erp.generate_data import INJECTED
from run_checks import run_checks


@pytest.fixture(scope="module")
def conn():
    return build()


@pytest.fixture(scope="module")
def results(conn):
    return {r["name"]: r for r in run_checks(conn)}


def scalar(conn, sql):
    return conn.execute(sql).fetchone()[0]


@pytest.mark.parametrize("check, expected", sorted(INJECTED.items()))
def test_each_check_finds_exactly_what_was_planted(results, check, expected):
    assert len(results[check]["rows"]) == expected


def test_every_check_is_covered(results):
    assert set(results) == set(INJECTED)


def test_open_quantity_never_exceeds_ordered(conn):
    assert scalar(conn, "SELECT COUNT(*) FROM RDR1 WHERE OpenQty < 0 OR OpenQty > Quantity") == 0


def test_delivered_plus_open_equals_ordered(conn):
    sql = """
        SELECT COUNT(*) FROM v_o2c_flow
        WHERE ABS(DeliveredQty + OpenQty - OrderedQty) > 0.001
    """
    assert scalar(conn, sql) == 0


def test_closed_orders_have_no_open_lines(conn):
    sql = """
        SELECT COUNT(*) FROM ORDR o JOIN RDR1 r ON r.DocEntry = o.DocEntry
        WHERE o.DocStatus = 'C' AND o.CANCELED = 'N' AND r.OpenQty > 0
    """
    assert scalar(conn, sql) == 0


def test_invoice_never_dated_before_its_delivery(conn):
    assert scalar(conn, "SELECT COUNT(*) FROM v_o2c_flow WHERE InvoiceDate < DeliveryDate") == 0


def test_document_numbers_follow_dates(conn):
    sql = """
        SELECT COUNT(*) FROM ORDR a JOIN ORDR b ON b.DocNum = a.DocNum + 1
        WHERE b.DocDate < a.DocDate AND b.CardCode <> 'C10040'
    """
    assert scalar(conn, sql) == 0


def test_otif_is_a_percentage(conn):
    for row in conn.execute("SELECT OTIFPct FROM v_otif_monthly"):
        assert 0 <= row[0] <= 100


def test_revenue_ranking_starts_at_one(conn):
    assert scalar(conn, "SELECT MIN(RevenueRank) FROM v_revenue_by_customer") == 1
