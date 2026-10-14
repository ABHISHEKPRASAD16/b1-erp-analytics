-- Schema modelled on the SAP Business One table layout.
-- Table and column names follow B1 naming (OCRD, ORDR/RDR1, ...),
-- reduced to the columns this project needs. Synthetic data only.
--
-- Header tables start with "O", line tables end with "1".
-- Documents are linked line-to-line through BaseType / BaseEntry / BaseLine:
--   BaseType = object type of the source document (17 = sales order, ...)
--   BaseEntry = DocEntry of the source document
--   BaseLine  = LineNum of the source line
--   BaseType = -1 means "created without a source document".

CREATE TABLE REF_DATE (RefDate TEXT NOT NULL);  -- "today" for the analysis

-- ---------- Master data ----------

CREATE TABLE OCRD (                -- Business partners
    CardCode   TEXT PRIMARY KEY,
    CardName   TEXT NOT NULL,
    CardType   TEXT NOT NULL CHECK (CardType IN ('C', 'S')),  -- C = customer, S = supplier
    LicTradNum TEXT,               -- VAT number
    Country    TEXT,
    City       TEXT,
    frozenFor  TEXT NOT NULL DEFAULT 'N',  -- 'Y' = blocked for new documents
    frozenFrom TEXT,
    CreateDate TEXT NOT NULL
);

CREATE TABLE OITM (                -- Items
    ItemCode   TEXT PRIMARY KEY,
    ItemName   TEXT NOT NULL,
    ItmsGrpNam TEXT NOT NULL,      -- item group (B1 stores a code in OITB; simplified)
    InvntryUom TEXT NOT NULL,
    MinLevel   REAL NOT NULL,      -- minimum stock level
    AvgPrice   REAL NOT NULL       -- average cost
);

CREATE TABLE OWHS (                -- Warehouses
    WhsCode TEXT PRIMARY KEY,
    WhsName TEXT NOT NULL
);

CREATE TABLE OITW (                -- Stock per item and warehouse
    ItemCode   TEXT NOT NULL REFERENCES OITM (ItemCode),
    WhsCode    TEXT NOT NULL REFERENCES OWHS (WhsCode),
    OnHand     REAL NOT NULL,
    IsCommited REAL NOT NULL,      -- reserved by open sales orders (B1 spelling)
    OnOrder    REAL NOT NULL,      -- open purchase quantity
    PRIMARY KEY (ItemCode, WhsCode)
);

-- ---------- Marketing documents ----------
-- Every document type uses the same header and line layout.

CREATE TABLE ORDR (DocEntry INTEGER PRIMARY KEY, DocNum INTEGER NOT NULL, CardCode TEXT NOT NULL,
    DocDate TEXT NOT NULL, DocDueDate TEXT NOT NULL, DocStatus TEXT NOT NULL, CANCELED TEXT NOT NULL,
    VatSum REAL NOT NULL, DocTotal REAL NOT NULL, DocCur TEXT NOT NULL);        -- Sales orders (17)
CREATE TABLE ODLN (DocEntry INTEGER PRIMARY KEY, DocNum INTEGER NOT NULL, CardCode TEXT NOT NULL,
    DocDate TEXT NOT NULL, DocDueDate TEXT NOT NULL, DocStatus TEXT NOT NULL, CANCELED TEXT NOT NULL,
    VatSum REAL NOT NULL, DocTotal REAL NOT NULL, DocCur TEXT NOT NULL);        -- Deliveries (15)
CREATE TABLE OINV (DocEntry INTEGER PRIMARY KEY, DocNum INTEGER NOT NULL, CardCode TEXT NOT NULL,
    DocDate TEXT NOT NULL, DocDueDate TEXT NOT NULL, DocStatus TEXT NOT NULL, CANCELED TEXT NOT NULL,
    VatSum REAL NOT NULL, DocTotal REAL NOT NULL, DocCur TEXT NOT NULL);        -- A/R invoices (13)
CREATE TABLE OPOR (DocEntry INTEGER PRIMARY KEY, DocNum INTEGER NOT NULL, CardCode TEXT NOT NULL,
    DocDate TEXT NOT NULL, DocDueDate TEXT NOT NULL, DocStatus TEXT NOT NULL, CANCELED TEXT NOT NULL,
    VatSum REAL NOT NULL, DocTotal REAL NOT NULL, DocCur TEXT NOT NULL);        -- Purchase orders (22)
CREATE TABLE OPDN (DocEntry INTEGER PRIMARY KEY, DocNum INTEGER NOT NULL, CardCode TEXT NOT NULL,
    DocDate TEXT NOT NULL, DocDueDate TEXT NOT NULL, DocStatus TEXT NOT NULL, CANCELED TEXT NOT NULL,
    VatSum REAL NOT NULL, DocTotal REAL NOT NULL, DocCur TEXT NOT NULL);        -- Goods receipt POs (20)
CREATE TABLE OPCH (DocEntry INTEGER PRIMARY KEY, DocNum INTEGER NOT NULL, CardCode TEXT NOT NULL,
    DocDate TEXT NOT NULL, DocDueDate TEXT NOT NULL, DocStatus TEXT NOT NULL, CANCELED TEXT NOT NULL,
    VatSum REAL NOT NULL, DocTotal REAL NOT NULL, DocCur TEXT NOT NULL);        -- A/P invoices (18)

CREATE TABLE RDR1 (DocEntry INTEGER NOT NULL, LineNum INTEGER NOT NULL, ItemCode TEXT NOT NULL,
    Quantity REAL NOT NULL, OpenQty REAL NOT NULL, Price REAL NOT NULL, LineTotal REAL NOT NULL,
    WhsCode TEXT NOT NULL, LineStatus TEXT NOT NULL, BaseType INTEGER NOT NULL, BaseEntry INTEGER,
    BaseLine INTEGER, PRIMARY KEY (DocEntry, LineNum));
CREATE TABLE DLN1 (DocEntry INTEGER NOT NULL, LineNum INTEGER NOT NULL, ItemCode TEXT NOT NULL,
    Quantity REAL NOT NULL, OpenQty REAL NOT NULL, Price REAL NOT NULL, LineTotal REAL NOT NULL,
    WhsCode TEXT NOT NULL, LineStatus TEXT NOT NULL, BaseType INTEGER NOT NULL, BaseEntry INTEGER,
    BaseLine INTEGER, PRIMARY KEY (DocEntry, LineNum));
CREATE TABLE INV1 (DocEntry INTEGER NOT NULL, LineNum INTEGER NOT NULL, ItemCode TEXT NOT NULL,
    Quantity REAL NOT NULL, OpenQty REAL NOT NULL, Price REAL NOT NULL, LineTotal REAL NOT NULL,
    WhsCode TEXT NOT NULL, LineStatus TEXT NOT NULL, BaseType INTEGER NOT NULL, BaseEntry INTEGER,
    BaseLine INTEGER, PRIMARY KEY (DocEntry, LineNum));
CREATE TABLE POR1 (DocEntry INTEGER NOT NULL, LineNum INTEGER NOT NULL, ItemCode TEXT NOT NULL,
    Quantity REAL NOT NULL, OpenQty REAL NOT NULL, Price REAL NOT NULL, LineTotal REAL NOT NULL,
    WhsCode TEXT NOT NULL, LineStatus TEXT NOT NULL, BaseType INTEGER NOT NULL, BaseEntry INTEGER,
    BaseLine INTEGER, PRIMARY KEY (DocEntry, LineNum));
CREATE TABLE PDN1 (DocEntry INTEGER NOT NULL, LineNum INTEGER NOT NULL, ItemCode TEXT NOT NULL,
    Quantity REAL NOT NULL, OpenQty REAL NOT NULL, Price REAL NOT NULL, LineTotal REAL NOT NULL,
    WhsCode TEXT NOT NULL, LineStatus TEXT NOT NULL, BaseType INTEGER NOT NULL, BaseEntry INTEGER,
    BaseLine INTEGER, PRIMARY KEY (DocEntry, LineNum));
CREATE TABLE PCH1 (DocEntry INTEGER NOT NULL, LineNum INTEGER NOT NULL, ItemCode TEXT NOT NULL,
    Quantity REAL NOT NULL, OpenQty REAL NOT NULL, Price REAL NOT NULL, LineTotal REAL NOT NULL,
    WhsCode TEXT NOT NULL, LineStatus TEXT NOT NULL, BaseType INTEGER NOT NULL, BaseEntry INTEGER,
    BaseLine INTEGER, PRIMARY KEY (DocEntry, LineNum));

CREATE INDEX ix_dln1_base ON DLN1 (BaseType, BaseEntry, BaseLine);
CREATE INDEX ix_inv1_base ON INV1 (BaseType, BaseEntry, BaseLine);
CREATE INDEX ix_pdn1_base ON PDN1 (BaseType, BaseEntry, BaseLine);
CREATE INDEX ix_pch1_base ON PCH1 (BaseType, BaseEntry, BaseLine);
