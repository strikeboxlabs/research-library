---
name: olivetin
description: Enumerate and exploit OliveTin automation dashboards.
---

# OliveTin testing

Use when an OliveTin instance is found (typically on 127.0.0.1:1337 on a compromised host, config at /etc/OliveTin/config.yaml, binary /usr/local/bin/OliveTin, systemd unit OliveTin.service). OliveTin runs configured `shell:` actions, frequently as root, and exposes a Connect-RPC JSON API.

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

When an action's `shell:` string embeds arguments in `{{ arg }}` placeholders, argument values are substituted UNSANITIZED into the shell command. Even `type: password` arguments are only quoting-validated by `ValidateArgumentType` (verified: metacharacters accepted as valid). If the shell string quotes the argument (e.g. `-p'{{ db_pass }}'`), break out with a leading single quote:

`"x' ; cat /root/root.txt > /tmp/r.txt; #"`

Verified root command execution this way (proj_009: `backup_database` action running `mysqldump ... -p'{{ db_pass }}'` as root). Actions using `exec:` argv style are NOT injectable this way; only `shell:` string actions are.

## Recon from a compromised shell

Read `/etc/OliveTin/config.yaml` (world-readable in the verified case) to enumerate actions, argument types and defaults before calling the API. Check reachability per local user: a local firewall may block the web user (www-data) but allow human accounts — pivot with `su` before declaring the port closed.
