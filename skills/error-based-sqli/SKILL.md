---
name: error-based-sqli
description: Run error-based SQL injection extraction reliably.
---

# Error-based SQLi extraction

Use when an injection point echoes database errors to the client (EXTRACTVALUE/UPDATEXML XPATH errors, duplicate-entry errors). Prefer this generic skill when the app-specific skill only names the injection.

## Payload shapes and parse

- EXTRACTVALUE: `AND EXTRACTVALUE(1,CONCAT('~R:',(<query>),'~')) -- ` (trailing space matters; `--+` is for URL-encoded contexts only). Parse `XPATH syntax error: '~R:<value>~` from the response; HTML-entity-decode.
- Truncation: EXTRACTVALUE echoes only ~32 chars (payload marker eats into it) — chunk with `SELECT SUBSTRING((<query>),<i>,<n>)` using n=25 to stay safely under the limit; a full chunk (len == n) means more data follows, a short chunk or NULL means end.
- Empty result: `SELECT COUNT(*)` / `SELECT 1` first to validate the channel before chunking; a NULL result means no rows, not a broken payload.

## Stacked queries

Same-parameter stacked statements work with PHP PDO multi-statement contexts (verify per app). Terminate the original query then append: `x'; <statement>; -- `. WRITE CAUTION: the error signature of a failed stacked statement can be IDENTICAL to a successful one (both return false-y to the app). Always read back the written value before building on it.

## Where you can't use INTO OUTFILE

MariaDB/MySQL reject INTO OUTFILE from subquery positions (error near 'INTO OUTFILE'), even with `secure_file_priv` empty. It only works as a top-level SELECT — via stacked statement after terminating the original query, or in a UNION tail. Check `@@secure_file_priv` first (EMPTY string = unrestricted, NULL = no file ops at all).

## Read-order discipline

1. `SELECT VERSION()` / `USER()` — engine and account.
2. `information_schema.schemata` → target schema.
3. `information_schema.tables`/`COLUMNS` for the tables you need — never guess column names; a wrong name shows as a syntax/access error, not empty data.
4. Chunked reads of actual rows; GROUP_CONCAT with SEPARATOR for batch listing (mind GROUP_CONCAT max length, default 1024 — chunk it too or SET SESSION group_concat_max_len if stacked queries work).

## Self-DoS awareness

Before ANY write, ask: does the application bootstrap from this table on every request? Writing malformed rows to settings/config tables (missing NOT NULL columns, wrong types) can 500 every page INCLUDING the injection point itself, with no recovery path except out-of-band DB access. Prefer tables used only for auth rendering or feature data (e.g. user tables with tolerant readers); test the write's blast radius on the least-critical table first.
