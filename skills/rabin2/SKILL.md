---
name: rabin2
description: Inspect acquired binary sections and segments with radare2's rabin2. Use when physical offsets, virtual addresses or declared permissions are confused with live memory mappings.
---

# Inspect the binary's declared layout

Read this entire SKILL.md before acting. Require the acquired file and intended format/architecture. No conditional resources are required. Finish with status and selected layout evidence; static metadata does not establish live access.

Confirm `rabin2 -v` and `rabin2 -h`. Define `binary` as the working copy:

~~~bash
rabin2 -I "$binary"
rabin2 -S "$binary"
rabin2 -SS "$binary"
~~~

Keep diagnostics/status for each query. `-I` reports binary information, `-S` sections and `-SS` segments. Select the actual sub-binary when inspecting a multi-architecture container. Do not force a format to hide a parser failure.

Keep paddr/file size separate from vaddr/virtual size and declared permissions. A PIE's static virtual address is not its current runtime address. Section names alone do not establish loaded protection; compare relevant segment mapping and acquired process context. Abbreviated rows cannot prove whole-file coverage. Use supported `-j` for structured output without assuming one release's fields.

Source: [rabin2 manual](https://raw.githubusercontent.com/radareorg/radare2/master/man/rabin2.1).
