---
name: getcap
description: Inspect Linux file capabilities and distinguish stored privilege metadata from effective process authority. Use when a collector flags an interpreter, packet tool or service binary with unexpected capabilities.
---

# Verify the exact file

Check `getcap -h` for the installed libcap options. Define `binary` as the absolute regular-file path actually used by the relevant invocation, resolving symlinks deliberately. Inspect it without launching the suspect executable:

~~~bash
getcap -n -v "$binary"
stat -c '%A %a %u:%g %n' -- "$binary"
findmnt --target "$binary" --output TARGET,OPTIONS
~~~

`-v` includes entries without file capabilities; `-n` reports a nonzero namespace root ID stored with namespaced capabilities. Capture errors separately from a successful no-capability result. An explicit empty capability value `=` differs from an absent capability attribute, notably for ambient capability handling. If discovery is necessary, use `getcap -r "$scan_root"` with an explicitly chosen directory; recursive output covers only accessible paths and must retain traversal diagnostics.

**Illustrative:** `/opt/lab/python3 cap_setuid,cap_net_bind_service=ep` reports capabilities attached to that file, independently of its SUID mode bit. `p` denotes file-permitted capabilities; the file's `e` flag requests that newly permitted capabilities become effective during exec. An `i` flag participates in inheritance rules rather than granting every child unconditional privilege. None of these letters reports the state of an already running process.

Interpret the capability's operation before inferring why it was assigned. `CAP_SETUID` can authorize process UID changes within the governing user namespace. `CAP_NET_BIND_SERVICE` concerns privileged Internet ports; `CAP_NET_RAW` concerns RAW/PACKET sockets. A packet-capture feature does not by itself explain granting arbitrary UID changes to a general-purpose interpreter.

## Check the execution conditions

File metadata alone does not prove a successful transition. The caller's capability sets/bounding set, namespace mapping, `no_new_privs`, tracing, mount `nosuid` and program behavior affect the outcome. The mount query above describes the inspecting process's namespace; verify the actual execution namespace when they differ. A copied file, replaced interpreter or package update can differ from the path/version recorded in an earlier report.

If the relevant process is already running and readable, define `pid` as its verified numeric PID and inspect its current evidence without starting a privileged test:

~~~bash
grep -E '^(Name|Uid|Gid|Cap(Inh|Prm|Eff|Bnd|Amb)|NoNewPrivs|TracerPid):' "/proc/$pid/status"
readlink "/proc/$pid/ns/user"
cat "/proc/$pid/uid_map"
~~~

The capability fields are hexadecimal masks. `CapEff` describes effective capabilities, while `CapBnd` limits potential acquisition and does not establish current possession. Uid/Gid list real, effective, saved and filesystem IDs; changing a UID does not necessarily change groups. This status view concerns the main thread, and capabilities are per-thread. Missing process files, permissions or a PID that exited/reused leave the observation incomplete.

A namespace-local UID 0 is not automatically initial-namespace root. Keep the exact file capability text, current mode, applicable namespace/mount conditions and any separately observed process state. Do not infer a demonstrated privilege change from a collector highlight alone, or run the interpreter merely to obtain help/version output.

Use the [getcap reference](https://man7.org/linux/man-pages/man8/getcap.8.html), [capability/exec rules](https://man7.org/linux/man-pages/man7/capabilities.7.html), [exec suppression conditions](https://man7.org/linux/man-pages/man2/execve.2.html) and [process status fields](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html) to resolve missing conditions.
