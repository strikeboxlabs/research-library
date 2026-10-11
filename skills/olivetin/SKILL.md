---
name: olivetin
description: Enumerate and exploit OliveTin automation dashboards.
---

# OliveTin testing

Use when an OliveTin instance is found (typically on 127.0.0.1:1337 on a compromised host, config at /etc/OliveTin/config.yaml, binary /usr/local/bin/OliveTin, systemd unit OliveTin.service). OliveTin is a general-purpose self-hosted automation dashboard (github.com/OliveTin/OliveTin), not a CTF-specific component — it appears on any kind of host where admins expose pre-configured shell commands via web UI. It runs configured `shell:` actions, frequently as root, and exposes a Connect-RPC JSON API.

## Known vulnerability classes (project-wide, not box-specific)

- **CVE-2026-27626 / GHSA-49gm-hh7w-wfvf** (all versions ≤ 3000.10.0): OS command injection via `password`-typed arguments — `checkShellArgumentSafety()` omits the `password` type, so metacharacters in password values reach `sh -c` unvalidated. Second vector: webhook-extracted JSON values skip type checks entirely (unauthenticated RCE on webhook-triggered actions).
- **GHSA-xc5w-4v5w-7x65**: same bypass for custom `regex:`-prefixed argument types; even restrictive-looking patterns are bypassable via `$()` command substitution.
- **GHSA-vc6p-m6vx-6cwq**: second-order injection via `shellAfterCompleted` — the `output`/`ot_username`/`exitCode` template variables are never type-checked before reaching `sh -c`.
- Net effect: any Shell-mode action with a password/regex-typed argument, or a webhook-triggered action, is an RCE primitive running as the OliveTin process user (often root).

## Default-exposed state (verified 2026-10-11, proj_009)

- `listenAddressSingleHTTPFrontend: 127.0.0.1:1337` — loopback only, but any local user who can reach it can use the API.
- `authRequireGuestsToLogin: false` with `defaultPermissions: view/exec/logs: true` — the API is usable unauthenticated as user `guest`.
- Actions defined in config.yaml with `shell: "..."` strings are executed by a shell under the OliveTin process user (often root).

## API

JSON over POST to `http://127.0.0.1:1337/api/olivetin.api.v1.OliveTinApiService/<Method>`:

- `Init` `{}` — version and auth state (`loginRequired`, `authenticatedUser`).
- `GetDashboard` `{}` — actions and bindings (find `bindingId`s).
- `ValidateArgumentType` `{bindingId, argumentName, value}` — argument validation (useful to test payloads without executing).
- `StartAction` / `StartActionAndWait` `{bindingId, arguments: [{name, value}...], uniqueTrackingId}` — execute.
- `GetLogs`, `KillAction` — post-execution evidence.

Content-Type: application/json. Responses are plain JSON (e.g. `{"executionTrackingId":"..."}`).

## Command injection via argument substitution into shell: strings

When an action's `shell:` string embeds named template arguments, argument values are substituted UNSANITIZED into the shell command. Even `type: password` arguments are only quoting-validated by `ValidateArgumentType` (verified: metacharacters accepted as valid). If the shell string quotes the argument, break out with a leading single quote:

`"x' ; cat /root/root.txt > /tmp/r.txt; #"`

Verified root command execution this way (proj_009: `backup_database` action running its configured database backup command as root). Actions using `exec:` argv style are NOT injectable this way; only `shell:` string actions are.

## Recon from a compromised shell

Read `/etc/OliveTin/config.yaml` (world-readable in the verified case) to enumerate actions, argument types and defaults before calling the API. Check reachability per local user: a local firewall may block the web user (www-data) but allow human accounts — pivot with `su` before declaring the port closed.
