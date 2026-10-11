---
name: checksec
description: Inspect an existing ELF's mitigation metadata with the pwntools checksec CLI. Use to distinguish NX, PIE, RELRO and canary indicators from host ASLR, runtime identity and proof of memory safety.
---

# Inspect ELF mitigation indicators

Read this entire SKILL.md before acting. This procedure uses the installed **pwntools** `pwn checksec` subcommand on an existing local artifact; standalone programs also named checksec have different argument syntax. Identify the implementation before invoking it. Finish with artifact/build identity, command status and the reported indicators, including any unreadable or unsupported fields.

Define `binary` as an existing absolute ELF path. Retain its fingerprint and source/build association. Inspect the available subcommand and then the selected file:

~~~bash
pwn checksec --help
pwn checksec "$binary"
~~~

This inspects the ELF rather than starting its program. A failure to parse it is an artifact/tool-support problem, not evidence that protections are disabled. Do not use a similarly named executable to obtain a successful-looking report.

| Reported field | Supported interpretation |
|---|---|
| NX enabled | The inspected ELF advertises a non-executable stack; it does not establish every runtime mapping or absence of memory corruption. |
| Canary found | A recognizable stack-protector indicator exists; this does not establish that every function is protected. |
| PIE / No PIE | Position-independent executable metadata, separate from the running host's ASLR policy and a particular process's observed mappings. |
| Partial / Full RELRO | Reported relocation-protection metadata, separate from proof that the application handles untrusted input safely. |

A report for a static executable still says nothing about successful setuid transitions. File mode, mount conditions, tracing and the actual process identity are separate evidence. If the question concerns a crash or a live address, obtain matching runtime/core state rather than deriving it from this report.

Resolve syntax and field behavior with the installed help and the pwntools [command-line documentation](https://docs.pwntools.com/en/stable/commandline.html#pwn-checksec) and [ELF API](https://docs.pwntools.com/en/stable/elf/elf.html#pwnlib.elf.elf.ELF.checksec). A historical `checksec file` alias in a transcript does not establish the current standalone tool's grammar.
