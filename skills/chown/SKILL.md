---
name: chown
description: Change ownership of one selected Linux file with GNU chown and verify numeric owner/group afterward. Use when ownership, mode bits and effective access are confused or a recursive script's scope is uncertain.
---

# Change the selected file's ownership

Read this entire SKILL.md before acting. Require the exact path, verified intended owner/group mapping and authority to make the change. Inspect file type and prior numeric ownership; no conditional resources are required. Finish with status, resulting ownership and any required restoration.

Define `file` as one verified regular file under an intended controlled directory, and `new_owner`/`new_group` as established account/group names. Retain its original metadata before the authorized change:

~~~bash
chown --version
stat --format='%F %u:%g %a %n' -- "$file"
chown --no-dereference -- "$new_owner:$new_group" "$file"
status=$?
stat --format='%F %u:%g %a %n' -- "$file"
~~~

Check both status and resulting metadata. This sets owner and group; an owner-only operand leaves the group unchanged, while an owner followed by a bare colon selects its login group. No-dereference affects a symlink itself if encountered, but is not protection against replacement of parent paths. Avoid recursive changes for one-file work. Ownership does not independently establish access, process identity or content integrity. Restore recorded ownership only when restoration is part of the task, then verify it.

Reference: [GNU chown](https://manpages.debian.org/bookworm/coreutils/chown.1.en.html).
