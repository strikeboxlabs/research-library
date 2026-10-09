---
name: impacket-reg
description: Query selected remote Windows registry keys with Impacket from Linux. Use when hive context, value types, registry permissions or RemoteRegistry service side effects need diagnosis.
---

# Impacket remote registry queries

Inspect `impacket-reg -h` and `impacket-reg query -h`; upstream may install `reg.py`. This is remote registry access over SMB/RPC, not offline hive parsing or a WinRM session. Successful SMB authentication does not establish registry-key access.

**Even a query can change service state.** The reviewed implementation checks RemoteRegistry, starts it when stopped, and can temporarily change a disabled start type. It attempts restoration afterward, with a named-pipe trigger fallback when service checks fail. If service changes are outside the task, choose an existing approved collection path instead. Do not describe this tool as universally read-only just because the selected registry action is `query`.

Define `identity` as the known `domain/user@host` without a password, and `registry_key` as the exact observed key path, stored with literal backslashes:

~~~bash
impacket-reg "$identity" query -keyName "$registry_key"
~~~

Enter the password at the prompt. This returns the key's values and immediate subkeys. For one selected value, define `value_name` and add `-v "$value_name"`. Use `-ve` for the unnamed default value. Add recursive `-s` only when the larger subtree is needed; it can expose much more data and encounter partial access failures.

Preserve key path, value name **and type**. `REG_MULTI_SZ` is a list, `REG_BINARY` needs its format interpreted, and environment-variable text in `REG_EXPAND_SZ` is not automatically an expanded path on your Linux machine. A printed credential-like string is historical/configuration evidence until independently validated.

`HKLM` is machine context; `HKCU` is the remote current-user mapping. `HKU` normally contains loaded user hives, often under SIDs, not every account's complete profile. Enumerate actual subkeys before constructing a path; do not assume the walkthrough's `HKU\Software` layout is universal.

Distinguish authentication, service-control, named-pipe, missing-key and access-denied errors. A partially printed subtree is not complete inventory. Inspect restoration diagnostics and verify any service state changes after interruption. `save`, `backup`, `add` and `delete` have different effects and are not substitutes for a failed query.

Documentation reviewed 2026-10-09; Linux execution untested. Case: APT pp. 10–11. Source: [reg CLI, query and service lifecycle](https://github.com/fortra/impacket/blob/master/examples/reg.py).
