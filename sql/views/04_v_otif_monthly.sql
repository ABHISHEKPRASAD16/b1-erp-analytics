-- OTIF (on time, in full) per month of the due date.
-- A line counts as OTIF when it was delivered completely on or before its due date.
-- Only lines already due are measured.
CREATE VIEW v_otif_monthly AS
SELECT
    strftime('%Y-%m', f.DueDate) AS DueMonth,
    COUNT(*) AS LinesDue,
    SUM(CASE WHEN f.DeliveredQty >= f.OrderedQty AND f.DeliveryDate <= f.DueDate THEN 1 ELSE 0 END) AS LinesOTIF,
    ROUND(100.0 * AVG(CASE WHEN f.DeliveredQty >= f.OrderedQty AND f.DeliveryDate <= f.DueDate
                           THEN 1.0 ELSE 0.0 END), 1) AS OTIFPct
FROM v_o2c_flow f
CROSS JOIN REF_DATE rd
WHERE f.DueDate <= rd.RefDate
GROUP BY strftime('%Y-%m', f.DueDate);
