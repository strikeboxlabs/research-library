---
name: impacket-lookupsid
description: Resolve a bounded Windows RID range to account and group names with Impacket lookupsid from Linux. Use to retain SID scope and principal types and distinguish incomplete lookup coverage from an empty directory.
---

# Bounded SID lookup

Read this entire SKILL.md before acting. Require the selected server, permitted session, SID scope and bounded RID interval. No conditional resource is required. Finish with resolved principal types, the complete lookup/error log and any incomplete interval; a successful exit alone does not establish coverage.

Check the installed entrypoint (`impacket-lookupsid` or `lookupsid.py`) and its `-h`. This is LSA name lookup over SMB, requiring a permitted session and policy lookup access. It does not validate passwords for the names returned.

The transport is genuinely SMB-only: the client always remaps the target to an `ncacn_np` pipe binding (`\\pipe\lsarpc`) and dials TCP 445. With 445 filtered, the run dies with a connection timeout to `:445` even when 135 is open — and passing a raw dynamic-port stringbinding such as `ncacn_ip_tcp:host[49664]` does not redirect it; the script prefixes the pipe name onto that string and still dials 445. To recover interface/port inventory without SMB, use `impacket-rpcdump` against 135 (endpoint-mapper query): it reports SAMR/LSA bindings including their dynamic TCP ports. Directly dialing those dynamic ports with a custom `DCERPCTransportFactory` script is the only bypass, and perimeter filtering usually drops them — treat a filtered dynamic RPC port as a closed path, not a lookup failure to retry.

Define `lookup` as that executable, `server` as one approved host, `domain`/`account` as the known login identity, `rid_limit` as the agreed positive upper bound, and `log` as a new private output path. Enter the known password at the prompt:

~~~bash
"$lookup" "$domain/$account@$server" "$rid_limit" >"$log" 2>&1
~~~

The positional bound is exclusive: 2000 requests RIDs 0–1999. Default 4000 is a range, not a complete user inventory. `-no-pass` suppresses prompting; it does not choose guest or anonymous identity. Select an empty-password account explicitly only when intended.

Preserve the reported SID prefix, host, range and complete log. Default lookup uses the target's account-domain SID; a member server's local accounts and AD accounts are different scopes. `-domain-sids` selects the primary-domain SID and can forward lookups to a DC, expanding the operation's reach. Check that scope before using it. `-target-ip` changes the connection address while retaining the target name.

Illustrative result rows:

~~~text
1000: LAB\DC01$ (SidTypeUser)
1104: LAB\alex (SidTypeUser)
1109: LAB\Support (SidTypeGroup)
~~~

Combine the recorded SID prefix with a row's RID to identify that principal. Keep the domain and type when extracting names offline; do not rerun network lookups merely to reformat output. `SidTypeUser` can include machine, built-in and service identities. These rows neither establish a human-login list nor show enabled state, group membership or access rights. Use a selected account's directory metadata when those distinctions matter.

No rows can mean unmapped RIDs, the wrong SID scope or a failed operation. Inspect authentication, pipe binding, policy access and lookup errors before expanding the range. The upstream script can log a failure and still exit zero; an exit code alone cannot certify coverage. Stop on an unresolved failure and retain the incomplete interval.

For packaging or behavior differences, compare the installed script with [upstream lookupsid](https://github.com/fortra/impacket/blob/master/examples/lookupsid.py); use Microsoft's [SID scope explanation](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers) to interpret local versus domain identities.
