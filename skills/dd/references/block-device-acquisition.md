# Acquire an identified offline block source

Use this for one approved, identified offline/quiescent block device or coordinated immutable snapshot, copied into a fresh regular file. Require the exact source identity/capacity, appropriate read access, GNU dd, util-linux blockdev and enough space in an owned destination filesystem. A guessed `/dev/sdb` name is not a source identity. Do not copy a live filesystem and claim application consistency.

Define `device` as its verified absolute block-device path and `output` as a fresh absolute regular-file destination under the selected private directory. Confirm the device against the task's snapshot/device record and make sure the destination is not a device, existing file or symlink. Establish authorized read context before running; these commands do not authorize adding arbitrary privilege.

~~~bash
umask 077
test -b "$device"
blockdev --getsize64 "$device"
dd if="$device" of="$output" bs=1M iflag=fullblock conv=excl,fsync status=progress
~~~

Proceed only after the source check and capacity query succeed, and record the returned byte capacity. `--getsize64` returns bytes; `--getsz` instead returns 512-byte sectors. `conv=excl` refuses an existing destination, and `fsync` requests output synchronization before successful completion. It does not freeze other writers. The source is opened for reading; reversing `if` and `of` would overwrite the wrong object.

Preserve dd status and diagnostics. After success, require a regular nonempty output whose exact byte size equals the recorded source capacity:

~~~bash
stat -c '%s' -- "$output"
sha256sum -- "$output"
~~~

Equal size and an artifact checksum identify the acquired file, not its filesystem health or coherence. Retain source identity, snapshot/quiescence facts, size, capture time and checksum. A partial file from failure is not an accepted image. Do not add `noerror,sync` to hide a failing read: padding changes bytes and requires a separate recovery process with error accounting.

A VM's encrypted container, a guest block device and an encrypted volume inside that device are separate representations. Capturing the guest-visible block device does not preserve the original VDI container bytes. Classify the acquired image, then inspect the actual partition/encryption layout before mounting; `crypto_LUKS` is an encryption container, not the mountable inner filesystem. Do not boot or repair the original merely to make it readable.

Primary options: [GNU dd manual](https://manpages.debian.org/bookworm/coreutils/dd.1.en.html) and [util-linux blockdev](https://github.com/util-linux/util-linux/blob/master/disk-utils/blockdev.8.adoc).
