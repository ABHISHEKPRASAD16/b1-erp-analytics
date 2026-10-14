-- Sales order backlog: order lines still waiting for delivery, with days overdue.
CREATE VIEW v_open_sales_orders AS
SELECT
    o.DocNum      AS OrderNum,
    o.CardCode,
    c.CardName,
    o.DocDate     AS OrderDate,
    o.DocDueDate  AS DueDate,
    r.ItemCode,
    r.Quantity    AS OrderedQty,
    r.OpenQty,
    ROUND(r.OpenQty * r.Price, 2) AS OpenValue,
    CAST(julianday(rd.RefDate) - julianday(o.DocDueDate) AS INTEGER) AS DaysOverdue
FROM ORDR o
JOIN RDR1 r ON r.DocEntry = o.DocEntry
JOIN OCRD c ON c.CardCode = o.CardCode
CROSS JOIN REF_DATE rd
WHERE o.CANCELED = 'N'
  AND r.OpenQty > 0;
