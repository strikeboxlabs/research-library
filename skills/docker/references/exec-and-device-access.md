# Execute in a selected running container

Use when a task permits an operation in an existing container, particularly an effective sudo grant restricted to `docker exec`. Preserve the **exact executable path, RunAs identity, allowed argument pattern and daemon context**. A grant for `exec *` does not grant `docker run`, `ps`, `inspect` or changing daemon configuration. Sudoers `*` can span whitespace/arguments; it can therefore admit `--user` and `--privileged` if the actual policy matches. A container hostname is only an ID lead because hostnames are configurable; establish that the selected identifier resolves in this daemon.

Define `docker_bin` as the permitted installed executable, and `container` as the selected running ID/name. Where that root RunAs operation is authorized, a bounded identity command is:

~~~bash
sudo -- "$docker_bin" exec --user 0 "$container" id
~~~

UID 0 is initially **container** identity. The daemon can be remote or rootless; user namespaces, capabilities, device policy and LSMs still constrain it. A running PID 1 is required; a stopped/paused container or absent `id`/shell is a distinct execution failure. Check the immediate command status and diagnostics. This does not establish permission to start/unpause a container or replace its image.

For an authorized privileged command in that same container, with an installed `sh` and interactive terminal:

~~~bash
sudo -- "$docker_bin" exec --user 0 --privileged -it "$container" sh
~~~

`-i` keeps stdin open; `-t` allocates a TTY. Omit `-t` for noninteractive output capture. `--privileged` grants extended privileges to the **new exec process**, not a new persistent container specification or automatic host filesystem mount. In Moby 20.10.24 the exec path gives this process all capabilities but retains the container's AppArmor profile. Device availability/cgroup restrictions and its existing mount namespace remain relevant; do not infer that every ordinary container can open every host block device. Check the deployed version when that distinction decides the task.

## Use an exposed filesystem for the selected task

Inside the exec context, inspect `id`, `mount` and `/proc/self/mountinfo` (or explicit `findmnt` columns if installed). Mount entries showing one block device at `/etc/hostname`, `/etc/hosts` and `/etc/resolv.conf` can be file bind mounts from different subtrees. They do not prove that the device is the host root or even that its device node is accessible here. Correlate an already permitted Docker inspection's `Mounts` source/destination and device/filesystem identities; if `inspect` is outside the grant, retain that missing evidence rather than require a prohibited subcommand.

For an exposed, identified and authorized block filesystem, define `device`, filesystem type `fstype`, empty unmounted directory `mountpoint` and deliberate `options` (`ro` for ordinary inspection, `ro,noload` for a compatible ext3/ext4 snapshot when journal writes must be avoided, or `rw` for the approved file-change task). Do not copy `/dev/sda1` from an example or skip snapshot/coherency requirements for a live filesystem. Execute only after verifying the node exists and the mountpoint is free:

~~~bash
test -b "$device"
mount -t "$fstype" -o "$options" -- "$device" "$mountpoint"
findmnt --kernel --mountpoint "$mountpoint" --output TARGET,SOURCE,FSTYPE,FSROOT,OPTIONS
~~~

Check each prerequisite/status before the next command; inspect `/proc/self/mountinfo` if `findmnt` is unavailable. Successful mount plus selected readable file establishes that observed filesystem access. The existence/mode of a file alone does not establish its contents or provenance. A host-root conclusion needs the filesystem's identity, not a familiar `root/` directory. Read-write access can affect the daemon host even though the process stays in container namespaces. `Operation not permitted` needs capability/LSM/device/user-namespace diagnosis, not an unsupported conclusion that the device is absent.

If the selected task explicitly includes modifying an account's authorized-key file through that filesystem, preserve its actual account/path mapping, existing bytes and metadata, append only the controlled public key and verify file/read-back and separately authorized host login. Do not overwrite all existing keys as a default, copy the private key into the container, or equate a file write with SSH acceptance. Server `AuthorizedKeysFile`, ownership and authentication policy still apply. This is the actual permitted file-change task; mounting only for inspection does not establish it.

Finish with the requested read/change, exec identity, namespace/host attribution and any unresolved prerequisites. Restore temporary file changes as agreed, leave the created mountpoint, and `umount -- "$mountpoint"` only for the mount created for this task; inspect success before exiting the exec shell. Exiting that shell does not necessarily destroy a mount in the container's shared namespace. Do not stop the pre-existing container as cleanup.

See [exec options](https://docs.docker.com/reference/cli/docker/container/exec/), [20.10.24 process privileges](https://github.com/moby/moby/blob/v20.10.24/daemon/exec_linux.go), [rootless Docker](https://docs.docker.com/engine/security/rootless/) and [mount/namespace semantics](https://github.com/util-linux/util-linux/blob/master/sys-utils/mount.8.adoc).
