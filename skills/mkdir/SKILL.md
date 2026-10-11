---
name: mkdir
description: Create one selected owned Linux working directory with GNU mkdir. Use when a build/output tree needs deliberate permissions and an existing directory must not be mistaken for a newly created empty workspace.
---

# Establish the selected working directory

Read this entire SKILL.md before acting. Require the intended path beneath an existing owned parent and decide whether a fresh or pre-existing directory is acceptable. No conditional resources are required. Finish with creation status and actual directory metadata; successful creation does not validate its later contents.

Confirm `mkdir --version` for GNU coreutils. Define `directory` as the intended new absolute child path under that verified parent:

~~~bash
mkdir -m 700 -- "$directory"
status=$?
~~~

Check status/stderr before changing into or using it. Existing destination, missing parent and denied access are different failures; do not delete a conflicting directory or add -p automatically. Verify its type, ownership and effective access. Mode700 requests owner read/write/search only, but inherited group/ACL and filesystem policy require metadata review when that matters.

For an intentionally reusable directory tree, `mkdir -p -- "$directory"` creates missing parents and accepts existing directories. It does not make an existing tree empty or repair its owner/mode. `-m` does not set the modes of intermediate parents created by -p; the umask affects those. Keep build-specific cache/source identity separate from directory existence. A relative `build` path refers to the current directory, not automatically the checkout a previous command mentioned.

Reference: [GNU mkdir manual](https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html).
