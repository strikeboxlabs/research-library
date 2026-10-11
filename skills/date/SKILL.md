---
name: date
description: Format an established epoch timestamp with GNU date without changing the clock. Use when a local-time display, omitted timezone or empty input obscures an artifact-time comparison.
---

# Format an established epoch value

Read this entire SKILL.md before acting. Confirm GNU coreutils with `date --version` and establish the input's unit, provenance and desired timezone. No conditional resources are required. Finish with the original value, formatted time, timezone and status; a successful conversion does not verify the event's timestamp.

Define `epoch_seconds` as the validated numeric seconds since the Unix epoch, including a fractional part only when supplied by the source. Convert explicitly to UTC:

~~~bash
LC_ALL=C TZ=UTC0 date --date="@$epoch_seconds" '+%Y-%m-%dT%H:%M:%S%:z'
status=$?
~~~

Check stderr and `status`. `--date` formats a supplied value; it does not set the system clock. The leading `@` selects epoch seconds, avoiding ambiguous calendar strings. Milliseconds must be converted with their scale and precision understood before this command. Missing or malformed input remains unresolved; do not substitute the current time or a successful empty-string parse.

Retain the input and explicit zone when comparing results. This format displays whole seconds; retain the original fraction if finer comparison matters. A day/month/year display without timezone can obscure ordering across systems or daylight-saving changes. Time conversion does not identify file creation, the running kernel, clock synchronization or why a file changed.

See the packaged [GNU date manual](https://manpages.debian.org/bookworm/coreutils/date.1.en.html).
