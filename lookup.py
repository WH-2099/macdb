# /// script
# requires-python = ">=3.14"
# ///
import csv
import sys
from pathlib import Path


REGISTRATION_AUTHORITY = "IEEE Registration Authority"
MATCH_LENGTHS = (6, 7, 9)

type MacRecord = dict[str, str]
type MacDatabase = dict[str, MacRecord]


def load_database(csv_path: Path) -> MacDatabase:
    """Load the MAC database into memory for fast lookup."""
    if not csv_path.is_file():
        print(
            f"Error: {csv_path} not found. Please run the build process first.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    database: MacDatabase = {}
    with csv_path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            database[row["assignment"]] = row
    return database


def lookup_mac(mac_address: str, database: MacDatabase) -> MacRecord | None:
    """Look up a MAC address using IEEE MA-L, MA-M, then MA-S hierarchy."""
    clean_mac = "".join(c for c in mac_address if c.isalnum()).upper()

    result = None
    for length in MATCH_LENGTHS:
        if len(clean_mac) < length:
            break

        record = database.get(clean_mac[:length])
        if record is None:
            break

        result = record
        if record["org_name"] != REGISTRATION_AUTHORITY:
            break

    return result


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python lookup.py <MAC_ADDRESS>")
        print("Example: python lookup.py AA:BB:CC:DD:EE:FF")
        raise SystemExit(1)

    mac_input = sys.argv[1]
    db_path = Path(__file__).with_name("mac.csv")

    db = load_database(db_path)
    result = lookup_mac(mac_input, db)

    if result:
        print(f"MAC Assignment: {result['assignment']}")
        print(f"Registry:       {result['registry']}")
        print(f"Organization:   {result['org_name']}")
        print(f"Address:        {result['org_address']}")
    else:
        print(f"No vendor found for MAC: {mac_input}")


if __name__ == "__main__":
    main()
