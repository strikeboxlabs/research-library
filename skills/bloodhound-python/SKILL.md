---
name: bloodhound-python
description: Collect scoped AD directory evidence with BloodHound.py from Linux. Use when selecting CE versus legacy collectors, diagnosing Kerberos/DNS failures or distinguishing collected rights from current access.
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

## Turn a graph path into specific evidence questions

Keep each edge's source principal, destination object and collection time. A user marked owned is an operator annotation; it does not verify a credential or session. Evaluate different edge types separately:

| Edge or observation | What to verify next |
|---|---|
| `WriteOwner` over a group | Current owner and applicable DACL. Changing ownership, changing the DACL and changing membership are separate operations; the edge does not mean the user is already a member. |
| `WriteDacl`, `GenericWrite` or `GenericAll` | The exact destination and requested operation. Inspect applicable ACEs, property/extended-right GUIDs, group context and restrictions; a broad graph label is not a completed attribute write. |
| `CanPSRemote` to a computer | Current account context, reachable WinRM endpoint and session-configuration permissions. This is a graph relationship, not an AD user attribute or proof of an established remote session. |

Ownership normally brings implicit DACL control, but `OWNER RIGHTS` ACEs and server/object-specific restrictions can change that conclusion. Resolve uncertain ownership paths against Microsoft's [owner-rights conditions](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/fb7c101d-ec8b-4fbf-bca8-7d7c2d747d0c) and [SID definitions](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers). A historical graph cannot settle the current object's state.

Use [collector generation and method guidance](https://github.com/dirkjanm/BloodHound.py), [CE CLI](https://github.com/dirkjanm/BloodHound.py/blob/bloodhound-ce/bloodhound/__init__.py), [legacy CLI](https://github.com/dirkjanm/BloodHound.py/blob/master/bloodhound/__init__.py) and the [CanPSRemote definition](https://bloodhound.specterops.io/resources/edges/can-ps-remote) when resolving format or edge differences.
