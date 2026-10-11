---
name: named-checkconf
description: Check a selected BIND configuration and included files with named-checkconf. Use to distinguish syntax acceptance, optional primary-zone loading and actual service reload success.
---

# Check a selected BIND configuration

Read this entire SKILL.md before acting. Select the actual configuration and its include/path context; finish with checker status and the precise scope checked. Missing includes or a different root directory remain unresolved prerequisites.

Define `config` as the existing absolute configuration path:

~~~bash
named-checkconf -v
named-checkconf "$config"
~~~

Exit status zero indicates no error detected by this syntax check, including parsed includes. It does not establish runtime policy, reachability or a successful reload. Capture diagnostics on failure; suppressed stdout alone is insufficient.

If the selected task requires loading all configured primary zones and their files are available:

~~~bash
named-checkconf -z "$config"
~~~

This expands validation scope; it does not start or restart named. A matching chroot can require `-t` with its actual directory. Files parsed separately, such as rndc configuration, are not automatically covered. Configuration printing with `-p` can expose secrets; `-p -x` obscures shared secrets when a canonical representation is specifically needed.

Retain the invocation, input context and status before a separate deployment decision. Consult the installed version and [BIND manual](https://bind9.readthedocs.io/en/stable/manpages.html#named-checkconf-named-configuration-file-syntax-checking-tool).
