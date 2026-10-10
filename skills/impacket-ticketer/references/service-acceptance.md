# Use a generated service ticket for the selected service

This follows generation/inspection in the entrypoint, using the service account's actual key and explicitly approved client identity/groups. It is a forged service-ticket test (often called a silver ticket), not KDC issuance of an enterprise-principal TGT. A machine account key can serve an SPN belonging to that account; it does not sign every service in the domain. RC4/AES acceptance and PAC validation depend on the actual service/policy.

For an explicitly supplied NT key rather than the entrypoint's keytab, the generation inputs are:

~~~bash
impacket-ticketer -spn "$spn" -nthash "$service_nt" -domain "$domain" \
  -domain-sid "$domain_sid" -user-id "$user_rid" -groups "$group_rids" \
  -duration 1 "$test_user"
~~~

The key argument is exposed to local process inspection. Defaults for RID/groups/lifetime are not the selected task's authority; supply the reviewed values. A source that leaves them implicit may generate more privilege/lifetime than its visible username suggests.

After locating and inspecting the newly saved cache, export its absolute path in the consuming shell. For an SMB/CIFS ticket, use the selected host's actual FQDN so the client requests the same SPN:

~~~bash
export KRB5CCNAME="$cache"
impacket-smbclient -k -no-pass -dc-ip "$dc_ip" "$domain/$test_user@$service_fqdn"
~~~

In the resulting client, `shares`, `use <selected-share>` and a selected listing/read test progressively establish access. `-no-pass` prevents a password prompt; verify actual cache use and the intended service. A numeric network address can be supplied through supported target-IP controls when needed, while keeping the hostname/SPN unchanged.

A service may reject an otherwise structurally valid ticket for key, encryption, SPN, time, PAC or account policy reasons. Preserve the failure stage without widening identities/groups or silently adding another credential. A successful authenticated SMB action is not automatically permission for WinRM, SCM or domain replication. If the selected follow-on task is remote credential acquisition, treat its effects/scope separately from ticket generation.

Finish with generated fields, actual target/service operation and observed authorization. Keep service keys/caches private and account for their lifetime; removing a local cache does not revoke a service key. See [ticketer fields](https://github.com/fortra/impacket/blob/master/examples/ticketer.py) and [SMB cache consumer](https://github.com/fortra/impacket/blob/master/examples/smbclient.py).
