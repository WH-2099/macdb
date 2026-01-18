# /// script
# requires-python = ">=3.14"
# ///
import csv
import sys
from pathlib import Path
from typing import Dict, Optional


def load_database(csv_path: Path) -> Dict[str, dict]:
    """Loads the MAC database into memory for fast lookup."""
    database = {}
    if not csv_path.exists():
        print(
            f"Error: {csv_path} not found. Please run the build process first.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use assignment as key for O(1) lookup
            database[row["assignment"]] = row
    return database


def lookup_mac(mac_address: str, database: Dict[str, dict]) -> Optional[dict]:
    """
    Look up a MAC address in the database following IEEE hierarchy rules.
    """
    # Normalize: "AA:BB:CC:DD:EE:FF" -> "AABBCCDDEEFF"
    clean_mac = "".join(c for c in mac_address if c.isalnum()).upper()

    if len(clean_mac) < 6:
        return None

    # 1. Match 24 bits (MA-L)
    res = database.get(clean_mac[:6])

    # 2. Check for MA-M (28 bits) if the first match is a registration authority
    if res and res["org_name"] == "IEEE Registration Authority" and len(clean_mac) >= 7:
        res_28 = database.get(clean_mac[:7])
        if res_28:
            res = res_28

            # 3. Check for MA-S (36 bits)
            if res["org_name"] == "IEEE Registration Authority" and len(clean_mac) >= 9:
                res_36 = database.get(clean_mac[:9])
                if res_36:
                    res = res_36

    return res


def main():
    if len(sys.argv) < 2:
        print("Usage: python lookup.py <MAC_ADDRESS>")
        print("Example: python lookup.py AA:BB:CC:DD:EE:FF")
        sys.exit(1)

    mac_input = sys.argv[1]
    db_path = Path(__file__).parent / "mac.csv"

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
