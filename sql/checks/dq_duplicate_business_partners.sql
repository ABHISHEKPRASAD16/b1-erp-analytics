-- severity: error
-- description: Customers that exist more than once with the same VAT number
SELECT
    LicTradNum,
    COUNT(*) AS Records,
    GROUP_CONCAT(CardCode, ', ') AS CardCodes,
    GROUP_CONCAT(CardName, ' | ') AS Names
FROM OCRD
WHERE CardType = 'C' AND LicTradNum IS NOT NULL
GROUP BY LicTradNum
HAVING COUNT(*) > 1;
