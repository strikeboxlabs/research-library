---
name: more
description: Page through one selected Linux text file with util-linux more. Use when terminal pagination, search, an early quit or a pipe makes displayed content coverage uncertain.
---

# Read the selected text file

Read this entire SKILL.md before acting. Require a readable selected text artifact and an interactive terminal for paging. Finish with the requested content and actual coverage or read failure; quitting the pager is not proof that the whole file was read. No conditional resources are required.

Check `more --version` and help for util-linux. Windows more is a different implementation; do not copy its switches here. Define `text_file` as the selected absolute path and account for existing MORE option settings:

~~~bash
MORESECURE=1 more -- "$text_file"
~~~

On builds supporting MORESECURE, this disables shell/editor escapes; it does not sanitize terminal control characters or make an arbitrary binary safe to display. Use a suitable escaped/byte view when the artifact's contents or encoding are uncertain.

Space advances a screen, Return advances a line, `/pattern` searches a regular expression and `n` repeats the search. `:f` identifies the current file/line; `q` quits. A skipped page or search hit leaves intervening content unreviewed. Backward paging works on files, not pipes in this implementation. A truncated upstream pipe cannot be repaired by continuing the pager.

Preserve read diagnostics and distinguish reaching EOF from an early quit. Nonterminal output may pass content through without interactive prompts; redirecting output is not evidence of a human review. Paging neither validates a configuration nor executes the displayed source.

See [util-linux more manual](https://github.com/util-linux/util-linux/blob/master/text-utils/more.1.adoc) for installed-version behavior and secure-mode support.
