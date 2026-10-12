---
name: impacket-getst
description: Request a Kerberos service ticket with Impacket getST and inspect the resulting cache. Use when SPNs, existing delegation, cache identity or confusing service tickets with TGTs causes authentication failures.
---

# Request the ticket for the intended service

Read this entire SKILL.md before acting. Require the known requesting identity, KDC, exact service principal and any existing delegation selected by the task. No conditional resource is required. Finish with the actual cache's identity, service, flags and lifetime plus request errors; ticket issuance and application authorization remain separate outcomes.

Check `impacket-getST -h`; upstream also ships `getST.py`. Define `getst_bin` as the installed executable, `identity` as the known `domain/account`, `dc_ip` as the intended KDC address, `spn` as the exact registered service/hostname, and `out` as a new private directory:

~~~bash
umask 077
mkdir "$out" && (
    cd "$out" || exit
    "$getst_bin" -dc-ip "$dc_ip" -spn "$spn" "$identity"
)
~~~

Without a password in `identity`, this prompts for the known password. An existing compatible TGT can instead be selected through an absolute `KRB5CCNAME` with `-k -no-pass`; inspect its principal and lifetime first. Missing/unusable cache credentials can cause a fresh TGT attempt, so inspect the authentication log rather than assuming cache reuse.

For a specifically authorized test of **existing** constrained delegation, `-impersonate "$delegated_user"` requests a service ticket for that named user through S4U. Establish the requesting account, delegated identity, target SPN and actual delegation permission beforehand. The switch does not grant that permission. `-self` stops at S4U2Self, which is not the completed S4U2Proxy ticket to the intended service. Do not add ticket-alteration switches to hide an unexplained failure.

Use the actual cache filename reported by the installed build; names differ across versions. Define `ticket_cache` as that absolute file and inspect it with `klist -c "$ticket_cache"`. Check client identity, service principal, realm, flags and validity before selecting it for a client. The saved result of the normal/S4U service-ticket flow is a **service ticket**, not a reusable TGT for arbitrary services, even if the tool obtained a TGT internally.

`KDC_ERR_S_PRINCIPAL_UNKNOWN` calls for checking SPNs, account/realm and the operation stage. `KDC_ERR_BADOPTION` can reflect delegation or ticket-flag restrictions; it does not prove a bad password. Verify clock agreement without automatically resetting the host clock. A ticket issued successfully can still be rejected by the application or authorize fewer actions than expected.

Use the [upstream CLI and cache saving](https://github.com/fortra/impacket/blob/master/examples/getST.py) and [MIT klist](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/klist.html) to resolve installed ticket/cache behavior.
