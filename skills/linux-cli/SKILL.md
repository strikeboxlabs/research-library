---
name: linux-cli
description: Investigate native Linux crashes and existing core dumps with GDB. Use for SIGSEGV or SIGABRT crashes, stack traces, missing symbols, and inconclusive backtraces when a core dump and executable are available. Covers offline core analysis and evidence-driven follow-up.
---

# Linux CLI investigations

Requires Linux with file access and shell command execution. Tool-specific requirements are listed in each reference.

Use the [tool index](references/index.md) to select guidance matching the user's question. Search by executable, alias, or symptom. The tier identifies a full procedure (A), a short correction to familiar usage (B), or an index entry with no card (C). Read only the relevant reference. Resolve paths relative to this installed skill directory.

For the current starter, [GDB](references/gdb.md) covers examining an existing native core dump. If the question lies outside indexed coverage, use available authoritative documentation and make the coverage limit clear.

Read [runtime guidance](references/runtime.md) when command execution, output handling, or session requirements are uncertain. Check only the prerequisites that affect the selected procedure.

Use the procedure as an adaptable investigation:

1. Identify the question and the evidence the chosen tool can provide.
2. Run the relevant command with actual, defined inputs.
3. Interpret the result within its recorded limits and select a next check that can change the conclusion.
4. Finish with the supporting evidence or the specific missing capability/artifact that prevents an answer.

Use each reference's verification record to distinguish documented guidance from executed cases. A successful command is one observation; it does not establish that the user's problem is understood or resolved.

Each card links to a provenance companion. Read it when checking a claim, resolving a version conflict, or maintaining the reference; ordinary use does not require loading the source list.
