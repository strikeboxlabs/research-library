---
name: rlwrap
description: Add local Readline editing to an existing interactive CLI with rlwrap. Use when a simple nc or other terminal client lacks line editing, while keeping history and remote PTY behavior separate.
---

# Wrap the selected local interactive client

Read this entire SKILL.md before acting; reuse complete current context. Select the already authorized program/arguments, require a real local input terminal and decide whether its input may be saved. Finish with the wrapped command's result and terminal/session state, not a claim that the remote peer gained a PTY.

Define `program` as the verified local executable. Append its reviewed arguments after it; options before the command belong to rlwrap:

~~~bash
rlwrap --version
rlwrap -H /dev/null -- "$program"
~~~

`-H` selects the history file; `/dev/null` avoids keeping input in rlwrap's ordinary per-command history file. It does not erase shell/peer logs or provide secret input handling. For deliberately retained history, use an existing private directory and selected history path; don't silently reuse a sensitive previous command's file. Output logging with `-l` can also capture echoed input.

rlwrap runs the command and interposes local line editing/history/completion. Wrapped nc may still carry a raw remote shell stream with no job control, terminal size propagation or reliable password echo behavior. Establish a remote PTY separately when the authorized task requires one. Do not force `--always-readline` or `--always-echo` to fix every prompt: the child can request direct/raw input or disable echo, and overriding it changes input/password handling.

When stdin is not a terminal, rlwrap simply executes the command without useful Readline editing. Prefer the unwrapped program for automated finite pipes or binary protocol bytes. A wrapper prompt/history error is distinct from a transport or child failure. rlwrap normally returns the child's status, or a nonzero wrapper error; preserve which failed. Stop the tracked wrapped session, checking owned child lifetime rather than accumulating listeners.

Reference: [upstream manual](https://github.com/hanslub42/rlwrap/blob/master/doc/rlwrap.man.in).
