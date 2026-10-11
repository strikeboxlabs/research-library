---
name: vim
description: Use Vim for file inspection, vi-style literal substitutions and copied swap recovery with controlled startup. Use when modelines, plugins, swap ownership or incomplete recovery make an ordinary editor launch inappropriate.
---

# Separate inspection from recovery

Read this entire SKILL.md before acting. Select inspection, copied-swap recovery or the controlled substitution below, using fresh output paths and controlled startup. Finish with the actual recovered/edited content and any unresolved coverage/format gap.

Record `vim --version`, including patches and build features. A command named `vi` need not be Vim; establish the implementation before using these startup flags. A historical modeline vulnerability does not establish that every current package is affected; distribution backports also matter. Avoid loading source-provided editor configuration or plugins to inspect a document.

Define `artifact` as an existing absolute working-copy path. For inspection:

~~~bash
vim -Nu NONE -i NONE -n -M --cmd 'set nomodeline' -- "$artifact"
~~~

`-u NONE` skips startup configuration/plugins, `-i NONE` avoids viminfo, and `-n` disables swap creation. `--cmd` sets `nomodeline` **before** reading the file. An ordinary `-c` command runs later. `-M` disables modification/writing initially; `-R` alone is only read-only mode and can be overridden. These settings do not turn Vim into a security sandbox or stop explicitly requested shell commands.

For a found `.swp`/`.swo`, first determine whether the original editor is still running. Vim normally maintains a swap during editing; its existence alone does not establish a crash or unsafe exit. Its recorded user, host, PID and filename are recovery clues, not proof of current ownership or a current process on this machine. Do not delete a swap merely because Vim reports it. Preserve both the swap and any original file available from the same capture.

Recover a **copy** in a scratch directory. Start an empty editor with controlled startup:

~~~bash
vim -Nu NONE -i NONE -n --cmd 'set nomodeline'
~~~

At the Vim command prompt, use `:recover /absolute/path/to/copied.swp`, substituting the actual copied swap path. Inspect the recovered buffer before `:write /absolute/path/to/fresh-output`; use a new output name and no forced overwrite. Record any request for a missing original file and any recovery diagnostics. Some unchanged blocks may depend on the original file, so an isolated swap does not guarantee complete recovery.

Search the recovered buffer for Vim's `???` recovery markers, inspect suspicious boundaries and compare against the captured original where available. Marker absence alone does not prove completeness. `strings` output from a swap is useful triage but does not reconstruct edit order or the complete buffer. Report recovered content and missing/corrupt regions separately.

## Replace a verified presentation token in a working copy

For an intentionally editable copy, use the same controlled startup without `-M`. Preview a literal token's occurrences with `:%s/&#34;/"/gn`, then use `:%s/&#34;/"/gc` to confirm each replacement and `:write /absolute/path/to/fresh-output` to preserve the original. `g` visits all matches per line, `n` counts without replacing, and `c` requests confirmation. This exact token is HTML's decimal quote entity; replacing it alone is not general HTML decoding, JSON parsing or validation. Do not apply it blindly inside nested JSON string data or to content already decoded by a browser. Use the actual serialization parser when other entities/escaping layers occur, then validate the complete destination format.

Sources: [startup](https://github.com/vim/vim/blob/master/runtime/doc/starting.txt), [modelines](https://github.com/vim/vim/blob/master/runtime/doc/options.txt), [recovery](https://github.com/vim/vim/blob/master/runtime/doc/recover.txt), [substitution flags](https://github.com/vim/vim/blob/master/runtime/doc/change.txt).
