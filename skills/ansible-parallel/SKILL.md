---
name: ansible-parallel
description: Run reviewed independent Ansible playbooks concurrently with Julien Palard's ansible-parallel wrapper. Use when overlapping state, missing interactive input or a combined progress/status report makes a batch result misleading.
---

# Run an explicit reviewed playbook set

Read this entire SKILL.md before acting. Require the installed wrapper and compatible ansible-playbook, reviewed playbooks/inventory/configuration and authority for every affected host/change. Establish that the selected plays can run concurrently. Finish with each playbook's host recap/errors and requested state; missing runtime, credentials or recap leaves that part incomplete.

Inspect `ansible-parallel --help`, the installed distribution metadata and `ansible-playbook --version`. The child's version is not the wrapper's version. Establish its effective Ansible configuration, inventory, identities and privilege settings before running; a filename suffix does not constrain a playbook's effects.

Define `playbook_a` and `playbook_b` as distinct absolute paths to reviewed independent plays with explicit approved targets and prepared noninteractive credentials. Use a fresh private `log` path:

~~~bash
umask 077
(set -o noclobber; ansible-parallel "$playbook_a" "$playbook_b" > "$log" 2>&1)
status=$?
~~~

Explicit files avoid admitting an unexpected newly dropped .yml file through a wildcard. Validate any forwarded Ansible options against the installed wrapper's argument parsing; remaining options are passed to each child. `--check` is Ansible check mode, not a sandbox or a guarantee that no plugin/module performs an effect.

The documented implementation launches a separate ansible-playbook for each file; it does not establish ordering between them. Use sequential plays when one consumes another's changed state or both contend for the same resource. Child stdin is closed, so an interactive password prompt is not a reliable authentication plan.

The progress display uses terminal controls and the final report is grouped by playbook. Preserve the raw log, then read each host's failed/unreachable/skipped/rescued/ignored result in context; a task named like a service check can still start or enable that service. No recap after a launch/parse error is not success. Diagnose the failed child before selecting a bounded retry; do not blindly rerun successful changes alongside it.

The reviewed release returns the sum of child exit codes. A shell status does not retain every child's reason and can be truncated by the process-status interface; retain per-playbook errors as completion evidence. A zero changed count is not proof the requested task ran: skipped/check-mode work and unavailable hosts need separate interpretation.

Use the maintainer's [package description and releases](https://pypi.org/project/ansible-parallel/) for wrapper behavior and the installed release source when its reporting/argument behavior differs. Tool installation and scheduler/privilege changes are separate tasks.
