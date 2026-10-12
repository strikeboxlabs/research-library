---
name: klist
description: Inspect a selected MIT Kerberos credential cache from Linux. Use to verify principal, realm, service and expiry before a client login, without confusing a cached ticket with application authorization.
---


# Inspect the actual cache used by the consumer

Read this entire SKILL.md before acting. Identify the cache implementation/type and current client environment. Finish with principal, service, validity and the selected cache path; inspection alone does not validate target acceptance or authority.

For a known MIT file cache, define `cache` as its existing absolute path:

~~~bash
klist -c "$cache"
~~~

Check `Default principal`, realm, validity times and server names. `krbtgt/REALM@REALM` is a TGT; `cifs/host` or `host/host` is a service ticket. A service-only cache does not automatically allow requests for unrelated services. A future/expired ticket needs real time evidence, not a copied clock-change command.

When the selected consumer requires particular ticket flags, inspect that same cache explicitly:

~~~bash
klist -f -c "$cache"
~~~

MIT's `F` flag means forwardable; `f` means forwarded. A plain listing without flags, or a copied `kinit -f` request, does not prove the issued ticket has the required flag. Defaults can depend on configuration and the KDC can restrict requests. Record flags for the actual relevant ticket; they do not establish delegation rights or service authorization. Check installed help when a different Kerberos implementation renders them differently.

A bare klist examines the default cache chosen by this shell/environment. Export `KRB5CCNAME="$cache"` in the actual consuming process's shell if that is its supported selection method. Absolute filenames survive directory changes. MIT typed names such as `FILE:/path` and collection caches are not supported identically by every Python/Impacket consumer; use the representation that consumer accepts.

`klist -s -c "$cache"` is a silent status check for the selected cache; read its exit status. It is not an online service authorization test. Keytab inspection is a different mode (`-k`); avoid `-K`, which prints key material, when only entry metadata is needed. Do not diagnose a permission denied service as an invalid cache solely because authentication metadata looks unusual.

See [MIT klist](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/klist.html).
