---
name: adduser
description: Provision one approved local Linux account with Debian/Ubuntu adduser and distinguish its primary group, configured hooks, partial creation and effective sudo rights.
---

# Create the selected account

Read this entire SKILL.md before acting. Require an explicit account-provisioning task, an approved account name and administrative authority on the selected Linux image. Confirm the installed implementation and local account policy before changing it; BusyBox adduser is a different interface. Finish with the resulting account, home and groups, or the exact incomplete step.

Define `account` as the approved new local account name. Inspect `adduser --version`, the local manual, `/etc/adduser.conf`, configured skeleton files and any local provisioning hook. A build or backup containing similarly named files does not configure this system. Check whether the account and same-named group already resolve:

~~~bash
getent passwd "$account"
getent group "$account"
~~~

These are NSS lookups, which can include directory identities. Check status and the selected local account files as needed: a failed lookup is not proof that an unavailable directory has no collision. Resolve existing accounts/groups instead of selecting a conflicting UID or forcing a rejected name.

For a normal interactive account using the reviewed Debian/Ubuntu defaults and an approved sudo session:

~~~bash
sudo -- adduser "$account"
status=$?
~~~

Follow the approved password policy through the interactive prompt; keep passwords out of arguments and logs. This operation can create an account, primary group and home, copy skeleton files and execute a configured local hook. Review those effects before invocation. A one-name invocation selects normal-account creation; a two-name invocation instead adds an existing user to an existing group.

Inspect the final status and messages, then verify the selected result:

~~~bash
getent passwd "$account"
id "$account"
~~~

Check that the returned UID, primary/supplementary groups, home and shell meet the requested policy, and inspect the created home. A success status can describe an already existing compatible account in some versions; compare with the pre-change observation. A late password or hook failure can leave earlier account/home changes behind. Inspect the partial state before retrying; do not automatically delete a home or force another creation.

A same-named primary group is not an administrative grant. Effective privileges depend on local policy and memberships. Do not infer sudo rights from an account name, group name or login greeting, and do not create a specially privileged name as a diagnostic probe. Check effective sudo policy separately when privilege validation is part of the provisioning task.

For service accounts or password-disabled creation, select the installed version's documented options and the requested login mechanisms first. A locked password alone need not prevent SSH-key login. Missing implementation, policy, identity availability or administrative authority is an unresolved prerequisite, not successful provisioning.

References: [Ubuntu adduser manual](https://manpages.ubuntu.com/manpages/jammy/man8/adduser.8.html), [getent and NSS lookup status](https://manpages.ubuntu.com/manpages/jammy/man1/getent.1.html).
