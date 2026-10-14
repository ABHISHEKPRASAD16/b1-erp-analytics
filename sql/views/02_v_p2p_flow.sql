-- Procure-to-pay document flow, one row per purchase order line:
-- PO line -> goods receipt PO line -> A/P invoice line.
CREATE VIEW v_p2p_flow AS
SELECT
    p.DocNum        AS PONum,
    p.CardCode,
    s.CardName      AS SupplierName,
    p.DocDate       AS PODate,
    p.DocDueDate    AS DueDate,
    pl.LineNum,
    pl.ItemCode,
    pl.Quantity     AS OrderedQty,
    pl.LineTotal    AS OrderedValue,
    g.DocNum        AS GoodsReceiptNum,
    g.DocDate       AS ReceiptDate,
    a.DocNum        AS APInvoiceNum,
    a.DocDate       AS APInvoiceDate,
    al.LineTotal    AS InvoicedNet
FROM OPOR p
JOIN POR1 pl ON pl.DocEntry = p.DocEntry
JOIN OCRD s  ON s.CardCode = p.CardCode
LEFT JOIN PDN1 gl ON gl.BaseType = 22 AND gl.BaseEntry = pl.DocEntry AND gl.BaseLine = pl.LineNum
LEFT JOIN OPDN g  ON g.DocEntry = gl.DocEntry
LEFT JOIN PCH1 al ON al.BaseType = 20 AND al.BaseEntry = gl.DocEntry AND al.BaseLine = gl.LineNum
LEFT JOIN OPCH a  ON a.DocEntry = al.DocEntry
WHERE p.CANCELED = 'N';
