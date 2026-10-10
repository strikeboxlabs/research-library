---
name: apport-cli
description: Collect or view selected Ubuntu Apport problem reports and assess a privileged report pager. Use when a sudo grant, terminal-dependent View report branch or distro backport changes the process identity.
---

# Apport reports and the pager boundary

Read this entire SKILL.md before acting; reuse complete current context. Select the intended process/report and collection scope. For a privileged invocation or CVE-2023-1326 assessment, read [privileged report paging](references/privileged-pager.md) fully before that procedure. Finish with the collected/viewed report or observed pager identity and its conditions; a sudo listing or version string alone is not proof of privileged execution.

Use the installed `apport-cli --help` and `apport-cli --version`. For patch assessment, obtain the full installed distribution package revision as well as the upstream version. Apport is Ubuntu's problem-reporting system; its availability on another Debian-derived image must be established rather than assumed.

For a selected running process, define `pid` as its current decimal PID and `report` as a fresh private path ending in `.apport`:

~~~bash
umask 077
apport-cli -f -P "$pid" --save "$report"
~~~

`-f` reports a non-crash problem; `-P` selects the running program. This gathers operating-system/package/process information and may execute installed collection hooks or ask whether to include changed configuration. It does not deliberately crash the process. Confirm its identity/start time first; do not reuse an old PID or automatically include unrelated private files. `--save` keeps the report locally instead of reporting it to a bug tracker. Require a successful collection and the intended file, not merely a progress banner.

To open one existing authorized report, define `report` as its actual `.apport` or `.crash` path:

~~~bash
apport-cli -c "$report"
~~~

This enters a reporting interface, not a passive text-only viewer; it can collect further information. Select **View report** for local review, then **Cancel** when done. **Send report** uploads and can open a browser; **Keep report** saves for later; **Ignore future crashes** changes suppression state. Follow the actual menu, not a scripted string of keystrokes. Do not upload or change suppression as part of a task that only asks for local inspection.

No arguments processes pending crash reports, which is broader than selecting one. Missing/vanished process, unavailable package metadata, collection refusal and a denied report read are distinct failures. A report can omit large or binary data from the display; the pager's shown text is not the complete serialized artifact. Retain only the evidence needed for the requested diagnosis.

Consult the [Apport options](https://manpages.ubuntu.com/manpages/jammy/man1/apport-cli.1.html) for the installed release's collection/save behavior.
