---
name: useradd
description: Provision one approved local account with shadow-utils useradd and explicit home, primary group and login shell; diagnose partial creation separately from authentication policy.
---

# Provision the selected account

Read this entire SKILL.md before acting. Require an approved new local account, administrative authority and selected account/home/group policy. Confirm shadow-utils useradd, defaults, skeleton and configured hooks before mutation. Finish with actual account/home/group state and any incomplete step.

Define `account`, `home_dir`, `primary_group` and `login_shell` as approved values; the group must already exist and the shell must be the selected installed executable. Check NSS/local collisions and parent-directory permissions first. Inspect `useradd -D` without additional options to read defaults; adding options can change those defaults.

~~~bash
useradd --help
getent passwd "$account"
getent group "$primary_group"
sudo -- useradd -m -d "$home_dir" -g "$primary_group" -s "$login_shell" "$account"
status=$?
~~~

`-m` creates the home and copies the configured skeleton. Inspect status/messages, then verify `getent passwd "$account"`, `id "$account"` and the home. Late failure can leave partial state; inspect before retrying or deleting anything. Without an initial password option the password starts locked; set it separately through the approved interactive mechanism if required. Do not put password material in arguments.

Choosing `/bin/false` as a shell rejects ordinary shell execution; it does not by itself prove every authentication or SSH forwarding path is disabled. Verify the selected service's account/PAM/forwarding policy separately. Creation grants no automatic administrative rights.

See [shadow-utils useradd](https://manpages.debian.org/bookworm/passwd/useradd.8.en.html).
