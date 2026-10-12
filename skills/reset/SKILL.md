---
name: reset
description: Reinitialize a selected owned interactive terminal with ncurses reset. Use when a failed program leaves display, echo or line-processing modes broken and the real terminal type is established.
---

# Recover the selected interactive terminal

Read this entire SKILL.md before acting. Require the identified owned terminal, installed ncurses reset and a supported description of the actual terminal emulator. All instructions are inline. Finish with usable display/input and observed terminal settings; missing TTY or terminfo remains unresolved.

Run in the terminal being repaired. Define `terminal_type` from its established emulator/terminfo, rather than assuming every relay is xterm:

~~~bash
reset -V
reset "$terminal_type"
stty -a </dev/tty
~~~

Inspect errors and verify normal line editing/echo in that session. Reset sends terminal reset sequences and selects conventional cooked/echo modes, disabling raw/cbreak processing. It does not restore an exact saved stty state or create a remote PTY. Local and remote relay terminals require separate decisions; reinitializing the wrong end can break an intentional raw relay.

The terminal type can be prompted for when unresolved; text supplied at that prompt is not necessarily an executable command. Do not feed arbitrary capability output to eval. A worker without an interactive terminal needs its existing terminal facility; piping output to a log does not repair another terminal.

Reference: [ncurses reset/tset behavior](https://manpages.debian.org/bookworm/ncurses-bin/reset.1.en.html).
