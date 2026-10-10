---
name: omv-rpc
description: Call an installed OpenMediaVault backend with omv-rpc, inspect mounted filesystems and run a selected package installation. Use for local socket/role boundaries, version-specific JSON parameters and asynchronous job output.
---

# OpenMediaVault local RPC

Read this entire SKILL.md before acting; reuse complete current context. Identify the installed CLI/service version and actual session identity. Use the selected read below; before package installation or background-job handling, read [installation and jobs](references/install-and-jobs.md) fully. Finish with the requested data or completed job and its effect, not merely an accepted RPC or status-file name.

Define `rpc_bin` as the verified installed omv-rpc executable. Inspect its `--help`; service/method/JSON contracts must match that image's service implementation. The examples target the upstream 6.x contracts, not every future OpenMediaVault release:

~~~bash
"$rpc_bin" --help
id
"$rpc_bin" -u admin FileSystemMgmt enumerateMountedFilesystems '{"includeroot":true}'
~~~

Require CLI exit success and inspect the returned JSON array. Selected records describe device, mountpoint, filesystem type and used/available space; `includeroot` includes the root filesystem in this enumeration. Mounted/readable inventory is not a grant to mount, reformat or install packages. Retain a transport, role, schema or backend exception separately from an empty successful array.

In the 6.x CLI, `-u admin` constructs an administrator RPC context; it does not perform a password login or change the process's OS UID. The CLI contacts the local engined Unix socket. Socket filesystem permissions and session group membership are therefore consequential trust boundaries. A named-account group lookup is not proof that the running session has those groups or can reach that socket. Keep the current `id` result, actual socket policy and method result together; do not change permissions/groups to turn a denied call into acceptance.

When a method is missing or rejects parameters, inspect the installed RPC service and matching datamodel as text. Do not execute/import its PHP merely to list methods, or extrapolate an admin method from a successful read. Roles, validation and side effects are method-specific. Local backend authority is different from the HTTP web login and from the caller's Unix user name.

References: upstream 6.x [CLI context and error handling](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/sbin/omv-rpc), [engine socket boundary](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/sbin/omv-engined), and [filesystem parameters](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/share/openmediavault/datamodels/rpc.filesystemmgmt.json).
