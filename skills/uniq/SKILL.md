---
name: uniq
description: Collapse adjacent repeated records or report adjacent-run counts with GNU uniq. Use when a local text list needs deduplication and ordering, projected identity fields or partial input can change the result.
---

# Compare the intended complete records

Read this entire SKILL.md before acting. Establish the record delimiter, comparison identity and whether order must be retained before choosing adjacent-run filtering or global deduplication. No conditional resources are required. Finish with status, selected records and ordering/coverage limits; reduced output does not establish complete acquisition or valid account identities.

Check `uniq --version` for GNU coreutils. Define `input` as the preserved existing newline-delimited file and `output` as a fresh distinct path. To collapse only consecutive equal lines:

~~~bash
umask 077
LC_ALL=C uniq -- "$input" > "$output"
status=$?
~~~

Uniq compares adjacent records and retains the first in each equal run. **Illustrative:** `alpha, alpha, beta, alpha` on four separate lines yields three lines `alpha, beta, alpha`; the last alpha survives. It is not a global uniqueness test. If global deduplication and reordering are intended, use `LC_ALL=C sort -u -- "$input" > "$output"` instead, preserving its status and that changed order. Do not sort merely to hide a producer's duplicate/order anomaly.

For observed adjacent-run sizes, use `LC_ALL=C uniq -c -- "$input"` with the same file contract. Those counts are per run; one value can have several separate counts. `-u` emits only singleton runs and **removes** repeated runs, rather than retaining one copy of every distinct value. `-d` emits one line per repeated run. Select the behavior deliberately.

Default comparison is case-sensitive; `-i`, field/character skipping and limited comparison widths can merge different records. Choose case normalization only from the consuming format's identity rules. NUL-delimited filename input needs supported `-z` and a NUL-aware downstream reader; newline splitting cannot preserve filenames containing newlines.

Before projecting directory data into names, retain each complete DN, sAMAccountName and UPN association. A UPN prefix before `@` need not equal the account's logon name, and missing UPNs can silently omit accounts. Grepping any `@` line or cutting formatted text can mix attributes and collapse domains. Uniq cannot repair that projection, validate a schema or distinguish two objects reduced to the same string.

Check saved status and stderr; failed input reads can leave partial output. Avoid same-file redirection or aliases, which truncate the source first. A final successful uniq in a pipeline does not establish that a directory query completed. Preserve the producer's own diagnostics/status and reconcile returned record counts before using the selected list.

Reference: [GNU uniq packaged manual](https://manpages.debian.org/bookworm/coreutils/uniq.1.en.html).
