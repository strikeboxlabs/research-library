---
name: impacket-getadusers
description: Query AD user email and logon metadata with Impacket GetADUsers from Linux. Use when default filtering hides accounts, a certificate subject needs directory attributes or displayed dates and empty results need qualification.
---

# Inspect selected AD user metadata

Read this entire SKILL.md before acting. Require the installed compatible client, selected DC and an existing usable authentication context. No conditional resource is required. Finish with the selected subject/DC, returned metadata and status/diagnostics; an empty or failed query remains a visibility or prerequisite gap rather than proof of account absence.

Check `impacket-GetADUsers -h`; upstream installs may expose `GetADUsers.py`. This is an authenticated directory query. The commands below require the installed generation to support `-dc-host`, `-dc-ip`, `-k`, `-no-pass`, `-all` and `-user`. Use a verified DC hostname and a known usable Kerberos file cache; check its identity and expiry with `klist` first.

Define `cache` as that absolute cache path, `domain` as the AD DNS domain, `user` as the requesting account, `dc_fqdn` and `dc_ip` as the same selected DC, `subject` as one observed sAMAccountName, and `report`/`errors` as fresh private files:

~~~bash
umask 077
KRB5CCNAME="$cache" impacket-GetADUsers "$domain/$user" \
  -k -no-pass -dc-host "$dc_fqdn" -dc-ip "$dc_ip" \
  -all -user "$subject" >"$report" 2>"$errors"
status=$?
~~~

The default filter omits accounts lacking `mail` and disabled accounts. `-all` removes those exclusions; `-user` keeps the request focused. For an explicitly required directory-wide inventory, remove `-user "$subject"` while retaining `-all`. The account supplied before the switches authenticates the query; it is distinct from the selected subject.

Review both files and status. Some implementations catch errors and log them without a failing process exit. An empty table can mean a filter/permission/transport problem; a printed header is not collection success. This output is a display table rather than CSV: names and blank email fields make whitespace splitting unreliable. If exact attribute association matters, use an LDAP client that preserves DNs and values. Do not insert arbitrary unescaped filter characters into a selector.

## Interpret the four columns

| Observation | What to check next |
|---|---|
| Blank Email | No `mail` value was returned in this query. Establish attribute visibility before declaring it unset. A UPN or application email is a separate property. |
| A populated Email | Stored directory metadata, not mailbox verification or proof of enrollment permission. Check the actual certificate template and subject requirements. |
| LastLogon shows an old date or `<never>` | `lastLogon` is maintained independently on each DC. One DC cannot establish the account's latest domain-wide activity. |
| PasswordLastSet is `<never>` | The formatter uses this for zero. AD also uses zero for password-change-at-next-logon behavior under applicable account flags; it is not proof that a password never existed. |

Record the queried DC and the collector's timezone. The formatter uses local time without an offset; do not compare it directly with a UTC packet timestamp. Keep current account state and successful authentication separate from these stored dates. For a domain-wide last-logon conclusion, Microsoft's [lastLogon definition](https://learn.microsoft.com/en-us/windows/win32/adschema/a-lastlogon) requires comparing the relevant DC values. Its [pwdLastSet definition](https://learn.microsoft.com/en-us/windows/win32/adschema/a-pwdlastset) explains the zero-value special case.

Use the [upstream CLI/filter/format implementation](https://github.com/fortra/impacket/blob/master/examples/GetADUsers.py) and [connection helper](https://github.com/fortra/impacket/blob/master/impacket/examples/utils.py) to resolve release differences. A clock, SPN or bind failure calls for checking cache, DC naming and authentication/transport policy; it does not establish that the subject is absent.
