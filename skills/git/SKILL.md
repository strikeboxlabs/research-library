---
name: git
description: Acquire a selected upstream checkout or inspect historical files, stored links/submodules, patches, remote configuration and local Git hooks. Use when working-tree types, missing history, stored URLs or hook execution complicate repository evidence.
---

# Git repository evidence

Read this entire SKILL.md before acting. Choose the requested task and complete its relevant checks; report the observed evidence and remaining limits, not just command success. Use an existing trusted repository or isolated evidence copy.

- Acquiring a selected upstream source: [source checkout](references/source-checkout.md). Read this reference fully before its procedure.
- Removed/replaced files, patch search or ambiguous diff endpoints: [historical content](references/history-recovery.md). Read it fully before selecting/extracting a revision.
- Exposed application settings or a redundant restore after acquisition: [configuration evidence](references/exposed-settings.md). Read it fully before recovery.
- Stored URLs: [remote configuration](#inspect-an-acquired-remote-configuration).
- Hook behavior: [local hook diagnosis](#diagnose-a-missing-or-unexpected-local-hook).
- Patch validation: [scoped patch checks](#prepare-and-check-a-scoped-patch).
- Link/submodule types: [stored modes and metadata](#inspect-stored-symlinks-and-submodules-without-checking-them-out).

Define `repo` as an existing repository's absolute path. Start with `git -C "$repo" status --short` and `git -C "$repo" rev-parse --is-shallow-repository`; preserve local edits and history limitations. For historical content, follow the reference above before selecting a revision or extracting a blob. The remaining branches below use that same `repo` and explicitly defined task paths; none requires a checkout/reset or a live authentication attempt.

## Inspect an acquired remote configuration

For an acquired Git config file, define `config_file` as its absolute working-copy path and `remote_report` as a fresh private output file. Query it without contacting a remote or following include directives:

~~~bash
umask 077
git config --file "$config_file" --no-includes --show-origin \
    --get-regexp '^remote\..*\.(url|pushurl)$' >"$remote_report"
~~~

Check status before interpreting the report: 1 means no matching key, while invalid syntax is a separate error. Keep embedded URL credentials out of routine output. A stored HTTP username/password or token identifies configuration evidence, not a currently valid login or the same identity on SSH or a web application.

This query covers one file. It intentionally excludes included files, other configuration scopes and credential helpers; no match does not prove no remote or credential exists. URLs can also be rewritten by `url.*.insteadOf` settings. Inspect relevant configuration separately before asserting the effective destination. Do not fetch, pull or invoke a credential helper just to inspect stored values.

See [Git configuration](https://git-scm.com/docs/git-config) for file/include scope and [remote URL behavior](https://git-scm.com/docs/git-remote) when stored and effective URLs differ. The older `--get-regexp` spelling supports Git versions predating the `config get` subcommand.

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


## Prepare and check a scoped patch

For an intended change to a tracked file, use the trusted `repo` and define `path` as the selected repository-root-relative file path. Define `patch` as a fresh absolute file outside the worktree:

~~~bash
git -C "$repo" --no-pager diff --binary --full-index --no-ext-diff --no-textconv -- "$path" >"$patch"
git -C "$repo" apply --stat "$patch"
~~~

Check the first status before reading the patch. This comparison captures unstaged changes against the index; it omits staged-only changes and ordinary untracked files. Select `--cached` for staged changes or an explicit base revision for tracked working-tree changes relative to that revision. Inspect status and the patch's paths/hunks before treating it as the complete intended change. `--binary` includes applicable binary differences; `--full-index` also makes textual patches carry full blob IDs. A human text-conversion view is not necessarily an applicable patch.

Set `base_repo` to a separate unchanged working copy of the intended base, at its root:

~~~bash
git -C "$base_repo" apply --check "$patch"
~~~

`--check` validates applicability without applying. Run from the intended repository root: from a subdirectory, Git can ignore patch paths outside that directory and still return zero. An empty or unexpected `--stat` report is a scope problem to resolve before accepting the check. Checking against the already-edited copy can fail because it contains the new content. Zero status does not prove behavior or authorize a CI build; a job can execute patched build scripts. A failed check needs base/path/context investigation, not an automatic `--reject` or `--unsafe-paths` retry.

A captured diff is not generally a full file. Removing every leading `+` loses unchanged context and mixes file headers/hunks. A snipped patch cannot reconstruct omitted bytes; retain that limitation when reviewing historical configuration or credentials.

See [diff selection](https://git-scm.com/docs/git-diff) and [apply/check semantics](https://git-scm.com/docs/git-apply).

## Inspect stored symlinks and submodules without checking them out

When a path looks like a plain file on one machine but a link on another, compare the index and selected revision. Use the existing isolated `repo`; define `path` as the selected root-relative file path and `revision` as the observed commit:

~~~bash
git -C "$repo" ls-files --stage -- "$path"
git -C "$repo" ls-tree -r "$revision" -- "$path"
~~~

The first describes the current index, which can differ from the revision. Stage 0 is the ordinary entry; stages 1-3 indicate an unresolved merge. Interpret the stored mode before reading content:

| Mode | Meaning and next check |
|---|---|
| `100644` / `100755` | Regular / executable blob; an executable bit does not establish that it ran. |
| `120000` | Symlink blob containing the link target text. Inspect that blob rather than following the working-tree path. |
| `160000` | Gitlink naming a submodule commit. Inspect `.gitmodules` at the same revision for its path/URL mapping; the commit need not exist in the superproject object store. |

For an observed symlink blob ID, set `oid` to that ID:

~~~bash
git -C "$repo" cat-file -p "$oid"
git -C "$repo" show "$revision:.gitmodules"
~~~

The first reads stored link text, without dereferencing the link. The second reads metadata without initializing/fetching the submodule; an absent `.gitmodules` is an evidence gap, not permission to guess its URL. With `core.symlinks=false`, checkout can produce a plain file while the index still records `120000`. Check effective configuration and actual filesystem behavior before concluding the type changed. Use `-z` listings when programmatically handling unusual filenames.

Recursive cloning is not passive inspection. For [CVE-2024-32002](https://github.com/git/git/security/advisories/GHSA-8h77-4q3w-gfgv), affected Git, recursive submodules, case-insensitive filesystem behavior and symlink support matter together. A README's version claim or an isolated link alone does not prove those conditions. Establish the actual client/package patch status; do not recursively clone an untrusted sample to find out.

See [index modes](https://git-scm.com/docs/gitformat-index), [index listings](https://git-scm.com/docs/git-ls-files), [tree listings](https://git-scm.com/docs/git-ls-tree) and [symlink configuration](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coresymlinks) for representation differences.
