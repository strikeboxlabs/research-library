---
name: diff
description: Compare acquired directory trees or selected text files with GNU diff. Use to locate unexpected application changes against a matching baseline and distinguish differences from incomplete comparisons.
---

# Compare content against the right baseline

Read this entire SKILL.md before acting. For trees, establish corresponding roots and the baseline version/distribution before comparing recursively; for selected text files, use the hunk workflow below. Finish with the comparison scope, status, diagnostics and specific changes; a partial comparison or untrusted baseline cannot establish integrity.

Confirm GNU `diff --version` and support for `--no-dereference`. Define `baseline` and `observed` as existing absolute directory paths whose contents correspond. Match the application version, distribution and expected local customizations; a banner alone does not establish the exact release. Work from acquired copies and keep the originals. Removing documentation or configuration files to make trees match discards potentially relevant evidence.

Define `report` and `errors` as fresh files outside both trees:

~~~bash
if diff -r -q --no-dereference -- "$baseline" "$observed" > "$report" 2> "$errors"; then
    status=0
else
    status=$?
fi
~~~

- Status 0: no content differences under the selected comparison rules and coverage.
- Status 1: differences found; inspect the report. This is an ordinary result, including under shell `set -e` when handled by the shown conditional.
- Status 2: trouble, such as an unreadable or missing operand. Preserve diagnostics; reported differences may be partial. Correct the access/acquisition issue before claiming complete coverage.

`-r` descends into common subdirectories; a nonrecursive comparison can miss their differences. `-q` reports which files differ. **Illustrative:** `Only in /evidence/observed: extra.php` identifies an unmatched pathname on that side, not who created it or why. `--no-dereference` compares symbolic links themselves instead of following their targets; account for excluded target contents separately. This is not a full comparison of ownership, permissions or timestamps.

## Inspect the relevant text change

Choose one relative path present as an ordinary file on both sides. Define `baseline_file` and `observed_file` as its full paths, and `patch`/`file_errors` as fresh output files:

~~~bash
if diff -u --no-dereference -- "$baseline_file" "$observed_file" > "$patch" 2> "$file_errors"; then
    status=0
else
    status=$?
fi
~~~

Apply the same status rules. Unified hunks show `-` lines from the baseline and `+` lines from the observed file; inspect their surrounding control flow. Text inside a comment is not an executed statement, and an existing log does not prove that the currently displayed code wrote it. A differing configuration file deserves interpretation, not dismissal by filename.

For a binary difference, retain both artifacts and use the format's inspection tools. Avoid initially hiding whitespace, case, carriage-return or excluded-file differences; those options change what equality means. Record any later normalization explicitly. No reported differences supports equality only within the comparison's scope, not a claim that the baseline, acquisition or application is trustworthy.

See the [GNU diff option reference](https://man7.org/linux/man-pages/man1/diff.1.html) for comparison modes and status semantics.
