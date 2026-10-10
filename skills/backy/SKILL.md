---
name: backy
description: Run and verify a local archive task with vdbsh/backy. Use when a task JSON, existing cycle archive, silent subprocess or custom wrapper makes backup scope and success unclear.
---

# Verify a backy archive job

This covers the small Go utility [vdbsh/backy](https://github.com/vdbsh/backy), whose source reports version 1.2. Confirm the installed program's identity; other tools share this name. Its argument is a task JSON path, so do not assume `--help` or `--version` is supported. A separate `backy.sh` is a local wrapper: inspect it before assigning its behavior to backy.

Define `source_dir` as one approved, stable, readable absolute directory; `backup_dir` as an existing empty destination outside it; and `task`/`log` as fresh local files outside the source. Use an ordinary account that can read the source and write the destination. With jq available, create an archive-only configuration:

~~~bash
umask 077
jq -n --arg src "$source_dir" --arg dst "$backup_dir" \
  '{destination:$dst, archiving_cycle:"daily", multiprocessing:false,
    verbose_log:true, directories_to_sync:[], directories_to_archive:[$src],
    exclude:[]}' >"$task"
~~~

Review the generated values before running. Empty exclusions include hidden files; `exclude:[".*"]` can omit important dotfiles. Avoid empty path strings and use explicit absolute paths instead of relying on the executing account's `~` expansion. Run only one writer for this task/destination:

~~~bash
if backy "$task" >"$log" 2>&1; then
  status=0
else
  status=$?
fi
printf 'backy status: %s\n' "$status"
~~~

Read the log and inspect the actual output file. Status 1 means missing configuration, 2 configuration failure, 3 synchronization error, 4 archiving error, and 5 both operation errors. Unexpected panics or missing outputs need separate diagnosis. With `verbose_log:false`, child diagnostics can disappear.

An **illustrative** `Nothing to archive` can mean this cycle's filename already exists. Version 1.2 checks existence, not archive integrity or source changes, and ignores rename errors. Consequently, status 0 does not prove a fresh usable backup. Set `archive` to the observed completed `.tar.bz2` file and check its final listing status:

~~~bash
tar --list --verbose --file="$archive"
~~~

Inspect selected member contents in a separate restore directory before accepting the backup. Preserve failed output/logs; investigate destination permissions, space and child-tool failures before retrying. Do not delete an existing archive just to force another run. A fresh destination distinguishes a new job without destroying the old evidence; do not overlap it with another job's `.part` file.

## Check the entire configuration before reuse

Nonempty `directories_to_sync` invokes rsync with `--delete` and `--delete-excluded`; it can remove destination data. Backy has no dry-run switch in this implementation. Keep synchronization out of an archive-only task and inspect every consumed field, including destination and exclusions, when reviewing a wrapper.

Regex removal and textual path prefixes do not establish filesystem containment. A wrapper that rewrites a task before checking it has already changed the input; reopening a caller-writable JSON later can also change what is consumed. Review the file actually used and the executing identity before any privileged invocation. See the [implementation](https://github.com/vdbsh/backy/blob/main/backy.go) for version-specific flags, path handling and skipped-archive behavior.
