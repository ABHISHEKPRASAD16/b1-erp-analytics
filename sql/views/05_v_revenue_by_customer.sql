-- Net invoiced revenue per customer, ranked.
CREATE VIEW v_revenue_by_customer AS
SELECT
    c.CardCode,
    c.CardName,
    COUNT(*) AS Invoices,
    ROUND(SUM(i.DocTotal - i.VatSum), 2) AS NetRevenue,
    RANK() OVER (ORDER BY SUM(i.DocTotal - i.VatSum) DESC) AS RevenueRank
FROM OINV i
JOIN OCRD c ON c.CardCode = i.CardCode
WHERE i.CANCELED = 'N'
GROUP BY c.CardCode, c.CardName;
