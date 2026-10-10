---
name: impacket-ticketer
description: Prepare and inspect a narrowly scoped synthetic Kerberos service-ticket fixture with Impacket ticketer. Use to distinguish service keys, SPNs, identity fields, cache creation and actual service acceptance in an authorized lab.
---

# Prepare a synthetic service-ticket fixture

Use this only for an authorized lab ticket fixture with known service-key material. Check `impacket-ticketer -h`; upstream may use `ticketer.py`. Specify `-spn` explicitly: omitting it changes the operation to TGT generation. A service ticket is not a general TGT for requesting unrelated services.

Establish the exact SPN, service account/key type, domain SID and intended test identity before generating anything. A domain SID is the domain portion, while `-user-id` is the account RID. The current defaults select RID 500, several privileged groups and a ten-year lifetime; choose these fields deliberately. An SPN assigned to an account is not proof of a currently running service or that a synthetic ticket will be accepted.

Define `ticketer_bin` as an absolute executable path, `out` as a new private directory, `spn` as the exact service principal, `domain` as the realm's DNS domain, `domain_sid`, `test_user`, `user_rid`, and `group_rids` as the approved fixture values. Define `keytab` as an existing absolute service-key file containing the matching SPN and intended key. For a one-hour offline fixture:

~~~bash
umask 077
mkdir "$out" && (
    cd "$out" || exit
    unset KRB5CCNAME
    "$ticketer_bin" -spn "$spn" -keytab "$keytab" -domain "$domain" -domain-sid "$domain_sid" -user-id "$user_rid" -groups "$group_rids" -duration 1 "$test_user"
)
~~~

The keytab form avoids putting key bytes in the command line; inspect its entries first rather than assuming the chosen encryption type. Clearing the inherited cache here prevents current versions from importing unrelated cache contents. Without request/impersonation modes this generates local ticket bytes. `-request` is a separate KDC-authenticated template flow, not an offline validation flag.

Where a fixture explicitly supplies an NT service key, `-nthash` replaces `-keytab`; AES uses `-aesKey`. These command-line forms expose the supplied key to local process inspection. An NT hash is the RC4-HMAC password-derived key; NetNTLMv2 responses and Kerberoast ciphertext are different artifacts, and an NT hash is not an AES key.

Use the output filename actually reported by the installed release. Define `cache` as that absolute path:

~~~bash
klist -c "$cache"
~~~

Check client, realm, service/hostname/port and validity. For SQL over TCP, retain the intended SPN's port instead of silently shortening it. Cache inspection proves structure and metadata, not a valid signature, target acceptance or authorization. A successfully saved cache can still fail because of key/encryption mismatch, SPN, time, PAC validation or application policy. Any service login is a separate, scoped test; retain its actual result without broadening the ticket's identities or groups to hide a failure.

See [ticketer's CLI and cache handling](https://github.com/fortra/impacket/blob/master/examples/ticketer.py), [MIT klist](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/klist.html), [RC4-HMAC key derivation](https://www.rfc-editor.org/rfc/rfc4757.html) and [SQL SPN formats](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/register-a-service-principal-name-for-kerberos-connections).
