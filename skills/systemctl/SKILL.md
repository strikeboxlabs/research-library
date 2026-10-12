---
name: systemctl
description: Inspect selected systemd services and timer activations or manage an owned unit. Use for startup failures, effective configuration and start, stop, reload, restart or daemon-reload decisions.
---

# Explain the unit state before changing it

Read this entire SKILL.md before acting. Read [timer activation](references/timer-activation.md) fully for a scheduled task and [service changes](references/service-changes.md) fully before a start, stop, reload, restart or unit-file change. Establish the exact manager/unit and required observation first. Finish with relevant state and application result; command completion alone is not service health.

Use the system manager by default. For a user service, add `--user` consistently to every systemctl command and use that user's session context; a missing user bus is not evidence that the system service is absent. A container/chroot without a running systemd manager needs a different control path.

For a historical version or vulnerability claim, retain `systemctl --version` including the distribution package suffix and compiled features. An upstream-looking release number alone does not establish the vendor's patch status or the effective pager configuration. Compiled support is separate from a selected unit's enabled restrictions.

Set `unit` to the exact unit name, including `.service` or the intended instance:

~~~bash
systemctl --no-pager --full status "$unit"
systemctl show "$unit" -p LoadState -p ActiveState -p SubState -p Result \
  -p MainPID -p ExecMainCode -p ExecMainStatus -p FragmentPath -p DropInPaths
systemctl --no-pager cat "$unit"
journalctl -b -u "$unit" -n 100 --no-pager
~~~

`status` can return nonzero for an inactive/failed unit; still read its evidence. `show` exposes structured current properties; `cat` shows backing files and drop-ins on disk, which can differ from the manager's loaded configuration. Use the journal's failure immediately preceding repeated restarts, not merely the last rate-limit message. Journal access errors or rotation can leave the original cause unavailable.

The commands above suppress the interactive pager. When elevation is needed, check the exact sudo command and argument restrictions before adding flags: a grant for a particular `status` invocation may reject an added `--no-pager`. Record that policy limitation and obtain an approved way to capture the required status; do not weaken pager security or assume a privileged caller grants arbitrary child commands.

| State/evidence | Interpretation |
|---|---|
| `LoadState=not-found` | Check unit name, manager and installation. |
| Masked unit | An intentional start prohibition; enabling it is not the same as unmasking it. |
| `active (exited)` | May be a successful oneshot with retained state, not a running daemon. |
| `Result=exit-code` with nonzero status | Inspect the program's error and startup context; do not erase it with repeated restart. |
| `start-limit-hit` | Diagnose earlier failures, fix the cause, then deliberately reset the rate-limit state. |

For path/environment problems, inspect `systemctl show "$unit" -p ExecStart -p User -p Group -p WorkingDirectory -p EnvironmentFiles`. A service does not inherit the interactive shell's directory or PATH. Treat serialized ExecStart output as evidence, not a shell command to eval. Inspect permissions and sandbox restrictions when a command succeeds interactively but fails in the unit.

See the [systemctl manual source](https://github.com/systemd/systemd/blob/main/man/systemctl.xml) and [service execution model](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).
