---
name: ldapdomaindump
description: Export an authorized Active Directory inventory with ldapdomaindump. Use when HTML, JSON and tabular reports must retain bind context, attribute coverage and group-versus-description distinctions.
---

# Export a directory inventory

Read this entire SKILL.md before acting; reuse complete current context. Require authorization for the domain-wide inventory, a verified LDAP endpoint/transport, a known bind identity and a fresh private output directory. Check the installed implementation, collect the reports and finish with bind/query status, artifact coverage and unresolved visibility limits.

This CLI queries the discovered default naming context for users, computers, groups, policy and trusts. It is useful when those reports are the requested artifact; use a query tool with a selected base/filter when the task permits only a narrower subtree. Read `ldapdomaindump --help` for the deployed version and select its approved LDAP transport/authentication configuration before sending credentials. An `ldaps://` spelling alone does not establish the client's certificate-validation policy.

Define `identity` as the known `DOMAIN\username` and `endpoint` as the verified directory endpoint. Define `output_dir` as a new absolute directory path under a private parent. With the intended deployed transport policy:

~~~bash
umask 077
mkdir -- "$output_dir" || exit 1
ldapdomaindump -u "$identity" --minimal -o "$output_dir" "$endpoint"
status=$?
~~~

Omitting `-p` requests a password prompt; quoting preserves the identity's backslash. Default password authentication is NTLM in the reviewed upstream CLI; simple bind is a separate choice. A bind success establishes authentication for that connection, not access to every requested attribute.

`--minimal` reduces selected user/computer/group attributes, not the number of objects or the policy/trust queries. It retains useful identity, membership, description and SPN fields in the reviewed implementation. Without format-disabling options, HTML, JSON and greppable reports are enabled. DNS resolution is off by default; `-r` adds resolver traffic and should be selected only when required for the inventory.

Inspect the actual report headers before selecting tab-separated columns: a fixed third-field extraction can identify the wrong value on a different release. Keep full records and distinguish an account's free-text `description` from `memberOf`, primary-group information or creation audit evidence. A label such as “HelpDesk User” is not proof of membership in a security group. Prefer JSON when multivalued attributes or object associations matter.

Require successful bind and process status, inspect query diagnostics and the expected report files, and record their object/attribute coverage. A finished banner does not overcome ACL visibility, absent attributes or incomplete query results. Missing data remains unknown until checked with the same bind context and the intended query. Do not infer login validity or effective permissions from an exported account row.

The upstream [README and implementation](https://github.com/dirkjanm/ldapdomaindump) explain supported formats, authentication and attribute selection; compare them with the installed release when output differs.
