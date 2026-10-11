---
name: tree
description: Inspect the layout of a selected owned directory with bounded depth. Use to distinguish build artifact names, hidden entries, link targets and incomplete directory listings.
---

# Read the selected directory layout

Read this entire SKILL.md before acting. Require installed tree, the exact owned directory and permission to inspect its entries. No conditional resources are required. Finish with the directory, options/depth, status and visible paths or access gaps; a layout is not an artifact-integrity or build-success check.

Check `tree --version`. Define `directory` as the selected absolute directory:

~~~bash
tree -a -L 2 -- "$directory"
status=$?
~~~

`-a` includes dot-prefixed entries; `-L 2` bounds display depth. `--` ends option processing. Default listing shows symbolic-link targets without descending into linked directories; `-l` would change that scope. Review errors and the saved status before treating missing entries as absent. Increase depth deliberately when the required subtree is outside this view. The footer describes listed entries, not a census below the depth limit or unreadable directories.

An **illustrative** `dist/example-1.0.tar.gz` beside `dist/example-1.0-py3-none-any.whl` identifies two filenames with different distribution suffixes. Inspect the selected artifact separately when contents, hashes, compatibility or producer completion matter. Names and directory presence cannot establish those properties. Tree's display is human-readable; unusual filename characters require separate exact-path handling before feeding paths to another command.

Reference: [tree options and listing behavior](https://manpages.debian.org/bookworm/tree/tree.1.en.html).
