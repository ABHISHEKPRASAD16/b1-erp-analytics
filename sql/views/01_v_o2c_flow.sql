-- Order-to-cash document flow, one row per sales order line.
-- Follows each line forward: order line -> delivery line -> invoice line,
-- using the B1 link fields BaseType / BaseEntry / BaseLine.
CREATE VIEW v_o2c_flow AS
SELECT
    o.DocNum        AS OrderNum,
    o.CardCode,
    c.CardName,
    o.DocDate       AS OrderDate,
    o.DocDueDate    AS DueDate,
    r.LineNum,
    r.ItemCode,
    r.Quantity      AS OrderedQty,
    r.OpenQty,
    r.Price,
    d.DocNum        AS DeliveryNum,
    d.DocDate       AS DeliveryDate,
    COALESCE(dl.Quantity, 0) AS DeliveredQty,
    i.DocNum        AS InvoiceNum,
    i.DocDate       AS InvoiceDate,
    il.LineTotal    AS InvoicedNet
FROM ORDR o
JOIN RDR1 r  ON r.DocEntry = o.DocEntry
JOIN OCRD c  ON c.CardCode = o.CardCode
LEFT JOIN DLN1 dl ON dl.BaseType = 17 AND dl.BaseEntry = r.DocEntry AND dl.BaseLine = r.LineNum
LEFT JOIN ODLN d  ON d.DocEntry = dl.DocEntry
LEFT JOIN INV1 il ON il.BaseType = 15 AND il.BaseEntry = dl.DocEntry AND il.BaseLine = dl.LineNum
LEFT JOIN OINV i  ON i.DocEntry = il.DocEntry
WHERE o.CANCELED = 'N';
