---
name: passwd
description: Set or change a selected Linux account's password interactively with shadow-utils passwd and interpret password status separately from account or SSH-key access.
---

# Change the selected password

Read this entire SKILL.md before acting. Require an explicitly requested password change, exact local account, installed implementation and authority for that account. Use the approved interactive terminal and local password policy; keep secrets out of arguments, transcripts and reports. Finish with command status and selected account status.

For an administrator changing the approved existing `account`:

~~~bash
sudo -- passwd -S "$account"
sudo -- passwd "$account"
status=$?
sudo -- passwd -S "$account"
~~~

For the current user's own password, use `passwd` without an account argument and follow the current/new-password prompts. PAM and local policy can reject the change; retain the nonsecret error and final status before calling it complete.

In shadow-utils status output, L means locked password, NP means no password and P means usable password. Remaining fields describe password age, warning and inactivity policy. This establishes password state, not a successful login or effective privilege. A locked password can still allow another token such as an SSH key; a shell restriction is also a separate setting. Password deletion makes an account passwordless and is not an equivalent recovery action for a rejected password change.

See [shadow-utils passwd and PAM/status behavior](https://manpages.debian.org/bookworm/passwd/passwd.1.en.html).
