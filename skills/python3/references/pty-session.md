# Give a selected Unix child a pseudo-terminal

Use this branch when an already authorized shell/program channel reports no terminal or cannot use an expected terminal-dependent interface. Require a Unix Python environment with `pty`, an interactive input path and the selected executable; creating a PTY does not repair network reachability or grant another identity.

Define `python_bin` as the trusted Python 3.9+ interpreter and `child_bin` as the verified absolute executable on that same machine. For the selected interactive child:

~~~bash
"$python_bin" -c 'import os, pty, sys; status = pty.spawn([sys.argv[1]]); sys.exit(os.waitstatus_to_exitcode(status))' "$child_bin"
~~~

`pty.spawn` runs this child in a pseudo-terminal and copies data between it and the parent's input/output. It returns a wait status; converting it avoids reporting raw wait bits as an exit code. Adapt only reviewed child arguments, and expect its own startup files/policy to apply. Importing pty is not a Windows PTY compatibility mechanism.

Check the resulting child with its normal harmless terminal/identity query, such as `tty` and `id` for a shell. A `/dev/pts/...` result is evidence of that child-side terminal, not a different effective UID or full terminal emulation on the connecting client. Local Readline editing, terminal size, echo and signal forwarding remain separate; don't send local job-control keys assuming the remote child receives them.

Parent stdin EOF does not necessarily terminate a child that still waits for input; the documented copy loop can remain running. Use the owned session's total runtime budget and track the child rather than treating a quiet channel as success. Exit the intended child and restore any terminal state changed by your actual procedure. No blanket stty/background/listener ritual is required when the selected task does not need it.

Reference: [Python pty.spawn and status/EOF behavior](https://docs.python.org/3.12/library/pty.html).
