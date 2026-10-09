---
name: bloodhound-python
description: Collect scoped AD directory evidence with BloodHound.py from Linux. Use when selecting CE versus legacy collectors, diagnosing Kerberos/DNS failures or assessing incomplete graph imports.
---

# BloodHound.py collection

Match the collector to the receiving BloodHound generation. Upstream's `bloodhound-python` targets legacy 4.2/4.3; its CE branch provides `bloodhound-ce-python`. Check the installed executable's help/banner and the server's accepted format before collecting. Do not transplant a historical Neo4j setup into CE.

For directory groups, ACLs and object properties, start with `DCOnly`. Default collection also contacts member computers; `All` expands that work and still excludes some methods. Choose additional methods only for a specific missing observation.

Define `collector` as the verified executable, `domain` as the AD DNS domain, `user` as the known account, `dc_fqdn` as the actual DC hostname, `dns_ip` as its reachable AD DNS server, and `out` as a new private directory. This prompts for the known password and requires Kerberos:

~~~bash
umask 077
mkdir -- "$out" && (
  cd -- "$out" || exit
  "$collector" -u "$user" -d "$domain" -dc "$dc_fqdn" -ns "$dns_ip" -c DCOnly --auth-method kerberos --zip
)
~~~

For an existing ticket cache, export its absolute filename in `KRB5CCNAME` and add `-k -no-pass`. Confirm these switches in local help. `-k` alone is not evidence that an older collector actually used Kerberos: the supplied walkthrough logs NTLM fallback. Check authentication messages.

An alternative DNS server is not a replacement for every operating-system hostname lookup. Check DC FQDN resolution, KDC reachability, cache identity/expiry and clock agreement before changing authentication. A bare domain alias in `/etc/hosts` may not resolve the DC hostname.

Retain collection methods, errors and object counts with the archive. Verify import completion and expected objects in the receiving server. A ZIP file proves neither a successful import nor complete collection; failed methods can explain missing edges. A graph edge records a modeled relationship at collection time, not a completed remote action.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Administrator pp. 3–4. Sources: [generation and collection guidance](https://github.com/dirkjanm/BloodHound.py), [CE CLI](https://github.com/dirkjanm/BloodHound.py/blob/bloodhound-ce/bloodhound/__init__.py), [legacy CLI](https://github.com/dirkjanm/BloodHound.py/blob/master/bloodhound/__init__.py).
