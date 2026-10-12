---
name: ad-ldap-enum
description: Export authorized AD users, computers and group membership with Crowe ad-ldap-enum. Use when packaged CSV inventories, historical TSV files, authentication selection or partial-query results need interpretation.
---

# Export the selected directory inventory

Read this entire SKILL.md before acting. Require the installed trusted tool/dependencies, selected AD domain/DC and an identity authorized for this inventory. No conditional resources are required. Finish with actual bind/base, query diagnostics and parsed output coverage; a successful connection or created file is insufficient.

Check `ad-ldap-enum --help` against the installed parser. Interfaces differ across revisions: historical scripts use -d/-l/-u and TSV; the TARGET interface below uses `domain/user@dc`. Do not mix these grammars. Use an existing private Kerberos cache and trusted LDAPS endpoint; define `identity` as the known `domain.example/user`, `dc_fqdn` as the DC's actual FQDN, `cache_path` as the cache's absolute file path and `out` as a fresh absolute private output directory:

~~~bash
umask 077
mkdir "$out" && (
    cd "$out" || exit
    KRB5CCNAME="$cache_path" ad-ldap-enum "$identity@$dc_fqdn" \
      -k -no-pass --method ldaps -ql 30 --page-size 500 -o inventory_
)
status=$?
~~~

The installed authentication library must support this cache representation. Check its principal/expiry and actual server-returned identity. A host FQDN is the service endpoint, not a user's UPN suffix. Missing dependencies, DNS/SPN, trust or bind errors remain specific prerequisites; do not supply a recovered key or disable validation to repair an inventory command.

The tool queries users, groups and computers across its selected base, even when only computer output is wanted. Confirm that collection scope first. -ql is a search limit whose application depends on the dependency's API, not a whole-process deadline; apply the worker's task budget. Do not add nested expansion merely to find a computer's hostname.

Parse the emitted format by headers, retaining DN/account and SPN associations. Current CSV outputs include Extended_Domain_User_Information, Extended_Domain_Computer_Information and Domain_Group_Membership. Older TSV and optional Excel files differ. Outputs can include a readable userPassword attribute and personal directory data; retain them privately.

Query errors may be logged while partial/header-only CSVs are still written. Inspect all query diagnostics/counts and selected rows before claiming absence or completeness. A membership export is not a full effective-rights assessment; a computer SPN is not a currently verified listener. A channel-binding option/banner alone does not establish that the dependency applied it.

Resolve differences against [upstream usage](https://github.com/CroweCybersecurity/ad-ldap-enum) and the [actual parser/query writer](https://github.com/CroweCybersecurity/ad-ldap-enum/blob/main/adldapenum/cli.py).
