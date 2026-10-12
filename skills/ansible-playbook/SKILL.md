---
name: ansible-playbook
description: Check a selected reviewed local Ansible playbook and interpret parse errors or backup definitions. Use when YAML acceptance, collection resolution, link handling or a partial task result is confused with completed execution.
---

# Check the selected local playbook

Read this entire SKILL.md before acting. Require a reviewed playbook, its roles/includes and a trusted Ansible configuration and plugin environment. For a copy/archive/cleanup definition, read [backup semantics](references/backup-semantics.md) fully before interpreting it. Finish with the actual check status and unresolved dependency or parse error; syntax acceptance does not establish task execution.

From the reviewed working directory, inspect `ansible-playbook --version` and `ansible-playbook --help` for executable/interpreter/configuration and supported options. Loading untrusted plugins or lookups is executable behavior even when task execution is disabled. Keep acquired definitions as text until those dependencies are understood.

For a reviewed local-only play whose host pattern is `localhost`, define `playbook` as its absolute path, `config` as the trusted configuration file and `report` as a fresh private output path:

~~~bash
umask 077
(set -o noclobber
 ANSIBLE_CONFIG="$config" ansible-playbook -i 'localhost,' --syntax-check "$playbook" >"$report" 2>&1)
status=$?
~~~

Read diagnostics with the status. Invalid YAML, a scalar instead of a list of plays, a missing role and an unresolved collection module require different corrections. An offending-line excerpt can expose input content; it is neither a complete file dump nor an executed task result. Preserve private diagnostics rather than passing unrelated sensitive files to the parser.

A successful syntax check leaves runtime paths, permissions, variables and host state unverified. `--check` is a different mode that asks modules to predict changes; it is not a sandbox. For any separately authorized execution, retain per-host task results and the final recap, including skipped/failed/unreachable work and independently verified requested state.

Reference: [ansible-playbook options](https://docs.ansible.com/projects/ansible/latest/cli/ansible-playbook.html).
