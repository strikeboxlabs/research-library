---
name: msfconsole
description: Use Metasploit Framework modules, jobs and sessions from the Linux console. Use for module selection, configured checks, scoped auxiliary runs and matching a lab handler to an existing payload.
---

# Select and configure a Framework module

Read this entire SKILL.md before acting; reuse complete current context. Require the trusted installed Framework, selected permitted module task and explicit endpoint/observation scope. For handlers and session lifecycle, read [handlers and sessions](references/handlers-and-sessions.md) fully before that task; other console tasks use this entrypoint. Finish with the module/options used, its observed result and remaining jobs/sessions; loading a module is not executing it successfully. Missing module behavior, prerequisites or result evidence remains unresolved.

Start `msfconsole -q`. Review startup resources and global datastore values in an existing workspace; old global target/credential settings can affect a new module. A database is useful for organizing results but is not required for every console module.

`-r` selects a resource script whose commands are executed, rather than a report or inert RCE file. Review the selected file, included Ruby and its referenced modules/options before loading it; a generated filename does not prove listener settings, architecture or permitted effects. Retain acquisition/configuration evidence separately from execution and session identity. Do not load an acquired resource merely to inspect its contents. See [resource scripts](https://help.rapid7.com/metasploit/Content/general/resource-scripts.html).

For an **illustrative** authorized HTTP-version check on a lab endpoint:

~~~text
search type:auxiliary name:http_version
use auxiliary/scanner/http/http_version
info
show options
set RHOSTS 192.0.2.10
set RPORT 8080
set THREADS 1
show options
run
~~~

Replace the address/port with the actual selected endpoint. `RHOSTS` can accept ranges/files, so verify its final value even for a one-host task. Inspect `show advanced` when routing, TLS, timeouts or request behavior differs from the basic options. Confirm the module's SSL/virtual-host settings when the application requires them.

`info` provides the module's purpose, references and supported targets/actions. For an exploit module, inspect `show targets`, `show payloads` and all required options before choosing them. `check` is available only for modules implementing it, can send consequential requests and is not a universal passive or conclusive test. Read what that module checks. A version banner alone does not establish exploitability or matching target architecture.

Use `set` for module-local values. `setg` persists global values across module changes; `unsetg` clears a specific global when it no longer applies. `back` leaves module context without necessarily stopping background work. `spool PATH` records console output until `spool off`; select a private path because sessions and options may contain secrets.

Use [running modules](https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html) and [Framework documentation](https://docs.rapid7.com/metasploit/msf-overview/) for console behavior and module-specific references.
