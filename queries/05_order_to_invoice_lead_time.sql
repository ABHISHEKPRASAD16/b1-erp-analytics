-- Average days from order to delivery and from delivery to invoice, per month.
-- T-SQL: DATEDIFF(day, OrderDate, DeliveryDate) instead of julianday() differences.
SELECT
    strftime('%Y-%m', OrderDate) AS OrderMonth,
    COUNT(*) AS Lines,
    ROUND(AVG(julianday(DeliveryDate) - julianday(OrderDate)), 1)  AS AvgDaysToDeliver,
    ROUND(AVG(julianday(InvoiceDate) - julianday(DeliveryDate)), 1) AS AvgDaysToInvoice
FROM v_o2c_flow
WHERE InvoiceDate IS NOT NULL
GROUP BY strftime('%Y-%m', OrderDate)
ORDER BY OrderMonth;
