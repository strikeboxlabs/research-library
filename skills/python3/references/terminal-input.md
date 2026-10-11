# Reproduce a shared-terminal input boundary

Use this only on an owned or explicitly authorized Linux session to determine whether one process can queue input to the same terminal as another shell. Require the actual terminal/session relationship, the intended consumer and a harmless marker command. This procedure can enqueue terminal input; it does not by itself execute a command or change identity.

## Establish the consumer and kernel behavior

Record `tty`, `ps -o pid,ppid,sid,pgid,tpgid,tty,stat,user,comm,args` for the selected processes, real/effective identity and the exact account-switch command. Same tty path supports a shared endpoint but does not prove parentage or who consumes queued bytes. A process-observation timeline is not a process tree. Use a disposable shell with no unrelated input pending.

Current Linux source allows TIOCSTI only when legacy behavior is enabled or the caller has CAP_SYS_ADMIN, and otherwise returns an error; it also restricts callers outside the tty's controlling session. Kernel configuration/sysctl, namespaces, seccomp/LSM policy and a non-terminal fd0 can therefore block it. Record the exact errno/diagnostic. Do not change kernel settings to make the reproduction pass.

Define `marker_command` as a harmless one-line command that writes the consuming shell's real/effective identity to a fresh private path. The Python program must pass each character as exactly one byte:

~~~python
import fcntl
import os
import termios

marker_command = os.environ["MARKER_COMMAND"]
if not os.isatty(0):
    raise SystemExit("stdin is not a terminal")
for byte in (marker_command + "\n").encode("ascii"):
    fcntl.ioctl(0, termios.TIOCSTI, bytes([byte]))
~~~

Run it from the lower-privilege side of the confirmed shared terminal. A zero return establishes that bytes were accepted by the ioctl in this context; observe the selected consumer and marker before claiming execution. Quoting, line editing, foreground process group and pending input can alter what happens. Use ASCII for this small reproduction because terminal encoding/multibyte handling is a separate question.

Some demonstrations stop their immediate parent before queuing input. `os.getppid()` identifies only the immediate parent, not automatically a privileged shell. Do not send SIGSTOP unless that exact owned PID and recovery are established; record its prior state, and send SIGCONT only to that selected PID if the experiment requires it. A stopped intermediate process does not prove a higher-privilege consumer exists.

If util-linux su supports --pty, repeat the authorized account change with a separate PTY. Failure to enqueue or consume across that boundary supports the mitigation under those conditions, not a universal kernel verdict. Restore any selected startup file and marker afterward. Do not replace a global program or leave setuid bits as a terminal test.

See current Linux [TIOCSTI implementation](https://github.com/torvalds/linux/blob/master/drivers/tty/tty_io.c), Python [fcntl.ioctl](https://docs.python.org/3.12/library/fcntl.html#fcntl.ioctl) and util-linux [su --pty](https://github.com/util-linux/util-linux/blob/master/login-utils/su.1.adoc).
