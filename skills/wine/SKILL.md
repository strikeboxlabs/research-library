---
name: wine
description: Run one selected trusted Windows executable with Wine on Linux in an explicit existing prefix. Use when architecture, runtime dependencies, shell quoting or console support makes startup and application output ambiguous.
---

# Selected application in its Wine prefix

Read this entire SKILL.md before acting. Require the trusted executable, reviewed arguments and an existing compatible prefix on the controlled image. Run in that prefix as its ordinary owning user and finish with the application's requested result or specific startup/runtime gap. No conditional resources are required.

Define `prefix` as its initialized absolute Wine-prefix directory, `program` as the approved executable's absolute Unix path, and `program_args` as a Bash array of its actual arguments; an empty array means none:

~~~bash
wine --version
program_args=()
WINEPREFIX="$prefix" wine "$program" "${program_args[@]}"
status=$?
~~~

Keep the selected architecture/dependencies and application version with its result. Pass Windows-path arguments as literal quoted arguments; the shell's backslash processing is distinct from Wine's path mapping. Capture stderr separately from stdout when collecting machine-readable output; diagnostic text is not application data. Check completeness as well as status before consuming an artifact.

An omitted WINEPREFIX uses the default user prefix, potentially changing unrelated applications' registry/runtime state. Prefix selection separates Wine state, not host filesystem or network permissions; it is not a sandbox for unknown executables. Changing WINEARCH does not convert an existing prefix's architecture. A missing DLL/.NET dependency or architecture mismatch requires resolving that application/prefix contract, not blanket installation or suppression of diagnostics.

An application printing a filter then a directory error does not identify Wine as the cause. Retain the application/framework, prefix and Wine versions, and separate provider startup, bind and subsequent search results. A captured successful LDAP bind followed by `noSuchObject` supports checking the actual search base and request, not declaring LDAP unsupported. Requested API flags can differ from the observed provider exchange; use existing redacted capture evidence before changing dependencies or credentials.

Wine provides limited console support through this invocation. If a program needs an interactive Windows console, consult the installed wineconsole interface instead of assuming a plain redirected invocation supplies one. Finish with the requested application output; launching an executable does not prove its external action succeeded.

See the [packaged Wine manual](https://manpages.debian.org/bookworm/wine/wine.1.en.html) for prefix, architecture and argument behavior.
