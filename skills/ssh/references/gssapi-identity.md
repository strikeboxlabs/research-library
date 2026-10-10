# Kerberos/GSSAPI login and the resulting Linux identity

Use when an existing TGT should authenticate a selected OpenSSH connection, or when AD and Linux map the authenticated name differently. Require a GSSAPI-capable client/build, intended server FQDN and verified host key, valid selected credential cache, working realm/DNS and server GSSAPI/account policy. The OpenBSD manual and Linux portable builds can differ in GSSAPI options; inspect the installed build.

Select the actual cache, then use explicit authentication/delegation policy:

~~~bash
export KRB5CCNAME="$cache"
klist -c "$KRB5CCNAME"
ssh -v -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=no \
  -o PreferredAuthentications=gssapi-with-mic "$login_user@$server_fqdn"
~~~

`login_user` is the requested remote Linux account, not automatically the principal printed in the cache. `PreferredAuthentications` keeps a diagnostic GSSAPI attempt from silently succeeding via an unrelated password/key method. Keep host-key validation and inspect the actual authentication message; debug logs can contain sensitive names/routes.

In supporting portable builds, `ssh -K` both enables GSSAPI authentication **and delegates credentials**. It is not just shorthand for using the local ticket. Delegate only for an explicitly needed remote onward-authentication task with that host trusted to receive the credentials. A successful session without delegation can be enough to establish the mapping result.

Once connected, inspect `whoami`, `id` and the requested operation's real permission. A Kerberos client-name mapping through NSS/SSSD can differ from Windows SID/PAC-based authorization in a particular mixed-stack deployment. A changed UPN or a cache name resembling an administrator is not a universal Linux authorization bypass; server allow lists, account mapping and application policy still apply. Sudo authority is separate from SSH authentication.

If the server rejects the principal, preserve whether failure was at service-ticket acquisition, SSH GSSAPI authentication or account authorization. Verify FQDN/SPN, cache expiry, clock and mapping policy before requesting new credentials. Do not enable fallback/delegation merely to hide that distinction. Close the selected session after the requested evidence is obtained. See [portable GSSAPI option handling](https://github.com/openssh/openssh-portable/blob/master/ssh.c) and [mixed-vendor name mapping](https://www.pentestpartners.com/security-blog/a-broken-marriage-abusing-mixed-vendor-kerberos-stacks/).
