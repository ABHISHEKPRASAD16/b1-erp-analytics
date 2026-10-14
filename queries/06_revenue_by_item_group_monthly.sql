-- Monthly net revenue per item group, with each group's share of the month.
WITH monthly AS (
    SELECT
        strftime('%Y-%m', i.DocDate) AS InvoiceMonth,
        m.ItmsGrpNam,
        SUM(l.LineTotal) AS NetRevenue
    FROM OINV i
    JOIN INV1 l ON l.DocEntry = i.DocEntry
    JOIN OITM m ON m.ItemCode = l.ItemCode
    WHERE i.CANCELED = 'N'
    GROUP BY strftime('%Y-%m', i.DocDate), m.ItmsGrpNam
)
SELECT
    InvoiceMonth,
    ItmsGrpNam,
    ROUND(NetRevenue, 2) AS NetRevenue,
    ROUND(100.0 * NetRevenue / SUM(NetRevenue) OVER (PARTITION BY InvoiceMonth), 1) AS SharePct
FROM monthly
ORDER BY InvoiceMonth, NetRevenue DESC;
