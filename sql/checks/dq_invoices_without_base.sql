-- severity: warning
-- description: A/R invoices posted without a delivery (allowed in B1, but worth reviewing)
SELECT i.DocNum, i.CardCode, i.DocDate, i.DocTotal
FROM OINV i
WHERE NOT EXISTS (
    SELECT 1 FROM INV1 l WHERE l.DocEntry = i.DocEntry AND l.BaseType <> -1
);
