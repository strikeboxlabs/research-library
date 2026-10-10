# Selected key-credential recovery and UPN update

These are separate directory mutations. Require the actual target DN/SID, selected initiating identity and present attribute values. A BloodHound GenericWrite edge is a reason to inspect the current operation-specific rights, not proof either write succeeds. Preserve the original values and a restoration route before changing them. Never clear all key credentials merely to repair a failed attempt.

## Temporary KeyCredentialLink operation

Use when a scoped credential audit specifically permits adding a key credential to one account, authenticating with it and recovering that account's NT hash. Require a supporting DC/Kerberos PKINIT environment and suitable KDC certificate; an LDAP write alone cannot supply those prerequisites. Existing legitimate device credentials must remain intact.

Define `certipy_bin` as the verified ly4k tool, `operator` as its known `user@domain` login, `subject` as the exact target account and `dc_ip` as the selected DC. In a fresh private output directory:

~~~bash
"$certipy_bin" shadow list -u "$operator" -account "$subject" -dc-ip "$dc_ip"
"$certipy_bin" shadow auto -u "$operator" -account "$subject" -dc-ip "$dc_ip"
"$certipy_bin" shadow list -u "$operator" -account "$subject" -dc-ip "$dc_ip"
~~~

Enter known credentials through the supported prompt. Listing identifies DeviceIDs but is not a complete raw-attribute backup; retain the original attribute values through the selected directory evidence mechanism. The reviewed auto implementation reads old values, appends its credential, authenticates, attempts to restore old values and reports the recovered NT hash. Exceptions/interruption or restoration failure can leave the modification; verify the original set rather than trusting the name `auto`. A list with no values can also mean insufficient read permission.

Distinguish the LDAP write, PKINIT ticket, NT-hash recovery and cleanup outcomes. A private key/certificate, TGT and NT hash are different artifacts. The shadow certificate need not be a CA-enrolled certificate; this path depends on the account's KeyCredentialLink trust. A restored attribute does not destroy acquired caches/hash material. Finish with the selected identity/result and restoration evidence, redacting secrets. If authentication fails, diagnose KDC/PKINIT/identity separately and reconcile the owned credential before retrying.

## Change and restore one UPN

For an explicitly scoped UPN/name-mapping test, define `test_upn` as the reviewed value and preserve `original_upn` plus whether the original attribute was absent. Inspect installed `account` help and the exact target before update:

~~~bash
"$certipy_bin" account read -u "$operator" -user "$subject" -dc-ip "$dc_ip"
"$certipy_bin" account update -u "$operator" -user "$subject" -upn "$test_upn" -dc-ip "$dc_ip"
"$certipy_bin" account read -u "$operator" -user "$subject" -dc-ip "$dc_ip"
~~~

A changed UPN is not a SAM-name/SID change, nor permission on the similarly named account. Confirm uniqueness/lookup behavior and retain actual write/read-back status. In a supporting AD-to-Linux Kerberos test, request an enterprise-principal TGT using **this account's credential**, not a guessed password for the comparison account. With a reviewed Impacket getTGT invocation, an independent private directory and observed `domain`/`dc_ip`:

~~~bash
impacket-getTGT -principalType NT_ENTERPRISE -dc-ip "$dc_ip" "$domain/$test_upn"
~~~

Inspect the newly reported cache with `klist -c "$cache"`, including principal/realm/time. A supporting Linux service might authorize through a client-name/NSS mapping differently from Windows SSPI's original AD SID/PAC identity. Neither UPN write nor TGT proves that service maps to the intended Linux user; retain actual service authentication and remote identity. It also does not establish certificate ESC behavior by itself.

For a nonempty original UPN, restore with the same account update command using `-upn "$original_upn"` and read back. An originally absent attribute needs the installation's supported attribute-delete semantics; an arbitrary empty-string update is not assumed equivalent. Account for that prerequisite before the test. Do not rename the account or reset a password as cleanup.

See [shadow action implementation](https://github.com/ly4k/Certipy/blob/main/certipy/commands/shadow.py), [account operations](https://github.com/ly4k/Certipy/blob/main/certipy/commands/account.py) and the primary [mixed-stack Kerberos analysis](https://www.pentestpartners.com/security-blog/a-broken-marriage-abusing-mixed-vendor-kerberos-stacks/). Issuance/PFX authentication is a separate reference in the entrypoint.
