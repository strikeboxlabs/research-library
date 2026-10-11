---
name: screen
description: Inspect and resume GNU Screen sessions with understood ownership and lifecycle. Use when detached versus attached sessions, terminal errors or multiuser access makes reattachment ambiguous.
---

# Identify the session before attaching

Read this entire SKILL.md before acting. Identify the actual Screen executable, account and selected session; use the conditional attached/multiuser cases only when needed. Finish with session state and process identity or the concrete binary, terminal or access prerequisite gap.

Check `screen --version` and list sessions as the intended account:

~~~bash
screen -ls
~~~

Record the full session identifier, owner, host and attached/detached state. A session named `root` is only a label; it does not establish the shell's effective UID. Socket directories vary by package and `SCREENDIR`, so do not hardcode `/var/run/screen` or assume an inaccessible directory is empty. An unreachable/stale socket is not proof of a running session.

If more than one Screen executable is installed, check shell resolution with `command -v screen` and the selected executable's version/help. A version observed at one pathname does not describe another binary found through `PATH`. Define `screen_binary` as the actual inspected absolute executable path and use `"$screen_binary" -ls` for that installation; do not repair a version mismatch by changing socket permissions or enabling setuid.

Define `session` as an exact observed session identifier belonging to the task. For a detached session:

~~~bash
screen -r "$session"
~~~

If it is already attached, decide whether sharing is intended before using `screen -x "$session"`. That adds another display; `-d -r` detaches the other display, and `-D` combinations can log it out. Avoid `-R`/`-RR` as a blind recovery shortcut because they can create or choose a session when the intended one was not found.

Attaching joins live programs and input. Confirm the selected window/process before typing; a displayed prompt may belong to a different account or an application rather than a shell. The default detach key is Ctrl-A then D. Detaching leaves programs running. Exiting the shell or issuing a session-wide quit has different consequences; do not use either as a synonym for disconnecting.

A usable terminal and accurate `TERM` are needed. Setting `TERM=xterm` does not create a PTY or guarantee that xterm describes the actual terminal. Resolve the terminal allocation/capabilities when Screen reports a terminal error.

Cross-user `owner/session` attachment is conditional on the build's multiuser support, installation privileges and the session ACL. The documented cross-user mechanism requires setuid-root support. Backdoor's successful attachment demonstrates that lab's configuration, not universal access to root sessions. Inspect established access instead of changing socket permissions, enabling setuid or granting ACLs to force attachment.

Finish by detaching and checking the intended session remains in the expected state. Report session visibility, successful attachment and the observed process identity separately.

Resolve installation and session options with the [GNU Screen manual](https://www.gnu.org/software/screen/manual/screen.html).
