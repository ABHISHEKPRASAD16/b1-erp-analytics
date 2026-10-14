-- severity: error
-- description: Items with negative on-hand stock in a warehouse
SELECT w.ItemCode, m.ItemName, w.WhsCode, w.OnHand
FROM OITW w
JOIN OITM m ON m.ItemCode = w.ItemCode
WHERE w.OnHand < 0;
