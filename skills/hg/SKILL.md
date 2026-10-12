---
name: hg
description: Inspect bounded Mercurial history and a selected changeset in an existing trusted repository. Use when local revision numbers, working-copy differences or repository configuration obscure what actually changed.
---

# Inspect the selected changeset

Read this entire SKILL.md before acting. Require an existing trusted local repository, an identified Mercurial installation and the intended history/file scope. All instructions are inline. Finish with the changeset identity, comparison parent, selected files and command status; unresolved configuration trust or unreadable history is a prerequisite gap.

Review repository and applicable user/system configuration as text before invoking hg. Hooks, extensions and aliases can execute code; filesystem ownership or a read-oriented command name does not make acquired configuration trustworthy. Use the repository's ordinary account. Do not run an unreviewed repository under a more privileged identity. `HGPLAIN` normalizes output rather than providing a sandbox, and an empty `HGRCPATH` still permits repository configuration. See [configuration trust](https://www.mercurial-scm.org/help/topics/config#trusted) and [environment controls](https://www.mercurial-scm.org/help/topics/environment).

Check `hg --version` and installed `hg help log`/`hg help diff`. Define `repository` as the verified absolute root. List a bounded history:

~~~bash
hg --cwd "$repository" --pager never log --limit 10 --verbose
~~~

Read changeset IDs, parents, dates and changed-file lists together. Ten entries are a selected window, not complete history. Numeric revisions are local to a repository; retain the changeset ID rather than only the local number. Resolve an ambiguous abbreviation before selecting a change. A commit summary is an author's description, not proof of its effects or deployment. File-specific history has rename/removal limitations; use installed help when those determine coverage.

Define `revision` as the selected observed changeset ID and `tracked_path` as one intended tracked file relative to that root. Inspect its recorded change:

~~~bash
hg --cwd "$repository" --pager never diff --change "$revision" -- "$tracked_path"
~~~

`--change` compares that changeset with its first parent. For a merge, this is not a comparison with both parents. Without a revision selector, ordinary diff instead compares the working copy with its parent. Retain diagnostics/status: an empty patch can reflect the selected path or binary handling and does not prove the whole changeset is empty. Avoid forcing binary bytes into terminal text. Keep any sensitive history private and report the relevant source change without copying credentials.

These inspections do not update the working copy or fetch missing history. If the requested revision is absent, record that limit before choosing a separately intended synchronization. See [log coverage](https://www.mercurial-scm.org/help/commands/log), [diff comparisons](https://www.mercurial-scm.org/help/commands/diff) and [global options](https://www.mercurial-scm.org/help/commands).
