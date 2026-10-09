---
name: mdbtools
description: Inspect Microsoft Access database files on Linux with mdb-tables and mdb-export. Use to select and export relevant tables while preserving names, quoting and multiline field values.
---

# MDB Tools table inspection

Use a local database copy. Define `database` as its absolute path; confirm the actual file format rather than trusting `.mdb`. List tables one per line:

~~~bash
mdb-tables --version
mdb-tables -1 "$database"
~~~

Table names can contain spaces. Select a complete returned name, define `table` accordingly, and choose a fresh `csv` output path:

~~~bash
mdb-export "$database" "$table" > "$csv"
~~~

This exports the selected table, normally with a header and CSV quoting. Use a CSV parser: commas, quotes and newlines can occur inside fields, so splitting on commas or counting text lines misinterprets records. Keep column names with values; a field named `password` does not establish its encoding or present validity.

If a table is absent, inspect the inventory instead of assuming the application schema matches a walkthrough. System tables are hidden by default (`mdb-tables -S -1` includes them). A linked table may refer to data outside this file. Export errors, encrypted/unsupported database variants and partial downloads need investigation before treating an empty CSV as an empty table.

For garbled older Jet 3 text, check the original character set and the documented `MDB_JET3_CHARSET` setting rather than silently discarding characters. Retain the database identity, table name, tool version and any export errors with the findings.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Access PDF p. 5. Maintenance sources: upstream [mdb-tables](https://github.com/mdbtools/mdbtools/blob/dev/doc/mdb-tables.txt) and [mdb-export](https://github.com/mdbtools/mdbtools/blob/dev/doc/mdb-export.txt).
