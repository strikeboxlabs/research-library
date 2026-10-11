---
name: crunch
description: Generate a small patterned local text fixture with crunch. Use when literal characters, placeholder alphabets and output size need a reproducible bounded dataset.
---

# Generate a bounded owned text fixture

Read this entire SKILL.md before acting. Require installed crunch, an owned fresh output and a calculated finite pattern. No conditional resources are required. Finish with status, measured records/bytes and exact pattern; interruption leaves partial output.

Review installed help. For this illustrative five-character log-label fixture, define `fixture` as a fresh absolute file:

~~~bash
umask 077
(set -C; crunch 5 5 + + 0123456789 '!_' -t 'Log%^' >"$fixture")
status=$?
~~~

The four alphabets are lowercase, uppercase, digits and symbols; plus selects an unused default here. Percent substitutes a digit and caret a symbol; other pattern characters stay literal. Expected coverage is 20 labels and 120 bytes including newlines, not an execution result. Check status, count and sampled boundaries before accepting it.

Quote patterns/alphabets. Match min/max length to the complete template. Calculate expansion before running: chunk-size/line options split output rather than imposing a total work bound. Do not reuse an existing fixture or pass an incomplete file to its consumer.

Reference: [crunch patterns and output](https://manpages.debian.org/bookworm/crunch/crunch.1.en.html).
