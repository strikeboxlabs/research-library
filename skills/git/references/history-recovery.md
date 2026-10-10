# Recover selected historical content without changing the worktree

Use this when removed/replaced content, a misleading diff or incomplete history matters. A commit message about an accidental key is a lead; inspect both endpoints and retain the actual blob identity. Never infer present authentication rights from stored private-key bytes.

Define `repo` as its absolute path and `path` as one repository-root-relative file path:

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

When a known code line remains but its value changed, search changed lines rather than reading every patch. With `repo` and `path` defined above, set `marker_regex` to a relevant regular expression and `patch_file` to a fresh private file. The illustrative marker locates calls to an encoding API without putting a secret in the search argument:

~~~bash
umask 077
marker_regex='Encoding[.]ASCII[.]GetBytes'
git -C "$repo" --no-pager log --all --follow -n 20 -p \
  --no-ext-diff --no-textconv -G "$marker_regex" -- "$path" >"$patch_file"
~~~

`-G` selects changes whose added/removed lines match. `-S` instead detects a changed number of occurrences of a string: replacing one literal argument with another can leave the marker count unchanged and be missed by `-S`. The output limit bounds displayed commits, not history traversal cost. Check status and both sides of the selected patch, then extract the relevant revision/path using `show` above. Empty output can reflect the path, regex, refs or history limits. See [Git's patch-search semantics](https://git-scm.com/docs/git-log).

A historical secret proves it was stored at that revision, not that it is currently valid. Keep sensitive content out of routine reports. If ownership checks reject a repository, inspect ownership/trust first; do not set `safe.directory '*'` to bypass the check globally. Report commit ID, historical path and history limitations with the finding.

## Distinguish a replacement commit from later working changes

`git diff "$revision" -- "$path"` compares that revision with the current working tree. It does not mean “show what this commit changed”, and local edits can affect the result. `git diff "$revision" HEAD -- "$path"` instead compares two committed snapshots. A minus line means removed from the comparison's first endpoint, not inherently the accidentally added key.

For a selected ordinary non-merge commit, inspect its parent and path changes, then compare that parent with the commit:

~~~bash
git -C "$repo" --no-pager show --no-patch --format='%H %P %s' "$revision"
git -C "$repo" --no-pager diff --name-status --no-ext-diff --no-textconv \
  "${revision}^1" "$revision" --
git -C "$repo" --no-pager diff --no-ext-diff --no-textconv \
  "${revision}^1" "$revision" -- "$path"
~~~

`${revision}^1` means the first parent. A root commit has no parent; a merge has several, so choose the relevant parent explicitly rather than treating the first-parent diff as every merged change. A later correction can replace or remove a secret yet leave the prior blob in available history. Use the observed old/new path rather than stripping patch prefixes or concatenating added/deleted lines; a clipped screenshot or diff hunk is not a complete private key.

For a replacement where the desired old file was present in that first parent, define `historical_path` as its exact root-relative path there and `output_file` as a new private working-copy destination:

~~~bash
umask 077
(set -C; git -C "$repo" show "${revision}^1:$historical_path" >"$output_file")
~~~

Check the command status, full file boundaries and expected format. A failed command can leave an empty file; do not treat its existence as recovery success. The complete blob avoids diff context omission and minus-prefix contamination. Do not switch branches, reset or revert an existing worktree merely to read it. If the file appeared in another earlier revision, use that observed revision instead of assuming every correction has the same parent layout.

Report revision/parent, path, complete versus partial bytes and locally available history limits. A successful blob recovery establishes historical storage. Key parsing/fingerprint comparison and an explicitly requested account authentication are later, separate tasks; do not label a key “root's” solely from its filename, owner of a commit or the author of a correction.

See [diff endpoints](https://git-scm.com/docs/git-diff), [parent notation](https://git-scm.com/docs/gitrevisions) and [blob extraction](https://git-scm.com/docs/git-show).
