---
name: chntpw
description: List Windows local accounts and edit selected SAM account settings on an offline hive copy.
---

# chntpw offline SAM editing

Read this entire SKILL.md before acting. Define `sam` as a consistent, offline copy of the raw SAM hive, not a `.reg` text export; preserve the original. List accounts before selecting an edit and explicitly save only the intended changes. Finish with the selected RID, requested change, save outcome and post-edit listing; a successful offline edit does not prove a working login.

## Installed implementation

Use `/usr/sbin/chntpw` (package 140201-1.3). Its help advertises NT3.x through Windows 8.1 and 32/64-bit support; this is not a compatibility guarantee for newer Windows formats or account types. No service setup is needed.

## Listing accounts

~~~bash
/usr/sbin/chntpw -l "$sam"
~~~

The listing identifies local accounts by name and hexadecimal RID, with account state information. Record the intended RID before editing. An unreadable hive or incomplete listing is a failed prerequisite; diagnose the input or obtain a consistent copy before proceeding.

## Interactive edit of one account

Define `user` as the selected name or RID, such as `0x3e9`:

~~~bash
/usr/sbin/chntpw -u "$user" "$sam"
~~~

Use the displayed account menu to clear the password, unlock/enable the account or change group membership as requested. Alternatively, `/usr/sbin/chntpw -i "$sam"` opens the menu for selecting accounts interactively. Follow the available menu labels rather than assuming fixed option numbers. The registry editor (`-e`) is a separate mode and is not needed for these account edits.

Quit through the normal menu and confirm the save prompt to write the edited hive copy, then re-open it:

~~~bash
/usr/sbin/chntpw -l "$sam"
~~~

## Interpreting results

- A password-clear message describes an offline reset, not recovery of the old password or proof that a blank-password login is permitted. Account type, policy and the running system still matter.
- Distinguish an in-memory edit from a successful save. After an abnormal exit, inspect the copy and recorded output rather than assuming either a saved change or corruption. Retain the untouched original separately.
- SAM describes local accounts; domain-account passwords and cached domain credentials require different artifacts and procedures.
- `-N` restricts writes to same-length overwrites and `-E` prevents hive expansion. These allocation constraints do not prevent logically destructive account changes or replace a backup.
- `-L` logs changed filenames to `/tmp/changed` and, according to the installed manual, saves without prompting. Leave it out of the interactive confirmation workflow above; it is not merely an extra report option.
