-- Top 10 customers by net invoiced revenue in the last 90 days.
-- T-SQL (SQL Server, as used by B1): SELECT TOP 10 ... WHERE i.DocDate >= DATEADD(day, -90, GETDATE())
SELECT
    i.CardCode,
    c.CardName,
    COUNT(*) AS Invoices,
    ROUND(SUM(i.DocTotal - i.VatSum), 2) AS NetRevenue
FROM OINV i
JOIN OCRD c ON c.CardCode = i.CardCode
CROSS JOIN REF_DATE rd
WHERE i.CANCELED = 'N'
  AND i.DocDate >= date(rd.RefDate, '-90 days')
GROUP BY i.CardCode, c.CardName
ORDER BY NetRevenue DESC
LIMIT 10;
