---
name: logrotten
description: Assess and reproduce a selected logrotate directory race with the Logrotten CLI in an authorized disposable Linux fixture. Use to connect rotation configuration, directory control, inotify events and actual file-write evidence.
---

# Match the race to the rotation operation

Read this entire file and [race procedure and recovery](references/race-and-recovery.md) before acting. Logrotten changes directory paths and can redirect a privileged write. Require an isolated authorized fixture and ownership of its recovery. Finish with observed event, path state and file evidence; a logrotate version string is insufficient.

Check the installed Logrotten build and its help. The relevant preconditions include control of the log directory entry/parent needed for rename, a matching privileged rotation operation and creation/compression behavior that can follow the substituted path. Merely writing to a log file does not establish control over its directory.

Read the actual logrotate stanza, invocation identity and observed schedule. Distinguish `create`, `copytruncate`, compression and delayed compression. Debug/config inspection is not a rotation and cannot demonstrate that the race succeeds. Do not force rotation of unrelated system logs to make a test happen.

The historical implementation's default destination is `/etc/bash_completion.d`; that is a consequential write location, not a harmless output directory. Its advertised `-t` path branch has an uninitialized string-buffer issue in the reviewed legacy source. Do not assume `-t` makes that build a reliable safe sandbox. Use a reviewed corrected build or a disposable guest whose default destination is explicitly part of the fixture.

See [upstream usage](https://github.com/whotwagner/logrotten) and [implementation](https://github.com/whotwagner/logrotten/blob/master/logrotten.c) when identifying the exact build.
