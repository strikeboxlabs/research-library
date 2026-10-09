---
name: git
description: Inspect a file's Git history and recover historical content without changing the checkout. Use when removed configuration, renames or shallow history complicate repository investigation.
---

# Git historical file inspection

Use an existing trusted repository or an isolated evidence copy. Define `repo` as its absolute path and `path` as one repository-root-relative file path:

~~~bash
git -C "$repo" status --short
git -C "$repo" rev-parse --is-shallow-repository
git -C "$repo" --no-pager log --all --follow --format='%H %ad %s' --date=iso-strict -- "$path"
~~~

`--follow` follows one file across detected renames, not an entire directory. `--all` traverses locally available refs, not every remote commit or deleted unreachable object. Shallow/partial clones can limit results; a partial clone may fetch missing objects on demand. Record the repository state before treating an empty history as evidence that content never existed.

Choose `revision` from an observed commit and `historical_path` as the path at that revision, which can differ after a rename. Define `output_file` as a fresh private destination:

~~~bash
umask 077
git -C "$repo" show "$revision:$historical_path" >"$output_file"
~~~

This reads a blob without checking out the old revision, changing branches or disturbing uncommitted files. Verify exit status and output before using it. A missing path can mean the file was renamed/deleted at that commit; inspect the parent or the commit's path changes rather than assuming the repository is corrupt.

For changes to the chosen path, use `git -C "$repo" --no-pager log -p --no-ext-diff --no-textconv -- "$path"`. External diff/text-conversion helpers can execute configured programs; the explicit flags keep that comparison textual. Large/binary files need a format-specific reader after extraction.

A historical secret proves it was stored at that revision, not that it is currently valid. Keep sensitive content out of routine reports. If ownership checks reject a repository, inspect ownership/trust first; do not set `safe.directory '*'` to bypass the check globally. Report commit ID, historical path and history limitations with the finding.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Ambassador pp. 11–13. Sources: [git log](https://git-scm.com/docs/git-log), [git show](https://git-scm.com/docs/git-show), [safe.directory](https://git-scm.com/docs/git-config#Documentation/git-config.txt-safedirectory).
