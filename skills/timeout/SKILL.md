---
name: timeout
description: Bound an owned foreground command with GNU timeout and retain partial output and termination status. Use when a query budget or pipeline's final status hides an incomplete observation.
---

# Bound the selected process

Read this entire SKILL.md before acting. Require the reviewed command and intended duration/termination behavior. No conditional resources are required. Finish with status, captured result and termination evidence; a timeout is incomplete observation.

Confirm GNU `timeout --version`. Define `seconds` as a positive task budget, `command` as the reviewed executable and `output`/`errors` as fresh private paths. Add its selected arguments explicitly:

~~~bash
timeout --signal=TERM --kill-after=2s "${seconds}s" "$command" >"$output" 2>"$errors"
status=$?
~~~

The extra two seconds is an example grace period before KILL. Use INT instead when an owned collector needs that shutdown contract. Duration0 disables the associated limit.

Default status124 means timeout, 125 timeout's own failure, 126 cannot invoke and 127 command missing. Status137 indicates KILL and cannot by itself distinguish who was killed. Otherwise retain the command's status. `--preserve-status` changes this contract. Partial output can survive termination.

In a pipeline, save individual statuses or use deliberate pipefail; a final successful grep does not establish query completion. `--foreground` supports terminal interaction but does not time out children. Check remaining owned processes when that matters.

Source: [GNU timeout](https://manpages.debian.org/bookworm/coreutils/timeout.1.en.html).
