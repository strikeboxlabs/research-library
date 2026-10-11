# Review a scheduled Git job without triggering its helpers

Acquire the selected job script, repository configuration and process transcript as files. Read them without sourcing the script or running its Git operations. Establish the actual executable/version, working directory, environment, UID and repository owner independently. A `.git` directory identifies a Git repository, not specifically GitHub hosting; remote configuration and deployed service evidence are separate.

Trace the job's control flow before trusting its progress messages. `git status --porcelain` normally succeeds for both clean and changed worktrees; its records describe changes, while its exit status describes whether the query worked. `if ! git status --porcelain` tests failure, not absence of changes. In such a job, a successful clean query can enter the purported changes branch. Inspect handling of a failed `cd`, failed staging/commit and subsequent push separately; a push process is not evidence that a new backup commit was created or accepted.

For an already trusted, owned repository only, define `repo` as its absolute path and `status_file` as a fresh private file:

~~~bash
umask 077
(set -C; git -C "$repo" status --porcelain=v1 -z --untracked-files=all >"$status_file")
status=$?
~~~

Resolve nonzero status before reading the result. With zero status, an empty file means no records within this query's scope; a nonempty file needs interpretation of index, worktree, untracked and conflict states before any backup action. Preserve NUL framing, including the two path fields of a rename. Ignored files are omitted, and an index/worktree snapshot can become stale. This query neither commits nor pushes. Do not store NUL output in a shell variable or use line counts as a changed-file count.

Configuration can launch helpers outside ordinary commit hooks. In supported versions, `core.fsmonitor` can name a filesystem-monitor helper involved in index refresh, including status; newer builds also recognize boolean settings for a built-in monitor. Confirm the actual Git version before interpreting the value. Review includes, hook paths, filters, diff/text conversion and credential/transport helpers relevant to the selected operation. A file's owner and commit author are not the identity executing these programs.

Read untrusted configuration as data first. A narrowly scoped `git config --file ... --no-includes` query, as described in the entrypoint, reads that selected file without executing its monitor; it does not establish all effective scopes. Do not trigger helpers under elevated rights to prove a finding, add wildcard ownership exceptions or reproduce a supplied privileged payload. Report the configuration/control-flow finding, observed job identity and missing runtime/version evidence separately. An owned ordinary status check does not prove what a privileged scheduler previously ran.

References: [status records](https://git-scm.com/docs/git-status), [configuration and fsmonitor](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefsmonitor), [helper protocol and hook events](https://git-scm.com/docs/githooks).
