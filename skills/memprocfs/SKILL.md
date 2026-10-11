---
name: memprocfs
description: Mount an acquired Windows memory dump on Linux and identify its parsed OS, architecture and coverage. Use for offline incident-response metadata and parser or FUSE initialization failures.
---

# Identify an offline memory image

Read this entire SKILL.md before acting; reuse complete current context. This task requires an already installed trusted Linux MemProcFS build with its matching libraries/data files, working FUSE access, an acquired local dump and authority to handle its contents. Select the dump and private mount point before starting. Finish with parser identity, observed system metadata, input identity and confirmed mount cleanup; a missing dependency or unsupported image is a prerequisite gap. There are no conditional resources for this task.

Define `memprocfs_bin` as the selected executable, `dump` as the absolute path to a protected working copy, and `mountpoint` as an existing empty private directory that is not already mounted. Check the installed help for these options. Keep the original acquisition and its checksum; an extracted dump's expanded size can greatly exceed its archive's size.

~~~bash
"$memprocfs_bin" -device "$dump" -mount "$mountpoint" -disable-python -disable-symbolserver
~~~

`-device` selects the local file here; live devices and remote acquisition are different tasks. `-mount` supplies the Linux FUSE path. `-disable-python` disables Python plugins; `-disable-symbolserver` suppresses automatic Microsoft symbol downloads while retaining available cached symbols. These switches do not make an untrusted executable or arbitrary native plugin safe. Run from the trusted installation's documented working directory when its libraries/data require it. Resolve dependency, image-format or mount-access errors before adding privileges or changing parsing options.

Retain the startup banner and errors. It can establish the parser version and detected Windows kernel version/architecture. A Windows kernel version beginning `10.0` alone does not identify the marketed Windows edition. From another terminal, after successful initialization, read the built-in overview:

~~~bash
cat -- "$mountpoint/sys/sysinfo/sysinfo.txt"
~~~

This read-only virtual file is a selected system summary, not a complete memory inventory. Record the reported input mode, OS build, architecture and parse status; missing fields can reflect acquisition or parser limitations. Treat names, users and network fields as private incident evidence. Do not edit virtual plugin-installation files: saving them can download and install code rather than modify a harmless text note.

For this metadata task, leave batch forensic processing disabled. If the requested overview is unavailable, distinguish missing initialization, incompatible dump/build and incomplete acquired memory; retain the failure instead of treating an empty view as absence of activity.

Close readers and stop the foreground instance using its supported shutdown method. Verify with `findmnt -M "$mountpoint"` that the FUSE mount is gone. If it remains, use the installed FUSE unmount helper for this exact owned mount, then verify again; a busy or inaccessible mount remains an explicit cleanup gap. Preserve the dump and intentional results.

Resolve differences with the upstream [Linux prerequisites](https://github.com/ufrisk/MemProcFS/wiki/_Linux), [CLI options](https://github.com/ufrisk/MemProcFS/wiki/_CommandLine) and [system overview](https://github.com/ufrisk/MemProcFS/wiki/FS_Sys_Sysinfo). Match documentation to the installed build when older wiki text disagrees with its release notes or help.
