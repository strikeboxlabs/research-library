# Enterprise principal requests and identity mapping

Use this when the requested name differs from the account's SAM name/UPN, or a controlled assessment explicitly tests writable UPNs across AD and Linux Kerberos services. A normal `NT_PRINCIPAL` request and an `NT_ENTERPRISE` request can resolve the same string differently at the KDC. This is not offline ticket generation: the KDC authenticates the actual account and issues a TGT.

Require the exact affected account DN/SID, present SAM name/UPN, relevant write permission, selected comparison identity and credential, KDC, intended Linux service and a restoration plan for any attribute change. Capture the current attribute before the write. Do not infer write rights or account equivalence from a graph's `GenericWrite` label alone.

After a separately approved UPN change has been read back, define `enterprise_name` as that observed value, `domain` as the actual AD DNS realm and `dc_ip` as the selected KDC. In a new private directory:

~~~bash
umask 077
mkdir -- "$ticket_dir" && (
    cd -- "$ticket_dir" || exit
    impacket-getTGT -principalType NT_ENTERPRISE -dc-ip "$dc_ip" "$domain/$enterprise_name"
)
~~~

Enter the known credential for the **account to which the UPN resolves**, not a guessed credential for the displayed comparison name. A matching NT hash can instead be supplied with this build's `-hashes LM:NT` option; that exposes key material to process inspection. Use the full `-principalType` option; an abbreviated `-principal` in an old transcript is not a portable command spelling.

Inspect the exact reported cache filename in this directory, then:

~~~bash
klist -c "$cache"
export KRB5CCNAME="$cache"
~~~

Check its principal, realm, validity and `krbtgt` ticket. Do not construct the filename from the intended impersonated user's name. Keep original account SID, requested UPN, issued ticket name and subsequent service identity as separate evidence.

The documented mixed-stack issue concerns a service that maps the Kerberos client name through Linux name service/user authorization while not using the original AD SID/PAC identity equivalently. Windows SSPI and a particular MIT/Heimdal GSSAPI application need not authorize the same account from this ticket. A ticket whose displayed name resembles another user is not proof every Linux service accepts it as that user. The server's mapping rules, account allow lists and application behavior decide the outcome.

Test only the intended known service, retaining its authentication method and **remote** account/UID/group result. Authentication refusal, unexpected local mapping and a permission denial after authentication are distinct. A successful SSH login still does not establish sudo/root authority. Restore the original UPN and read it back even if the login failed; issued caches remain sensitive artifacts after the attribute is restored.

See [getTGT principal-type parsing](https://github.com/fortra/impacket/blob/master/examples/getTGT.py) and the primary [mixed-vendor Kerberos analysis](https://www.pentestpartners.com/security-blog/a-broken-marriage-abusing-mixed-vendor-kerberos-stacks/) for the affected mapping model, rather than treating an arbitrary UPN edit as universal impersonation.
