---
name: perl
description: Review a Perl backup or file-producing script and check compilation of fully reviewed owned source. Use when imported compile-time code, unchecked child statuses or success messages obscure what actually happened.
---

# Review the script and its producer results

Read this entire SKILL.md before acting. Review acquired source as text first. Compilation below requires fully reviewed owned source, imports and a trusted ordinary interpreter environment; it can execute compile-time code. Finish with compile diagnostics or the supported source-flow finding, and identify missing runtime/artifact evidence separately.

Trace input, interpreter/shebang, imports, effective-ID checks, output paths and every producer call. `use` loads modules during compilation. A call that changes UID is not a setuid file-mode observation; distinguish the call's checked result, file capabilities and already observed process IDs. Do not launch a privileged or capability-bearing interpreter merely to inspect its version or test a script.

For a selected trusted ordinary Perl, define `perl_bin` as its verified invocation and `source` as a bounded fully reviewed owned file whose compile-time effects are authorized. Use a trusted working directory and inspect PERL5OPT/PERL5LIB, include paths and module/startup hooks first:

~~~bash
"$perl_bin" -v
"$perl_bin" -c "$source"
~~~

`-c` checks compilation but runs BEGIN, UNITCHECK and CHECK blocks and imported compile-time code. It is unsuitable for passive inspection of untrusted scripts. A syntax error can coexist with earlier compile-time effects. A missing DBI/module diagnostic is a dependency/context gap, not proof that the deployed producer cannot run. Successful compilation does not execute the ordinary script body or verify its backup behavior.

For `system`, distinguish launch failure, signal termination and encoded child exit status. Zero is not proof that every requested file was included; ignored nonzero status followed by a printed “Completed” is not success evidence. Single-string calls containing shell metacharacters are interpreted through a shell; interpolated paths, globs and suppressed stderr need their actual context. Directory creation/removal and later moves each have their own checked results.

For an archive producer, correlate the exact output name/time, final creation status, archive member listing and subsequent destination. A gzip tar stream can have a .tar suffix; suffixes do not establish format. A later root-owned file with a different generated timestamp is not automatically this invocation's artifact. Source code and a displayed profile file also do not establish the policy loaded on the running process. Keep source interpretation, runtime observations and artifact validation separate.

See [Perl switches and compile-time behavior](https://perldoc.perl.org/perlrun#-c), [system return and shell rules](https://perldoc.perl.org/functions/system) and [special identity/status variables](https://perldoc.perl.org/perlvar).
