---
name: date
description: Format an established epoch timestamp or a current/relative job-date label with GNU date without changing the clock. Use when locale, timezone or a label mistaken for event coverage obscures a comparison.
---

# Format the selected time value

Read this entire SKILL.md before acting. Select an epoch conversion or a current/relative job label, confirm GNU coreutils with `date --version`, and establish the desired timezone. For a supplied timestamp, establish its unit and provenance first. No conditional resources are required. Finish with the input/clock context, formatted time, timezone and status; a successful query does not verify an event's timestamp.

For a current job label, `LC_ALL=C TZ=UTC0 date '+%Y-%m-%d'` formats the current clock in UTC; check its status before using the value. Without `TZ`, a scheduled `date +'%Y-%m-%d'` uses its process's timezone configuration. That label identifies the query's day, not the changed files' dates, a successful backup or a synchronized clock. Preserve the zone and distinguish this branch from converting a supplied artifact timestamp below.

For an explicitly UTC-based relative backup label, `LC_ALL=C TZ=UTC0 date --date='yesterday' '+%Y%b%d'` uses the job's current clock as its base. `%b` is a locale-dependent month abbreviation; the C locale makes that field predictable. Capture the label once and check status before constructing related filenames so separate queries cannot straddle midnight. This label does not select or date the records inside a compressed log. For another operational timezone, use its established rules and retain the zone/base time rather than silently interpreting the label as UTC. See [GNU date input guidance](https://www.gnu.org/software/coreutils/manual/html_node/Date-input-formats.html).

Define `epoch_seconds` as the validated numeric seconds since the Unix epoch, including a fractional part only when supplied by the source. Convert explicitly to UTC:

~~~bash
LC_ALL=C TZ=UTC0 date --date="@$epoch_seconds" '+%Y-%m-%dT%H:%M:%S%:z'
status=$?
~~~

Check stderr and `status`. `--date` formats a supplied value; it does not set the system clock. The leading `@` selects epoch seconds, avoiding ambiguous calendar strings. Milliseconds must be converted with their scale and precision understood before this command. Missing or malformed input remains unresolved; do not substitute the current time or a successful empty-string parse.

Retain the input and explicit zone when comparing results. This format displays whole seconds; retain the original fraction if finer comparison matters. A day/month/year display without timezone can obscure ordering across systems or daylight-saving changes. Time conversion does not identify file creation, the running kernel, clock synchronization or why a file changed.

See the packaged [GNU date manual](https://manpages.debian.org/bookworm/coreutils/date.1.en.html).
