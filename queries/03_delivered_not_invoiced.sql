-- Deliveries that have not been invoiced yet: revenue that is shipped but not billed.
SELECT d.DocNum, d.CardCode, d.DocDate, ROUND(d.DocTotal - d.VatSum, 2) AS NetValue
FROM ODLN d
WHERE d.CANCELED = 'N'
  AND NOT EXISTS (
      SELECT 1 FROM INV1 il WHERE il.BaseType = 15 AND il.BaseEntry = d.DocEntry
  )
ORDER BY d.DocDate;
