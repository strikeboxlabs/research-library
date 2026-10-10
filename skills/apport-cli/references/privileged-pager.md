# Assess and exercise a permitted report pager

Use for an explicitly authorized assessment of a sudo-permitted Apport report viewer. Required inputs are the effective sudo rule, its allowed executable/arguments and RunAs identity, installed distro/package revision, an authorized running process or report, and an interactive terminal. Report collection can include private process/configuration data; select those inputs deliberately. This procedure retains the actual report-view and shell branch, not just the policy review.

## Establish applicability

~~~bash
sudo -l
apport-cli --version
dpkg-query -W -f='${Package} ${Version}\n' apport
~~~

Use the observed allowed path as `apport_bin`; the command name used for discovery need not be the same binary. A path-only sudoers grant can allow arbitrary arguments; an argument-constrained grant may not permit `-f -P`. `(ALL : ALL)` names RunAs possibilities, but still requires matching policy/authentication. A sudo-group membership alone is not the grant.

For CVE-2023-1326, unpatched Apport invoked through sudo/pkexec ran its report pager without dropping privilege. The supported case additionally needs a pager with command execution, such as ordinary less, and a usable terminal. Upstream fixed the pager launch by running it as the originating user. Ubuntu backports mean **2.20.11 alone does not establish vulnerability**: Focal's fixed package begins at `2.20.11-0ubuntu27.26`, Jammy's at `2.20.11-0ubuntu82.4`. Compare only within the actual release/package lineage and inspect modified builds separately. See [Ubuntu's release-specific status](https://ubuntu.com/security/CVE-2023-1326) and the [upstream identity-drop change](https://github.com/canonical/apport/commit/e5f78cc89f1f5888b6a56b785dddcb0364c48ecb).

The selected pager is resolved by sensible-pager and its environment/installation. Do not assume less, or strip secure-mode settings just to reproduce a walkthrough. `LESSSECURE=1` normally disables less shell/editor commands; newer builds can selectively re-enable features through `LESSSECURE_ALLOW`. The actual inherited configuration and pager process identity matter more than a filename or prompt.

## Collect, view, and check the actual child

Select a current authorized PID rather than copying a historical number:

~~~bash
ps ux
ps -ww -p "$pid" -o pid=,ppid=,euid=,ruid=,lstart=,args=
~~~

Define `pid` from the selected row before the second command. `ps ux` includes this user's processes without controlling terminals, not every system process. A user's `systemd --user` is different from PID 1. Recheck a changed/vanished process before collection.

When the rule permits the operation and the task calls for this privileged collection:

~~~bash
sudo -- "$apport_bin" -f -P "$pid"
~~~

Answer collection questions for the selected task; do not automatically include modified system files. At the resulting menu select **View report** (commonly `V`). The information is passed to the pager; merely reaching the menu is not evidence that its child retained privilege. A preexisting authorized report can instead use `-c "$report"` if allowed by the rule, with the same collection/display caveats.

Inside an identified less pager which supports shell commands, a bounded identity query is:

~~~text
!id
~~~

This is a **less command**, not a Bash history expansion or Apport menu choice. Record the observed numeric IDs. An unprivileged result is compatible with a fixed Apport even if the parent collected as root. A command-disabled message means this pager's shell branch is unavailable; do not interpret it as proof about every other program feature. A short display that exits without an interactive pager or a broken/non-TTY input leaves this particular test incomplete; don't change global terminal/pager settings to force it.

If the authorized task specifically requires an interactive shell from the demonstrated vulnerable branch, enter in that same less session:

~~~text
!/bin/bash
~~~

Use the actual installed intended shell if `/bin/bash` differs on the controlled image. Check `id`, `id -u` and `id -ru` inside it before attributing authority. A shell can drop differing effective/real IDs; privilege must be observed, not inferred from the parent's RunAs. UID zero remains scoped by namespaces and other restrictions. Perform the selected work, `exit` back to less, `q` out of the pager, and **Cancel** the report interface. Track any local report created; don't choose Send or Ignore as cleanup.

Finish with policy, full package/release, pager/terminal conditions, actual child identity and selected effect. A blocked menu, patched identity drop or disabled shell command can be a useful negative result; it is not a universal host-security verdict. No crash, bug submission or security-setting change is needed merely to establish the pager boundary.
