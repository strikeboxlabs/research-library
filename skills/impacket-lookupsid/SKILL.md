---
name: impacket-lookupsid
description: Resolve a bounded Windows RID range to account and group names with Impacket lookupsid from Linux. Use to retain SID scope and principal types and distinguish incomplete lookup coverage from an empty directory.
---

# Bounded SID lookup

Check the installed entrypoint (`impacket-lookupsid` or `lookupsid.py`) and its `-h`. This is LSA name lookup over SMB, requiring a permitted session and policy lookup access. It does not validate passwords for the names returned.

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
