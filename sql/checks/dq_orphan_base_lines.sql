-- severity: error
-- description: Document lines that point to a source line that does not exist
SELECT 'DLN1' AS LineTable, l.DocEntry, l.LineNum, l.BaseType, l.BaseEntry, l.BaseLine
FROM DLN1 l
LEFT JOIN RDR1 s ON s.DocEntry = l.BaseEntry AND s.LineNum = l.BaseLine
WHERE l.BaseType = 17 AND s.DocEntry IS NULL
UNION ALL
SELECT 'INV1', l.DocEntry, l.LineNum, l.BaseType, l.BaseEntry, l.BaseLine
FROM INV1 l
LEFT JOIN DLN1 s ON s.DocEntry = l.BaseEntry AND s.LineNum = l.BaseLine
WHERE l.BaseType = 15 AND s.DocEntry IS NULL
UNION ALL
SELECT 'PDN1', l.DocEntry, l.LineNum, l.BaseType, l.BaseEntry, l.BaseLine
FROM PDN1 l
LEFT JOIN POR1 s ON s.DocEntry = l.BaseEntry AND s.LineNum = l.BaseLine
WHERE l.BaseType = 22 AND s.DocEntry IS NULL
UNION ALL
SELECT 'PCH1', l.DocEntry, l.LineNum, l.BaseType, l.BaseEntry, l.BaseLine
FROM PCH1 l
LEFT JOIN PDN1 s ON s.DocEntry = l.BaseEntry AND s.LineNum = l.BaseLine
WHERE l.BaseType = 20 AND s.DocEntry IS NULL;
