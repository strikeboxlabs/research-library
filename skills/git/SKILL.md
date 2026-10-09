---
name: git
description: Inspect historical files and diagnose local Git hook execution. Use when missing history, hook paths, pull outcomes or execution identity complicate a repository investigation.
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


## Diagnose a missing or unexpected local hook

A hosting platform's webhook and a local Git hook are separate events. A deployment endpoint can invoke Git after receiving an HTTP event; that does not make the HTTP event itself a `post-merge` hook.

For the selected trusted repository, inspect configuration and resolve the hook location without pulling:

~~~bash
git -C "$repo" config --show-origin --get core.hooksPath
git -C "$repo" rev-parse --git-path hooks/post-merge
git -C "$repo" config --show-origin --get-regexp '^(pull\.rebase|branch\..*\.rebase)$'
~~~

No matching config value normally returns status 1; distinguish that from a fatal repository error. `core.hooksPath` can replace the default hooks directory. Resolve relative paths in the hook's execution context; for a non-bare repository, Git runs `post-merge` from the worktree root. Inspect the resolved script, executable bit and interpreter as files; finding it does not prove it ran.

Use the actual pull transcript and invocation options to choose the next check:

| Observation (illustrative) | Interpretation and next check |
|---|---|
| `Fast-forward` with changed files | A merge-path update can invoke `post-merge` even without a merge commit. Check the effective path, permissions and hook output. |
| `Already up to date.` | No merge update occurred; do not expect this hook to run or manufacture a repository change to trigger it. |
| Merge conflicts | The failed merge does not invoke `post-merge`; resolve the intended repository operation before diagnosing deployment from that hook. |
| Pull uses rebase | Do not assume merge-hook behavior. Inspect the selected integration mode and its relevant hooks. |

The hook is post-operation: its failure cannot undo the completed merge. Verify the deployed artifact separately from Git's result. A privileged Git invocation can run hooks with that identity, but ownership checks, effective configuration and repository selection must be established first. Do not use `sudo git pull` as a diagnostic probe or globally disable ownership checks.

See [hook events](https://git-scm.com/docs/githooks), [pull integration modes](https://git-scm.com/docs/git-pull) and [hook-path configuration](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corehooksPath) when observed behavior differs.
