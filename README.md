# MAC Address Database

MAC Address Vendor Information Database

**English** | [中文](README_zh.md)

## Features

Identify device manufacturer information through MAC addresses.

## How It Works

The common 48-bit MAC address is actually defined by IEEE (Institute of Electrical and Electronics Engineers), originally named EUI-48 (48 Bits Extended Unique Identifiers). EUI-48 contains an OUI (Organizationally Unique Identifier), which is a unique identifier managed and assigned by IEEE to hardware manufacturers. By identifying this portion, the device manufacturer can be determined.

> EUI-48 and EUI-64 identifiers are most commonly used as globally unique network addresses (sometimes called MAC addresses), as specified in various standards. For example, an EUI-48 is commonly used as the address of a hardware interface according to IEEE Std 802, historically using the name "MAC-48". As another example, an EUI-64 may serve as the identifier of a clock, per IEEE Std 1588. IEEE Std 802 also specifies EUI-64 use for 64-bit globally unique network addresses.

**This project uses IEEE official website as the data source, integrates the database and syncs automatically on a daily basis.**

## Usage

### Supported Data Formats

Data files are available directly in the repository:

- CSV ([mac.csv](mac.csv))

### Field Description

| Field | Description | Original (IEEE) | Example |
| ----- | ----------- | --------------- | ------- |
| `registry` | Assigned OUI type | `Registry` | MA-L |
| `assignment` | IEEE assigned Unique Identifier | `Assignment` | 002272 |
| `org_name` | Manufacturer name | `Organization Name` | American Micro-Fuel Device Corp. |
| `org_address` | Manufacturer address | `Organization Address` | 2181 Buchanan Loop Ferndale WA US 98248 |

### Lookup Steps

1. Take the first **24** bits of the MAC address (in common hyphen-separated hexadecimal notation, this is the first 6 hex characters of the first three groups, e.g., AABBCC from AA-BB-CC-DD-EE-FF)\
   Perform an exact match against the `assignment` field in the database.
2. If the `org_name` field of the match result is `IEEE Registration Authority`, proceed to the next step;\
   Otherwise, return the current match result directly.
3. Take the first **28** bits of the MAC address (the first 7 hex characters, e.g., AABBCCD from AA-BB-CC-DD-EE-FF)\
   Perform an exact match against the `assignment` field in the database.
4. If the `org_name` field of the match result is `IEEE Registration Authority`, proceed to the next step; otherwise, return the current match result directly.
5. Take the first **36** bits of the MAC address (the first 9 hex characters, e.g., AABBCCDDE from AA-BB-CC-DD-EE-FF)\
   Perform an exact match against the `assignment` field in the database.
6. If there is a result, return it directly; if no result, return empty.

### Official Lookup Page

<https://regauth.standard.ieee.org/standards-ra-web/pub/view.html>

### Official Data Sources

1. MAC Address Block Large (**MA-L**) [TXT](http://standards-oui.ieee.org/oui/oui.txt) [CSV](http://standards-oui.ieee.org/oui/oui.csv)
2. MAC Address Block Medium (**MA-M**) [TXT](http://standards-oui.ieee.org/oui28/mam.txt) [CSV](http://standards-oui.ieee.org/oui28/mam.csv)
3. MAC Address Block Small (**MA-S**) [TXT](http://standards-oui.ieee.org/oui36/oui36.txt) [CSV](http://standards-oui.ieee.org/oui36/oui36.csv)

### Official Matching Guidance

> If the first 24 bits match an OUI assigned to the IEEE RA, then a search of the first 28 or 36 bits may reveal an MA-M or MA-S assignment. If the OUI-36 is not found in an MA-S search, then a search of the first 24 or 28 bits may reveal an MA-L or MA-M assignment from which the OUI-36 has been created from a member of the assigned block.

Note that the final lookup results may not always be completely accurate!

> Your attention is called to the fact that the firms and numbers listed may not always be obvious in product implementation. Some manufacturers subcontract component manufacture and others include registered firms' All MAC (MA-L, MA-M, MA-S) in their products.
