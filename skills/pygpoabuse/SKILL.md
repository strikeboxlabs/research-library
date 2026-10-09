---
name: pygpoabuse
description: Plan and verify a pyGPOAbuse immediate-task test on an isolated lab GPO. Use when command defaults, GPO scope, partial writes or cleanup behavior could affect unintended accounts or policy state.
---

# Establish the complete GPO mutation

Use Hackndo's pyGPOAbuse and inspect the installed revision/help. It writes a scheduled-task XML through SYSVOL and updates directory extension/version attributes plus `gpt.ini`. Selecting a GPO by GUID does not restrict execution to the DC used for the connection; linked scope and policy processing determine affected clients.

Use a dedicated lab GPO whose affected clients and restoration method are known. Confirm actual directory and SYSVOL rights, computer/user half, links and filtering. A BloodHound edge or share listing is a lead, not proof of every required write. Capture the prior XML state (including absence), `gpt.ini`, relevant extension attributes and `versionNumber` before a requested mutation. Without a complete before-state and restore path, stop at inspection.

Define `script` as the reviewed entrypoint, `identity` as `domain/account`, `dc` as the selected DC, `gpo_id` as the verified lab GUID, and `lab_host` as the only intended client FQDN. Define a unique descriptive `task_name`, a truthful `mod_date` in `YYYY-MM-DD HH:MM:SS` format, and a nonempty `proof_command` that produces an agreed harmless local marker. On a build with verified targeting support:

~~~bash
test -n "$proof_command" && python3 "$script" "$identity" -dc-ip "$dc" -gpo-id "$gpo_id" -taskname "$task_name" -description 'Authorized lab validation' -mod-date "$mod_date" -command "$proof_command" -filter-enabled -target-dns-name "$lab_host"
~~~

The password is prompted. Omitting or emptying `-command` invokes a default account-creation/admin command. Computer tasks use SYSTEM; `-user` selects a different policy half/context. Target-name options without `-filter-enabled` do not apply the filter. Verify the generated XML and effective client scope; do not treat a new option as tested confinement.

An existing `ScheduledTasks.xml` causes refusal unless forced. Do not add `-f` automatically. Errors after an XML or LDAP write can leave partial state. The success message establishes tool-side policy writes, not client execution; verify policy application and the marker on the intended client.

**Cleanup is not a complete rollback.** The reviewed `--cleanup` deletes the entire selected half's `ScheduledTasks.xml`; despite its help wording, that path does not restore prior LDAP attributes or versions. It can remove unrelated tasks. Restore only the owned change against the captured state, reconcile concurrent edits, and verify policy/client artifacts separately. Reusing the cleanup switch is not evidence of restoration.

Documentation reviewed 2026-10-09; Linux/AD execution untested. Case: BabyTwo pp. 9–11. Sources: [CLI](https://github.com/Hackndo/pyGPOAbuse/blob/master/pygpoabuse/cli.py), [GPO writes and cleanup](https://github.com/Hackndo/pyGPOAbuse/blob/master/pygpoabuse/gpo.py), [task generation](https://github.com/Hackndo/pyGPOAbuse/blob/master/pygpoabuse/scheduledtask.py).
