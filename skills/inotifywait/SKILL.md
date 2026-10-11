---
name: inotifywait
description: Wait for a selected local filesystem event with Linux inotifywait and distinguish creation, write closure and move events. Use when a file-processing trigger races writes or human-readable event output is parsed as an exact pathname.
---

# Observe one directory event

Read this entire SKILL.md before acting. Require Linux inotify-tools, an existing owned directory and the event/window relevant to the task. No conditional resources are required. Finish with the observed event, status and watch coverage; an event does not guarantee a complete or stable file.

Define `watch_dir` as the absolute directory. For a ten-second wait for its first relevant event:

~~~bash
inotifywait --timeout 10 --event close_write --event moved_to --csv "$watch_dir"
status=$?
~~~

Keep stderr: `Watches established` marks readiness, while stdout carries events. Arrange the owned producer after readiness if reproducing a trigger. Without `--monitor`, the command exits after the first matching event. Status 0 means a selected event occurred; 2 means the timeout expired; 1 indicates an error or watch loss/unexpected event. A timeout establishes only that no selected event was observed in this window.

`CREATE` occurs when an entry is created, potentially before writing ends. `CLOSE_WRITE` means a writable handle closed, not necessarily that bytes changed or no other writer remains. `MOVED_TO` observes an entry moved into the directory, including renames within it; pair it with the producer's actual completion contract. Watching the directory here is nonrecursive. `--recursive` needs one watch per subdirectory, can miss setup/race events and consumes watch limits. `--monitor` runs indefinitely; its inactivity timeout is not a fixed overall duration when events continue.

Default space-separated output does not escape filenames. CSV must be parsed by a CSV parser, not split on spaces or commas. For a supported version's programmatic pathname stream, `--format '%w%f%0' --no-newline` emits NUL delimiters; use a consumer that preserves them and verify support first. Formatted event strings have a documented size limit and can truncate. Do not infer exact arbitrary filename recovery from a sed replacement over the default display.

An event's path can be stale after a rename; queue overflow or watch loss can leave gaps. Recheck the selected file/type and producer state before processing, and retain the event log rather than treating it as a complete audit history. Running an extractor before checking its output already invokes that parser and its helpers; a later filename/description blacklist does not protect that earlier operation.

Reference: [inotifywait manual, events and limitations](https://manpages.debian.org/bookworm/inotify-tools/inotifywait.1.en.html).
