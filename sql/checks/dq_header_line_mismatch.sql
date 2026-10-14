-- severity: error
-- description: A/R invoices whose header net total differs from the sum of their lines
SELECT
    i.DocNum,
    i.CardCode,
    ROUND(i.DocTotal - i.VatSum, 2) AS HeaderNet,
    ROUND(SUM(l.LineTotal), 2)      AS LinesNet,
    ROUND(i.DocTotal - i.VatSum - SUM(l.LineTotal), 2) AS Difference
FROM OINV i
JOIN INV1 l ON l.DocEntry = i.DocEntry
GROUP BY i.DocEntry, i.DocNum, i.CardCode, i.DocTotal, i.VatSum
HAVING ABS(i.DocTotal - i.VatSum - SUM(l.LineTotal)) > 0.01;
