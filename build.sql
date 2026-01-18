INSTALL httpfs;
LOAD httpfs;

CREATE VIEW raw_mac AS
SELECT * FROM read_csv([
    'http://standards-oui.ieee.org/oui/oui.csv',
    'http://standards-oui.ieee.org/oui28/mam.csv',
    'http://standards-oui.ieee.org/oui36/oui36.csv'
], header=True, columns={
    'Registry': 'TEXT',
    'Assignment': 'TEXT',
    'Organization Name': 'TEXT',
    'Organization Address': 'TEXT'
});

CREATE VIEW mac AS
SELECT
    "Registry" AS registry,
    "Assignment" AS assignment,
    "Organization Name" AS org_name,
    "Organization Address" AS org_address
FROM raw_mac
ORDER BY assignment, registry, org_name, org_address;

COPY mac TO 'mac.csv' (HEADER TRUE);

SELECT count(*) || ' records processed' AS status FROM mac;
