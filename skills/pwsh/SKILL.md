---
name: pwsh
description: Inspect acquired PowerShell source and JEA configuration files offline, or interpret captured AD replication ACE evidence. Use to separate syntax, role declarations and individual access-control entries from effective permissions.
---

# PowerShell source inspection on Linux

Read this entire SKILL.md before acting. For a bounded acquired source file, require trusted installed PowerShell and use the required [source parser](scripts/inspect-source.ps1) below. For PSSC/PSRC or JEA evidence, also read [JEA configuration interpretation](references/jea-configurations.md) fully. For captured AD replication ACE records, read [replication rights evidence](references/replication-rights-evidence.md) fully; that data review does not require importing an AD module. Finish with input identity, selected source/permission evidence and unresolved binding, token or deployment facts.

Define `pwsh_bin` as the verified installed executable, `parser` as this package's absolute `scripts/inspect-source.ps1` path, `source_file` as the selected absolute input path and `result` as a fresh private output file:

~~~bash
"$pwsh_bin" -Version
umask 077
"$pwsh_bin" -NoLogo -NoProfile -NonInteractive -File "$parser" -SourcePath "$source_file" > "$result"
~~~

Check status immediately: the helper returns zero for parsed input, one for syntax errors and two for an input/parser exception. Its JSON preserves line numbers and diagnostics; an empty node list can still be valid parsed source. Read the original surrounding statements before interpreting a located name. `searchNestedScriptBlocks` is enabled, so a call inside a function or configuration script block is included even when that block never ran.

The helper locates `CommandAst` and `FunctionDefinitionAst` nodes, not every effect. A dynamic command name can be null; aliases, module qualification, shadowed names and generated code need the actual binding context. Parsed commands are source observations, not invocation history. A valid AST does not validate a PSSC schema, external dependencies, application logic or the security of a handler. Parsing very large input can consume substantial resources; select a bounded artifact first.

`-NoProfile` avoids PowerShell profile startup; it is not a sandbox for a script passed to `-File`. Here `-File` executes the trusted package helper, whose parser reads the acquired input. Do not dot-source, import or run that input to inspect it. Preserve source encoding and bytes; a historical Python or shell wrapper around PowerShell can have separate startup and quoting behavior.

An installed Linux pwsh alone does not establish WSMan remoting capability. Microsoft's current support guidance excludes WSMan remoting on non-Windows platforms; a historical `New-PSSession -ComputerName` transcript requires its actual client/dependency context. An SSH transport is a different endpoint and cannot be assumed to expose the same JEA policy. Record that gap instead of adding packages or changing TrustedHosts/listeners to imitate an old recipe.

References: [parser API](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parsefile), [nested AST search](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.ast.findall), [pwsh startup options](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pwsh), and [WSMan platform support](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/wsman-remoting-in-powershell).
