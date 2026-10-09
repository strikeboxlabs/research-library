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

Documentation reviewed 2026-10-09; Linux execution untested. Case: Bamboo pp. 7–12. Sources: [LinPEAS guidance](https://github.com/peass-ng/PEASS-ng/blob/master/linPEAS/README.md), [current flag implementation](https://github.com/peass-ng/PEASS-ng/blob/master/linPEAS/builder/linpeas_parts/linpeas_base/0_variables_base.sh), [shared file caching](https://github.com/peass-ng/PEASS-ng/blob/master/linPEAS/builder/linpeas_parts/linpeas_base/2_caching_finds.sh).
