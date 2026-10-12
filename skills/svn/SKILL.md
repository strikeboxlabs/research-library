---
name: svn
description: Acquire a selected Subversion source revision and interpret repository history. Use when a working-copy update is confused with a commit diff or checkout completeness is uncertain.
---

# Acquire the selected Subversion revision

Read this entire SKILL.md before acting. Require the approved repository URL, legitimate access and a fresh owned destination. No conditional resources are required. Finish with the selected URL/revision, checkout status and explicit omissions; acquiring source does not run it.

Define `url` as the trusted project URL. Inspect installed help and a bounded history:

~~~bash
svn --version --quiet
svn help checkout
svn log --limit 10 --verbose "$url"
~~~

Remote history queries need repository access; a checkout is not a complete offline history mirror. A URL's default history starts at HEAD, while a local path's default starts at its BASE. The limit makes this a sample, not exhaustive history. Commit messages are author-supplied descriptions; verbose changed paths provide separate evidence.

Choose numeric `revision` from the intended release/history and define `destination` as a nonexistent absolute directory in an owned parent:

~~~bash
svn checkout --ignore-externals -r "$revision" "$url@$revision" "$destination"
status=$?
~~~

The peg revision identifies the path at that revision; `-r` selects the requested content revision. Keep external dependencies excluded until independently selected. Check status and the final revision receipt, then:

~~~bash
svn info "$destination"
svn status "$destination"
~~~

Keep repository UUID/URL and working-copy revision distinct from Last Changed Rev. Interruptions, conflicts or obstructing files leave incomplete results; do not force checkout over an unrelated directory. A partial owned checkout can be resumed with the same pinned command after checking its identity and local edits. Do not build or execute downloaded scripts merely to validate acquisition.

An existing `svn update -r` changes the working copy toward that revision and may merge local edits. Its A/D/U notifications describe that transition, not necessarily the changes made by that one commit. Inspect the selected commit's verbose log separately; do not roll an edited worktree backward to answer a history question.

References: [checkout](https://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.checkout.html), [log scope](https://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.log.html), [info fields](https://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.info.html). Version Control with Subversion by Ben Collins-Sussman, Brian W. Fitzpatrick and C. Michael Pilato (CC BY 2.0); consult installed help for release differences.
