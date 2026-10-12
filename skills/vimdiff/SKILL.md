---
name: vimdiff
description: Compare two acquired text files side by side with Vim diff mode and controlled startup. Use when a changed function, hidden context or ignored whitespace obscures what a source comparison establishes.
---

# Inspect both sides of a source difference

Read this entire SKILL.md before acting. Require two identified existing absolute text-file working copies and their source/revision identities. All instructions are inline. Finish with the relevant differences and surrounding context, retaining missing-file, decoding or comparison limits; this does not establish which source built a deployed binary.

Check `vimdiff --version` for Vim and its `+diff` feature. Define `left` and `right` as the two working copies:

~~~bash
vimdiff -Nu NONE -i NONE -n -M --cmd 'set nomodeline' -- "$left" "$right"
~~~

If only the Vim executable exists, use `vim -d` with the same arguments. `-u NONE` skips configuration/plugins, `-i NONE` avoids viminfo, `-n` avoids swap creation and `-M` initially disables changes/writes. The early command disables modelines before file loading. These settings are not a sandbox and can be changed explicitly inside Vim.

Use `:args` to confirm both filenames actually loaded; a nonexistent operand may become an empty buffer rather than a valid acquired file. `Ctrl-W w` changes windows, `[c`/`]c` moves between changes and `zo` opens folded unchanged context. The aligned display compares loaded buffers; filler lines are alignment placeholders. Inspect `:set diffopt?`: whitespace/case-ignore options can conceal differences. Decoding and line-ending normalization also mean a visually equal text comparison is not a byte-identity check.

Read the enclosing function and other relevant call sites on both sides. Removing one prefork loop does not establish that request handlers contain no other fork calls. A current upstream checkout is not automatically the historical revision corresponding to an acquired binary. If a file changed externally, establish the intended capture before reloading; stale buffers are not a comparison of current disk contents.

Retain left/right identities, relevant changed statements and remaining calls that qualify the conclusion. Exit with `:qa!` after inspection. Diff merging or writing files requires a separate editing task.

Sources: [Vim diff viewing/navigation](https://vimhelp.org/diff.txt.html), [Vim startup options](https://vimhelp.org/starting.txt.html).
