-- Items whose usable stock (excluding the quarantine warehouse 03) is below the minimum level.
CREATE VIEW v_stock_below_min AS
SELECT
    m.ItemCode,
    m.ItemName,
    m.MinLevel,
    SUM(w.OnHand)     AS OnHand,
    SUM(w.IsCommited) AS Committed,
    SUM(w.OnOrder)    AS OnOrder,
    SUM(w.OnHand) - SUM(w.IsCommited) + SUM(w.OnOrder) AS Available,
    m.MinLevel - (SUM(w.OnHand) - SUM(w.IsCommited) + SUM(w.OnOrder)) AS Shortfall
FROM OITM m
JOIN OITW w ON w.ItemCode = m.ItemCode AND w.WhsCode <> '03'
GROUP BY m.ItemCode, m.ItemName, m.MinLevel
HAVING SUM(w.OnHand) - SUM(w.IsCommited) + SUM(w.OnOrder) < m.MinLevel;
