# Reproduce the selected directory race

Use a disposable guest with an expressly selected log directory and privileged rotation fixture. Record original directory paths, ownership, mode and relevant logrotate configuration. The historical code renames the log's directory to a sibling ending in `2`, then substitutes a symlink. Existing destination/sibling names and directory users matter; do not test against a shared service path.

Define `logrotten` as the reviewed installed binary, `logfile` as the absolute fixture log path and `marker_file` as an existing inert text file. The fixture's destination must not contain an existing file with the same basename. For the legacy default-destination branch in that disposable guest:

~~~bash
"$logrotten" -d -p "$marker_file" "$logfile"
~~~

The payload file need not contain an executable callback: a unique text marker is sufficient to establish redirected content. Start the specifically authorized fixture rotation separately while this process waits. Increasing log size or forcing rotation changes service state; it is a selected fixture action, not a routine discovery step.

`-d` exposes paths and progress. The default watches a move event; `-o` and `-c` select the open-event path in the legacy source. `-s` adjusts the delay before writing the supplied content. Choose from the actual rotation behavior; repeated timing tweaks without observing the triggering event provide little evidence.

## Interpret the stages

- Waiting indefinitely: confirm the watched path, event mask and actual rotation. No event does not establish that the service is secure.
- Rename/symlink message: inspect the resulting paths. This is not yet proof of a privileged file or payload execution.
- Write failure: inspect destination creation, mode, ownership and race timing. A symlink alone does not grant write access.
- Completion message: compare the destination's exact marker bytes, path and metadata. A redirected write is distinct from a later process consuming that file.

The implementation writes to the destination with truncation and changes its mode; it does not preserve an arbitrary pre-existing file. Keep the fixture destination empty for this basename. After the run, stop only the test watcher, restore the original directory arrangement and verify that the selected fixture's logging/rotation works. Prefer reverting the disposable guest when exact cleanup is uncertain. Do not wildcard-remove directories or completion scripts.

This procedure supports evidence of the race and write. It does not claim every listed historical logrotate version, distribution patch set or filesystem behaves identically. Record actual behavior and unresolved stages instead of a vulnerability conclusion from a version banner.
