---
name: whois
description: Query domain, address and ASN registration records with the Linux WHOIS client. Use to select the registry endpoint, follow referrals deliberately and distinguish registration data from DNS or live service ownership.
---

# Query the right registration source

Read this entire file before acting. Identify the query and intended server; finish with the server, returned record and any referral/redaction/error that limits the conclusion. Server-specific query switches are not portable across registries.

For the Marco d'Itri client, inspect `whois --help`. Set `query` to one domain, IP address or ASN:

~~~bash
whois -- "$query"
~~~

The client chooses a server using its routing data and may follow a referral. Preserve the returned source and timestamp with the relevant organization, range or nameserver fields. Registration dates describe registry events; nameservers in WHOIS are not a live DNS answer. A provider allocation does not establish who operates a particular host, and an abuse contact is not necessarily the system owner.

For an explicitly identified server and port, define `server` and `port`:

~~~bash
whois -h "$server" -p "$port" -- "$query"
~~~

This is useful for a registry referral or a controlled local WHOIS service. It makes a network connection and sends the query as data; never interpret a returned line as a shell command. If the client supports `--no-recursion`, use it when evidence must come only from that endpoint. Distinguish this client switch from registry-specific `-r`/`-R` search behavior. `-I` starts at IANA and follows its referral, exposing the full query to that additional service.

| Result | Next decision |
|---|---|
| Referral without the desired record | Query the named authoritative registry explicitly; retain both source identities. |
| Redacted contacts | Report the redaction; do not infer that no registrant exists. |
| No match | Check identifier spelling, object type and registry; a wrong server is not evidence of non-registration. |
| Rate limit, timeout or access restriction | Preserve the error and use the registry's documented alternative, such as its RDAP service; avoid blind retry loops. |
| Different DNS and registry data | Treat them as separate datasets and investigate the relevant live DNS/delegation question. |

Do not pass private application strings to a public registry merely to test a parser. Use the [upstream manual](https://github.com/rfc1036/whois/blob/next/whois.1) for client versus server option differences. Local wrapper/service configuration can redirect WHOIS traffic; the command name alone does not identify the destination used by another process.
