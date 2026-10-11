---
name: ansible-galaxy
description: Inspect the installed Ansible Galaxy CLI and selected local role directories; distinguish reported versions, missing metadata and configuration differences from role execution or installation success.
---

# Inspect local Ansible roles

Read this entire SKILL.md before acting; reuse complete current context. Use an installed `ansible-galaxy` under the intended account and trusted configuration. This task requires an existing selected role-parent directory and fresh private report/error paths. Inspect version/configuration and local role-list diagnostics below. Finish with the actual search paths, reported role versions and coverage gaps; no role installation or playbook run is part of this inventory.

Establish which executable, interpreter and configuration this invocation reports:

~~~bash
ansible-galaxy --version
ansible-galaxy role list --help
~~~

Use the installed help to confirm the role-list options. A wrapper, another account or a different working directory can select a different configuration or interpreter. Do not transfer this invocation's paths to a privileged wrapper without separate evidence. An Ansible/plugin error mentioning both system packages and a different Python/Jinja2 environment calls for resolving those exact versions and paths, rather than assuming every role is broken.

Define `roles_dir` as the selected existing parent directory, and `report`/`errors` as fresh absolute file paths. Listing inspects local role metadata:

~~~bash
umask 077
(set -o noclobber
 ansible-galaxy role list --roles-path "$roles_dir" >"$report" 2>"$errors")
status=$?
~~~

Read path labels and stderr alongside the status. Current upstream role listing can warn about unusable directories while returning success; roles lacking recognized metadata can be omitted, and an unknown version is not proof of an unversioned or corrupted installation. This list is neither a complete filesystem inventory nor an integrity check. If the requested role is absent, inspect the selected directory and its metadata as local files before concluding it is absent from other configured paths. Collection listing is a different task with different path-selection behavior.

An installation message establishes only what that installation operation reports. It does not establish that a role or dependency ran, or that a playbook completed. A playbook that reaches fact gathering or an individual task still needs its own task results and final recap. Keep that execution evidence separate from this inventory.

Finish with the selected account/configuration, searched role paths, names and versions actually reported, warnings and the remaining metadata or environment question. A missing executable or unreadable directory is a concrete inventory gap; installing packages or retrying with greater privilege is a separate action.

See the [CLI options](https://docs.ansible.com/projects/ansible/latest/cli/ansible-galaxy.html) and [upstream role-list implementation](https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py) when installed behavior differs.
