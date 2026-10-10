---
name: chmod
description: Change selected Linux file mode bits and verify the resulting owner/group access. Use when a private artifact needs restricted access or a permission change is being confused with ownership, directory traversal or authentication.
---

# Change the intended file's mode

Read this entire SKILL.md before acting; reuse complete current context. Confirm the selected path, file type, owner and intended access before changing its mode. Finish with the observed mode and relevant access result; chmod does not establish credential validity or server acceptance.

For GNU chmod, inspect `chmod --version` and local help. Define `file` as the actual selected **regular file**, verify it is not an unexpected symbolic link, and retain the prior mode/ownership if restoration is part of the task. For a private key or secret file that its owner must read and write:

~~~bash
chmod 600 -- "$file" && stat --format='%a %U:%G %n' -- "$file"
~~~

Octal `600` gives owner read/write and removes group/other read, write and execute bits on a regular file. Check the result rather than suppressing errors. A reported `600` file owned by another user can still be unreadable to the intended client. chmod changes mode bits, not ownership, and normally requires ownership or appropriate privilege; permission denied calls for correcting the task's access context.

On a symbolic link explicitly supplied as an operand, GNU chmod changes the target's mode. Avoid recursive mode changes when only one artifact is intended: directories require execute/search permission to traverse, and applying `600` throughout a tree can make it unusable. Parent-directory access, filesystem/mount rules and security policy can also affect the consumer despite the file's mode.

For a verified credential working copy, run its format inspection separately and then use it only with the selected authorized client/endpoint. OpenSSH's private-key permissions check, successful key parsing and remote key authorization are separate outcomes. Restricting a file after exposing its contents does not undo that exposure.

See [GNU chmod's packaged manual](https://manpages.debian.org/bookworm/coreutils/chmod.1.en.html) for numeric/symbolic modes, link handling and special-bit behavior. These are Linux permission semantics; a Windows file-mode check is not a substitute.
