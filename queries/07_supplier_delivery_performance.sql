-- Supplier delivery performance: share of PO lines received on or before the due date.
SELECT
    CardCode,
    SupplierName,
    COUNT(*) AS POLines,
    SUM(CASE WHEN ReceiptDate IS NOT NULL THEN 1 ELSE 0 END) AS Received,
    ROUND(100.0 * AVG(CASE WHEN ReceiptDate <= DueDate THEN 1.0 ELSE 0.0 END), 1) AS OnTimePct
FROM v_p2p_flow
GROUP BY CardCode, SupplierName
ORDER BY OnTimePct;
