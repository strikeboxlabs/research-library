---
name: locate
description: Find candidate Linux paths in an existing locate database and verify the selected current entry. Use when stale indexes, path substrings or access filtering obscure whether an artifact exists.
---

# Treat the index as a path lead

Read this entire SKILL.md before acting. Require the existing database accessible to the current account and a selected nonsecret filename fragment. Check the installed implementation/options with `locate --version` and `locate --help`; all instructions are inline. Finish with query status and the verified current selected entry, or the precise index/access gap.

Define `name_fragment` as a known literal filename component without glob metacharacters, and `matches` as a fresh private output file:

~~~bash
umask 077
locate -0 -- "$name_fragment" > "$matches"
status=$?
~~~

For an implementation supporting these flags, `-0` separates names with NUL. Consume them without line splitting and retain diagnostics/status; a failed database read is not no matches. In plocate, status1 covers both no matches and errors, so read stderr rather than interpreting that status alone. Substring matches may occur anywhere in the pathname, so select the actual basename and kernel/version directory deliberately. Do not execute a returned pathname as shell text.

Check the selected path's current type, metadata and readability before using it. The index can retain deleted entries and omit newer files, excluded mounts/directories or names hidden by access policy. `-e` can filter nonexistent paths where supported; it still does not prove readability or eliminate a later filesystem race. A missing index requires an appropriately scoped live search, not an automatic privileged `updatedb` run.

A module-file match identifies a candidate artifact on disk. Establish its association with the intended kernel/build and currently loaded module independently; a matching name or version-directory label is insufficient. The query neither loads that module nor validates its contents.

Reference: [locate/plocate database, matching and existence semantics](https://plocate.sesse.net/plocate.1.html). Use the installed implementation's manual for differing defaults or database policy.
