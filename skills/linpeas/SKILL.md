---
name: linpeas
description: Use a reviewed LinPEAS build for scoped Linux enumeration and verify its findings manually. Use when broad checks, authentication attempts, network lookups or color-coded output could obscure the actual permissions evidence.
---

# Select checks before running the collector

Use a saved, reviewed PEASS-ng release/script and retain its revision or checksum. Inspect `sh "$linpeas_script" -h` after defining the absolute script path. Option names and check groups change; old abbreviations may not select the intended group. Do not pipe an unreviewed download directly into a shell.

For a bounded first pass, define `seconds` as the observation budget and `report` as a new private output file. On a build supporting these exact options and group name:

~~~bash
umask 077
timeout --signal=INT "$seconds" sh "$linpeas_script" -s -n -N -o system_information > "$report" 2>&1
~~~

`-o` selects a check group, `-s` skips some expensive work, `-N` removes color and `-n` disables the described external hostname/IP reputation/leak checks. These switches are not a sandbox or a universal guarantee of no network/disk effects. Review the selected build/checks when those effects matter. Group selection can still run shared setup; some other groups perform broad filesystem caching. Run as the account whose visibility is being investigated rather than adding root to hide permission gaps.

Do not equate `-a` with harmless completeness. The reviewed implementation enables extra checks, process monitoring, `su` password guessing and online vulnerability lookup. `-P` supplies a password for authentication attempts; `-V` sends package/kernel inventory for an online lookup. Network discovery/scanning flags add another activity. Choose them only for the corresponding task, not to improve a quiet report. README wording and the installed implementation can differ.

Capture stderr and completion status. A timeout or missing helper leaves incomplete coverage; a normal exit does not prove every embedded check succeeded. The report can contain credentials and private configuration. Use debug output for a specific unexplained gap instead of rerunning all checks more aggressively.

Treat highlights as leads. Bamboo's writable PATH entry describes the collecting user's environment, not a privileged process's PATH. Establish the actual privileged invocation and inspect the exact file plus containing-directory permissions. File-content writes and directory-entry replacement are different rights. The observed absolute `/bin/sh /path/server-command` execution demonstrates a writable-script issue, not PATH lookup. Finish with evidence for the specific finding and what remains unobserved.


## Verify an unfamiliar SUID finding

`Unknown SUID binary!` is the collector's classification, not proof of a vulnerability or absence from the package database. Preserve the exact helper path: a desktop program, its privileged helper and a similarly named authentication utility can have different behavior.

Define `binary` as the verified absolute regular-file path, resolving any symlink deliberately. Inspect it without invoking the helper:

~~~bash
stat -c '%A %a %u:%g %n' -- "$binary"
findmnt --target "$binary" --output TARGET,OPTIONS
~~~

Retain mode, numeric owner/group and the containing mount from the relevant execution namespace. The SUID bit and root ownership do not alone establish a successful privileged transition: `nosuid`, the caller's `no_new_privs` or tracing can suppress it, and program logic can drop privilege. Missing mount/process evidence leaves that condition unknown.

Map the exact file to its installed package and complete vendor version, then check the advisory's affected helper and distribution fixes. A parent's `--version` output or a version embedded in a directory name is only a lead; invoking an unreviewed privileged helper for help/version still executes it. Separately retain any actual UID/effect evidence. A tool's success banner, or an intermediate error line, alone does not establish the final result.

Use the [SUID check implementation](https://github.com/peass-ng/PEASS-ng/blob/master/linPEAS/builder/linpeas_parts/8_interesting_perms_files/1_SUID.sh), [Linux exec credential rules](https://man7.org/linux/man-pages/man2/execve.2.html), [stat fields](https://man7.org/linux/man-pages/man1/stat.1.html) and [findmnt target selection](https://man7.org/linux/man-pages/man8/findmnt.8.html) to resolve these distinctions.
