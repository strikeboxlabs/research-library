---
name: impacket-gettgt
description: Obtain a Kerberos file credential cache using known credentials with Impacket getTGT. Use when Linux LDAP or SMB clients need a ticket and cache identity, hostname or clock errors interrupt authentication.
---

# Impacket getTGT

Read this entire SKILL.md before acting. Establish the selected account, credential, realm/KDC and fresh cache, then verify the issued principal and validity. For UPN/enterprise-principal mapping, read [enterprise identity selection](references/enterprise-principal.md) fully before requesting the ticket; cache creation alone is not service authorization.

Check `impacket-getTGT -h`; an upstream installation may provide `getTGT.py`. Define `domain` as the AD DNS domain, `user` as the bare account name, `dc_ip` as the DC address, and `ticket_dir` as a new absolute workspace directory.

~~~bash
umask 077
mkdir -m 700 "$ticket_dir" && cd "$ticket_dir" && impacket-getTGT "$domain/$user" -dc-ip "$dc_ip"
~~~

Supply the known password at the prompt. The command requests a TGT and writes `<user>.ccache` in the current directory. Use a fresh directory so an old cache cannot be mistaken for success. The DC address chooses the connection; it does not replace the domain/realm identity.

After the output confirms a new ticket was saved, select the actual file in the shell used by the consuming command:

~~~bash
export KRB5CCNAME="$ticket_dir/$user.ccache"
klist -c "$KRB5CCNAME"
~~~

Verify the default principal, realm, ticket validity times and `krbtgt` entry. Use an absolute filename: relative paths break when a later invocation changes directory. Impacket consumers expect a file path; MIT clients also support cache type prefixes such as `FILE:`, which are not interchangeable with every Impacket version. A separate agent shell may need the export repeated.

When consuming the cache, use the service's FQDN for SPN selection, even if a separate option supplies its IP. A valid TGT proves authentication, not permission to a share or directory object. Check the particular service and principal on access failure.

For preauthentication failure, verify the supplied identity and credential once before retrying. For skew/expiry, inspect actual times; a walkthrough's clock-reset command is not a universal fix. For service-principal errors, check FQDN, realm and DNS canonicalization. Preserve diagnostics: the script can catch an exception without a failing process status.

For option and cache differences, consult [getTGT implementation](https://github.com/fortra/impacket/blob/master/examples/getTGT.py) and [MIT klist](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/klist.html).
