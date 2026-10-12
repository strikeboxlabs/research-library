---
name: ksu
description: Switch to an explicitly authorized local Linux account with MIT ksu. Use to distinguish Kerberos authentication, local account authorization and the target session's ticket cache.
---

# Verify an authorized account transition

Read this entire SKILL.md before acting; reuse complete current context. Require installed MIT ksu, a known principal/cache, an explicitly permitted nonprivileged target account and the host's established Kerberos authorization policy. Perform the requested transition, verify the child identity, then exit and account for the target cache or report the precise failed stage.

Inspect the installed help and actual host policy. A TGT authenticates a principal; it does not authorize every local account. Shell access can depend on the target's `.k5login`, `.k5users` or configured principal-to-login mapping. A PAM `ignore_k5login` setting alone does not establish ksu's authorization result. Missing host principal/keytab or unusable cache is a prerequisite gap, not a reason to modify authorization files.

Define `target_user` as the permitted local account, `principal` as the exact authorized Kerberos principal and `cache_path` as the existing private MIT FILE cache. Always supply the account: omitted target defaults to root. For a session that needs no copied tickets:

~~~bash
ksu "$target_user" -n "$principal" -c "FILE:$cache_path" -Z
~~~

Inside the resulting shell, run `id` to retain real/effective UID and groups, then `exit`. Separate authenticated-principal, account-authorization and actual child-identity evidence. Invoking as root or selecting the source account bypasses ordinary authentication/authorization checks, so it is not a meaningful test of a different user's access.

`-Z` creates a target cache without copying source tickets; ordinary invocation can copy credentials. Without `-k`, ksu removes its target cache after the child exits; the source cache is separate and may have expired tickets removed. Check actual completion rather than assuming a lost terminal cleaned everything up.

`-e command` has a distinct command authorization path through `.k5users`; successful shell authorization does not guarantee it. Resolve the intended policy instead of substituting execution modes to bypass a denial. Password fallback depends on the build and needs a secure channel. See [MIT ksu authentication, authorization and cache semantics](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/ksu.html).
