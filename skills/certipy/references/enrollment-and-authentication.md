# Request and use a selected certificate

## Submit an authorized enrollment

Identify the CA hostname, CA configuration name, published template's internal name and intended subject. The authenticating account must satisfy enrollment/agent policy; an ESC finding does not make every template request valid. Define `certipy_bin`, `upn`, `ca_fqdn`, `dc_ip`, `ca_name`, `template` and a fresh private `output_prefix`. Check `req -h` for the installed generation:

~~~bash
umask 077
"$certipy_bin" req -u "$upn" -target "$ca_fqdn" -dc-ip "$dc_ip" \
  -ca "$ca_name" -template "$template" -out "$output_prefix"
~~~

The CA name is not necessarily its hostname. The default RPC path, DCOM and Web Enrollment have different endpoint/permission requirements; a working LDAP query proves none of those transports is reachable. Select an alternative only when that enrollment path is actually supported and in scope.

Read request disposition and the logged output paths. A pending request ID or saved private key is not an issued certificate. For an existing pending request, preserve the matching key and use the installed `req -retrieve REQUEST_ID` workflow with the same CA context when issuance is approved; do not generate a new unrelated key and expect it to match. On a required-email error, inspect the subject's directory mail attribute and template name flags rather than assuming a UPN suffices.

For an authorized enrollment-agent task, add `-on-behalf-of "$subject" -pfx "$agent_pfx"`, where `subject` is the intended `DOMAIN\account` and the PFX contains the agent certificate and private key. Verify the agent EKU, destination template requirements, CA agent restrictions and subject enrollment rights. The requester's ordinary credentials and the signing agent's PFX serve different roles. A PFX password is also distinct from an AD account password; use the installed protected-input handling available to the task.

## Authenticate with the issued identity

Inspect the issued subject/SAN/SID, EKUs, validity, private-key match and expected mapping. For a selected PFX and account, define `pfx`, `user` and `domain`, then run in a private working directory:

~~~bash
"$certipy_bin" auth -pfx "$pfx" -username "$user" -domain "$domain" \
  -dc-ip "$dc_ip" -no-hash
~~~

`-no-hash` requests authentication without the separate NT-hash recovery step; it does not make PKINIT local/offline. Record the actual principal and logged saved cache path. Select that cache deliberately for a later Kerberos client; a file's existence is not proof that another process used it.

| Failure/result | Next decision |
|---|---|
| Certificate/key mismatch or unreadable PFX | Resolve the container/key input before contacting more endpoints. |
| Principal/mapping mismatch | Compare requested identity and certificate SID/strong mapping with current DC policy. |
| PKINIT unsupported or KDC certificate problem | Identify KDC PKINIT support/trust; this alone does not determine Schannel applicability. |
| TGT saved but later service access denied | Check selected cache, SPN, ticket lifetime and service authorization separately. |

Certificate issuance and authentication produce persistent credentials/audit state. Restoring a directory attribute does not revoke issued certificates or invalidate all tickets. Complete the task's lifecycle/revocation requirements explicitly rather than calling an attribute rollback complete cleanup.

Use [request options](https://github.com/ly4k/Certipy/blob/main/certipy/commands/parsers/req.py), [authentication options](https://github.com/ly4k/Certipy/blob/main/certipy/commands/parsers/auth.py) and [Certipy AD CS guidance](https://github.com/ly4k/Certipy/wiki) for version-specific behavior.
