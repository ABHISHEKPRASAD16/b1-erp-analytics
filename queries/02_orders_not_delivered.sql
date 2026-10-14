-- Sales orders that are past their due date and have no delivery at all.
SELECT o.DocNum, o.CardCode, c.CardName, o.DocDueDate, o.DocTotal
FROM ORDR o
JOIN OCRD c ON c.CardCode = o.CardCode
CROSS JOIN REF_DATE rd
WHERE o.CANCELED = 'N'
  AND o.DocDueDate < rd.RefDate
  AND NOT EXISTS (
      SELECT 1
      FROM RDR1 r
      JOIN DLN1 dl ON dl.BaseType = 17 AND dl.BaseEntry = r.DocEntry AND dl.BaseLine = r.LineNum
      WHERE r.DocEntry = o.DocEntry
  )
ORDER BY o.DocDueDate;
