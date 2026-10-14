-- severity: error
-- description: Sales orders posted to a customer after the customer was blocked
SELECT o.DocNum, o.CardCode, c.CardName, o.DocDate, c.frozenFrom
FROM ORDR o
JOIN OCRD c ON c.CardCode = o.CardCode
WHERE c.frozenFor = 'Y' AND o.DocDate >= c.frozenFrom;
