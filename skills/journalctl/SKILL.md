---
name: journalctl
description: Read recent journal entries for one selected systemd service with journalctl. Use when a status script, unit filter, pager or restricted journal access obscures what the displayed log actually covers.
---

# Read the selected service journal

Read this entire SKILL.md before acting. Require a trusted installed journalctl, the exact service unit and permitted journal access. No conditional resources are required. Finish with selected filters, returned entries, diagnostics/status and coverage gaps; a short excerpt is not complete service history.

Confirm `journalctl --version` and local help. Set `unit` to the observed service name, including `.service`, without wildcard patterns. Read a finite recent slice:

~~~bash
journalctl --no-pager --unit="$unit" --lines=5
status=$?
~~~

Preserve stderr and status. The limit selects entries, which can render across several physical lines. Unit selection can include manager messages about that unit, not only messages emitted by its process. Without a boot/time restriction, recent retained entries can span boots.

No entries can reflect filters, retention or access restrictions; it does not establish that the service never logged. Use the task's selected journal-access mechanism rather than changing account groups as a diagnostic. A wrapper piping journalctl into another command can hide producer failure; retain the journalctl result separately.

`--no-pager` keeps this task outside an interactive pager. Historical pager behavior depends on the installed release, terminal, environment and secure-mode handling; a privileged parent does not independently establish a pager child's identity. Reading logs does not require a pager shell or configuration change.

Reference: [systemd journalctl documentation](https://github.com/systemd/systemd/blob/main/man/journalctl.xml).
