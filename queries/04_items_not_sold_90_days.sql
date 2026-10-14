-- Items with no sales order in the last 90 days (slow movers).
SELECT m.ItemCode, m.ItemName, m.ItmsGrpNam, MAX(o.DocDate) AS LastOrderDate
FROM OITM m
LEFT JOIN RDR1 r ON r.ItemCode = m.ItemCode
LEFT JOIN ORDR o ON o.DocEntry = r.DocEntry AND o.CANCELED = 'N'
CROSS JOIN REF_DATE rd
GROUP BY m.ItemCode, m.ItemName, m.ItmsGrpNam, rd.RefDate
HAVING MAX(o.DocDate) IS NULL OR MAX(o.DocDate) < date(rd.RefDate, '-90 days')
ORDER BY LastOrderDate;
