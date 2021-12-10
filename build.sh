#!/bin/bash

download() {
    curl -sSLO 'http://standards-oui.ieee.org/oui/oui.csv'
    curl -sSLO 'http://standards-oui.ieee.org/oui28/mam.csv'
    curl -sSLO 'http://standards-oui.ieee.org/oui36/oui36.csv'
}

merge_csv() {
    for file in oui.csv mam.csv oui36.csv; do
        sed -i '1d' "$file"
    done
    cat oui.csv mam.csv oui36.csv >mac.csv
    rm oui.csv mam.csv oui36.csv

}

commit() {
    git config user.name 'WH-2099 CI/CD'
    git config user.email 'github-actions@github.com'
    git add sha256sum.txt mac.csv mac.db
    git commit -m "CI/CD Auto Update"
    git push
}

build() {
    if ! sha256sum -c sha256sum.txt; then
        sha256sum mac.csv >sha256sum.txt
        dbfile='mac.db'
        table='mac'
        rm "$dbfile"
        sqlite3 "$dbfile" <<_EOF
        CREATE TABLE $table (
            registry TEXT,
            assignment TEXT COLLATE NOCASE,
            organization_name TEXT,
            organization_address TEXT
        );
        CREATE INDEX assignment_index ON $table (assignment);
_EOF
        sqlite3 "$dbfile" ".import --csv 'mac.csv' $table"
        commit
    fi
}

main() {
    download
    merge_csv
    build
}
main
