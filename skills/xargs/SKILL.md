---
name: xargs
description: Run a reviewed command over an explicit item list with GNU xargs, preserving filename boundaries and bounded concurrency. Use when whitespace splitting, empty input, child status or shared outputs make a batch unreliable.
---

# Run an explicit batch and assess its children

Read this entire SKILL.md before acting. Require GNU xargs, the reviewed command and a list whose item encoding and scope are known. Choose a finite concurrency and independent child task; finish with selected items, child/aggregate results and any incomplete batch. Missing command/list or uncertain shared-state effects must be resolved before running.

Inspect `xargs --version` and `xargs --help`. Define `list` as an existing NUL-delimited file of selected absolute local file paths. This **illustrative** read-only task obtains byte counts, at most two children at a time:

~~~bash
xargs -0 -r -n 1 -P 2 -a "$list" -- wc -c --
status=$?
~~~

`-0` treats each NUL-separated item literally; default input instead interprets whitespace, quotes and backslashes. The producer must use the same NUL contract. `-a` selects that file; a shell input redirection would replace a pipeline's input. `-r` avoids the usual one invocation on empty input. `-n 1` puts one item in each invocation; `-P` alone need not split a small list into multiple jobs. Zero concurrency means unbounded parallelism.

Items become command arguments, not shell source. Keep the child command fixed and use its own option terminator where supported, as with wc above; xargs's terminator does not protect the child. For commands requiring shell logic, keep the program fixed and pass items positionally rather than substituting filenames into shell code.

Parallel output order is unspecified and streams can mix. Retain file identity and use independent per-item output locations when exact reports matter; choose `-P 1` if ordered execution or shared state requires it. A filename list does not freeze file contents/identity between selection and use. `-a` leaves child stdin unchanged, whereas default input mode redirects it from /dev/null; establish noninteractive behavior rather than relying on an unexpected prompt.

Check diagnostics and each item's result. GNU aggregate status 123 means a child exited 1–125; 124 means a child returned 255; 125 a child signal; 126/127 command execution/lookup failure. A 255 result stops further input processing. GNU versions through 4.9.0 can return from parallel mode while other children still run after that result; establish their state before retrying shared work. Aggregate zero is not semantic validation of every artifact. See the [GNU xargs manual](https://manpages.debian.org/testing/findutils/xargs.1.en.html).
