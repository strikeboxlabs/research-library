---
name: vim
description: Inspect files and recover copied Vim swap artifacts with controlled startup. Use when modelines, plugins, swap ownership or incomplete recovery make an ordinary editor launch inappropriate.
---

# Separate inspection from recovery

Record `vim --version`, including patches and build features. A historical modeline vulnerability does not establish that every current package is affected; distribution backports also matter. Avoid loading source-provided editor configuration or plugins to inspect a document.

Define `artifact` as an existing absolute working-copy path. For inspection:

~~~bash
vim -Nu NONE -i NONE -n -M --cmd 'set nomodeline' -- "$artifact"
~~~

`-u NONE` skips startup configuration/plugins, `-i NONE` avoids viminfo, and `-n` disables swap creation. `--cmd` sets `nomodeline` **before** reading the file. An ordinary `-c` command runs later. `-M` disables modification/writing initially; `-R` alone is only read-only mode and can be overridden. These settings do not turn Vim into a security sandbox or stop explicitly requested shell commands.

For a found `.swp`/`.swo`, first determine whether the original editor is still running. Its recorded user, host, PID and filename are recovery clues, not proof of current ownership or a current process on this machine. Do not delete a swap merely because Vim reports it. Preserve both the swap and any original file available from the same capture.

Recover a **copy** in a scratch directory. Start an empty editor with controlled startup:

~~~bash
vim -Nu NONE -i NONE -n --cmd 'set nomodeline'
~~~

At the Vim command prompt, use `:recover /absolute/path/to/copied.swp`, substituting the actual copied swap path. Inspect the recovered buffer before `:write /absolute/path/to/fresh-output`; use a new output name and no forced overwrite. Record any request for a missing original file and any recovery diagnostics. Some unchanged blocks may depend on the original file, so an isolated swap does not guarantee complete recovery.

Search the recovered buffer for Vim's `???` recovery markers, inspect suspicious boundaries and compare against the captured original where available. Marker absence alone does not prove completeness. `strings` output from a swap is useful triage but does not reconstruct edit order or the complete buffer. Report recovered content and missing/corrupt regions separately.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended pp. 8–9, 15. Sources: [startup](https://github.com/vim/vim/blob/master/runtime/doc/starting.txt), [modelines](https://github.com/vim/vim/blob/master/runtime/doc/options.txt), [recovery](https://github.com/vim/vim/blob/master/runtime/doc/recover.txt).
