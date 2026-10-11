---
name: readlink
description: Inspect a selected symlink's stored target text and distinguish it from canonical path resolution. Use when a moved link, missing referent or path-check result complicates local file evidence.
---

# Read the link before interpreting its referent

Read this entire SKILL.md before acting. Select the exact existing local path and intended literal-target or canonicalization task, retain status/output, and report namespace and concurrent-change limits. All task instructions are inline; neither reading link text nor resolving a path authorizes reading or changing its referent.

Check `readlink --version` and installed help for GNU options. Define `link_path` as the selected absolute path, with no trailing slash, whose symlink metadata may be inspected:

~~~bash
readlink -v -- "$link_path"
status=$?
~~~

With no canonicalization flag, this reports the stored target string without opening its contents or requiring its referent to exist. A nonzero result can mean an ordinary file, a missing/unreadable path or another error; retain verbose diagnostics. A dangling link can still yield successful target text. A relative target is interpreted from the link's parent directory, so moving the link can change its referent without changing the stored text. Absolute targets depend on the resolving process's filesystem/mount namespace.

If the requested task instead requires an existing canonical path, define `selected_path` as that exact input:

~~~bash
readlink -v -e -- "$selected_path"
status=$?
~~~

`-e` follows links and requires every component to exist. `-f` permits a missing final component; `-m` removes component-existence requirements. Successful output from the latter modes therefore does not prove that the resulting object exists. None of these options measures its contents, owner, effective access or later process use. A loop or missing ancestor is a distinct failure to retain.

For machine-readable path data, use `-z` and a NUL-aware consumer. Command substitution removes trailing newlines, and ordinary newline output is ambiguous for unusual target names; do not silently normalize such evidence.

A resolved string is an observation, not a stable handle or containment guarantee. Another writer can change a link or parent component between inspection and use. A substring check on literal target text is not a directory-boundary policy. Report the exact mode, input, returned text/status and observation context; leave changed/missing objects unresolved rather than creating links or retrying a privileged consumer.

See the [GNU readlink manual](https://manpages.debian.org/bookworm/coreutils/readlink.1.en.html) for installed-option and missing-component differences.
