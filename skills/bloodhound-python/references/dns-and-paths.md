# TCP DNS and operation-specific path questions

For a SOCKS/ProxyChains route that only carries TCP, inspect the collector's `--dns-tcp` support. Explicitly select the reachable AD DNS server, DC FQDN and, where needed, `-gc` global-catalog FQDN. A server address does not replace its Kerberos service identity. Use the selected generation/methods from the entrypoint; `All` contacts more systems than a directory-only query.

With the same selected values and a reviewed task-specific proxy configuration:

~~~bash
proxychains4 -f "$proxy_config" "$collector" -u "$user" -d "$domain" \
  -dc "$dc_fqdn" -gc "$gc_fqdn" -ns "$dns_ip" --dns-tcp \
  -c DCOnly --auth-method kerberos --zip
~~~

A TCP DNS flag does not guarantee every resolver/Kerberos/client connection uses the intended proxy. Retain DNS/authentication/method errors and verify archive/import coverage before treating missing objects as absent. Use compatible output paths/generation; a timeout is not an empty directory.

Connect broad edges to the particular operational task:

| Observed relationship | Next decisive evidence |
|---|---|
| GenericWrite over one user | The user DN/SID and current ACE/property rights. A KeyCredentialLink write requires its own permissions and PKINIT environment; a UPN write changes name lookup, not the account SID. Check the selected attribute operation and read-back. |
| DNSAdmins or another nested group | Effective group context and rights on the intended zone/node; an allowed bind can still receive access denied on addition. |
| GPO write permission | The actual GPO GUID, linked OUs/sites/domains, enabled computer/user half, security/WMI filters and inherited/precedence effects. The eventual recipients can include computers beyond the current remote session. |
| Admin-like name or similarly named user | Distinct SAM/UPN/DN/SID. Do not merge `analyst` and `analyst.adm` based on display names. |

Graph collection time and current credential state can differ. Retain successful/failed actions separately from the modeled edge; an unrelated failed machine-account/DNS route does not invalidate a still-supported user attribute route. Finish with the selected rights/path finding and the evidence needed for the next permitted operation, without inventing an entire investigation.

See [collector options](https://github.com/dirkjanm/BloodHound.py/blob/master/bloodhound/__init__.py), [GenericWrite meaning](https://bloodhound.specterops.io/resources/edges/generic-write) and [Group Policy scope](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing).
