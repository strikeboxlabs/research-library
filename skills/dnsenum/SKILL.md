---
name: dnsenum
description: Compare a small approved hostname list with DNS records in an owned fixture using dnsenum. Use when aliases, wildcard responses or partial enumeration can be mistaken for complete host inventory.
---

# Resolve selected fixture names

Read this entire SKILL.md before acting. Require the installed implementation/dependencies, owned fixture zone and all its DNS endpoints, a small reviewed label list and permission for the tool's automatic zone-transfer attempts. Follow the bounded procedure below; finish with records, diagnostics, completion and limits. Missing prerequisites leave the task unresolved.

Review installed help against the [project overview](https://github.com/fwaeytens/dnsenum) and [actual option/operation implementation](https://github.com/fwaeytens/dnsenum/blob/master/dnsenum.pl). Run from a private disposable working directory: the tool writes a domain-named IP-list file. Its dependencies must already exist; this skill does not install them.

Set `zone` to the controlled fixture domain, `dns_server` to its resolver and `labels` to the existing absolute file containing only the approved hostname labels. Confirm fixture NS/MX names and endpoints beforehand. The initial server selection does not confine every operation: dnsenum also attempts AXFR against the zone's nameservers.

~~~bash
dnsenum --dnsserver "$dns_server" --noreverse --threads 1 --nocolor --verbose -f "$labels" "$zone"
status=$?
~~~

Keep stderr. This selects the short list and disables reverse-range queries. Omit recursion, WHOIS, scraping and the enum shortcut, which enables extra operations. If automatic contacts exceed the approved fixture, select a single-query client instead.

Preserve A/CNAME associations, wildcard diagnostics and individual query/transfer failures. A matching address can come from a wildcard. A CNAME alias does not establish another live server. Transfer denial is distinct from failed label resolution. Require the completion receipt plus status; even zero status cannot establish that every query succeeded or every possible hostname was tested. Verify the selected returned record before reporting it as inventory.
