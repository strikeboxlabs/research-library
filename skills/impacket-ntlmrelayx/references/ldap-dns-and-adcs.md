# LDAP DNS record action and enrollment destinations

Read the package's relay-stage reference first. This branch makes a specific directory change after relay; it is not passive hash capture. Require the selected source identity, DC LDAP endpoint/protection findings, record name/value, authoritative zone and a read-back/restore plan. A captured NetNTLM response is not an NT hash to feed into a later `-hashes` login.

For an authorized DNS-record addition, define `dc_host`, `listen_ip`, `record_name` and `record_ip`. With a current build exposing the shown listener controls:

~~~bash
impacket-ntlmrelayx -t "ldap://$dc_host" -ip "$listen_ip" --http-port 8080 \
  --add-dns-record "$record_name" "$record_ip" --no-dump --no-da --no-acl --no-validate-privs \
  --no-smb-server --no-wcf-server --no-raw-server --no-rpc-server \
  --no-winrm-server --no-mssql-server --no-rdp-server
~~~

Match the installed options and verify actual listeners before arranging the controlled HTTP client connection. If TLS/signing/channel binding or directory rights reject the operation, preserve that stage; do not switch protocols/targets automatically. `--no-validate-privs` skips a privilege-assessment path and can assume privileges for subsequent actions; **it does not disable ACL changes**. `--no-acl`, `--no-da` and `--no-dump` explicitly suppress their separate actions. Do not copy a reduced switch list and call it DNS-only without reviewing this build's other defaults.

The action adds a DNS node with the chosen A record. Preserve bind principal, LDAP result, authoritative read-back and the specific object/value created. A successful authentication followed by access denied means this identity could bind but could not make that change. An existing-node/collision failure is not permission failure. Clean up only the owned node/value and verify removal; leave pre-existing records intact.

A long marshalled-target suffix used in a Kerberos relay experiment must follow its exact encoding/label constraints; it is not an arbitrary DNS label. This tool's LDAP addition only establishes the record action. A later SMB/Kerberos callback and certificate issuance require separate protocol evidence. Keep credentials, new caches and certificates private; removing DNS does not revoke a certificate.

For a separately selected classic Web Enrollment destination, the pertinent action options are:

~~~text
-t https://<verified-ca-host>/certsrv/certfnsh.asp --adcs --template <verified-template>
~~~

These are a branch to configure with the full intended listener controls, not an additional action on the preceding LDAP command. Validate URL, TLS/authentication and victim enrollment conditions. If HTTP negotiation does not offer the required NTLM scheme, the target cannot be assumed compatible merely because HTTPS responded. Do not equate a discovered Kerberos CES endpoint with `/certsrv`, or reinterpret an NTLM negotiation error as proof of PKU2U. A Kerberos relay implementation is a distinct protocol capability and still needs its own supported target.

An issuance request ID, HTTP 200, saved capture or a locally generated filename is not enough: inspect the issued certificate/private-key match and requested principal, then separately verify any requested authentication. See [CLI action/server controls](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py), [LDAP action ordering](https://github.com/fortra/impacket/blob/master/impacket/examples/ntlmrelayx/attacks/ldapattack.py) and [HTTP enrollment action](https://github.com/fortra/impacket/blob/master/impacket/examples/ntlmrelayx/attacks/httpattack.py).
