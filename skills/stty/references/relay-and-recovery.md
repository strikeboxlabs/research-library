# An interactive relay needs two terminal decisions

A remote `script -q -e -c /bin/bash /dev/null` or reviewed Python PTY child supplies a remote TTY. Confirm that shell exists and the child is running before adjusting the local terminal. Local echo plus remote PTY echo can duplicate input; local canonical buffering can delay keystrokes. Raw mode is useful only when that is the intended relay behavior.

For a manual Bash session with job control, suspend the known relay using its local suspend key while local signal processing still works. Inspect `jobs -l` and choose that exact job. In the same parent shell, define `relay_job` as its job specification and use the saved `tty_state` from SKILL.md:

~~~bash
stty raw -echo </dev/tty
fg "$relay_job"
stty "$tty_state" </dev/tty
~~~

The restore command runs when the foreground job returns. Keep a recovery route to the local terminal: in raw mode Ctrl-C/Ctrl-Z can become bytes delivered to the remote child rather than signals controlling the local relay. Do not put `fg` inside a subshell or run this recipe in a worker shell with no jobs; it requires the original interactive shell's job table. If the relay ends with a damaged terminal, execute the saved restoration command in that local shell (carriage return may be necessary); use `stty sane` only when the saved state is unavailable. A separate session can use `stty -F "$owned_tty_device" "$tty_state"` for the explicitly identified same device, if permitted.

Set dimensions on the remote PTY only after measuring the actual local rows/columns. For defined positive `rows` and `columns`, `stty rows "$rows" cols "$columns" </dev/tty` operates on the terminal where it is run. Preserve/restore dimensions separately. Choose a `TERM` value supported by both the actual emulator and remote terminfo, rather than blindly copying `xterm`. Verify the intended application behavior and exit the child before closing the relay. An SSH session with managed terminal forwarding can be simpler when available.
