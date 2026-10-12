---
name: qemu-system-x86-64
description: Boot an approved x86-64 Linux kernel and disposable raw root filesystem in QEMU, with serial-console and optional local GDB-stop diagnosis. Use when a controlled guest fixture is needed to distinguish boot, disk and debugger failures.
---

# Boot a controlled Linux guest

Read this entire SKILL.md before acting. Require a trusted bootable kernel, compatible root filesystem, sufficient resources and a disposable guest task. Read [local debugging](references/local-debugging.md) fully when pausing for a debugger. Finish with actual guest kernel/boot evidence and shutdown state; a launched QEMU process is not a booted guest.

Define `kernel` as the absolute boot image and `disk` as an owned disposable raw image; avoid commas in these option paths. Confirm the selected executable's supported machine/CPU/accelerator options:

~~~bash
qemu-system-x86_64 -version
qemu-system-x86_64 -help
~~~

For a guest whose kernel supports the default IDE disk and ttyS0 console:

~~~bash
qemu-system-x86_64 -kernel "$kernel" \
  -drive "file=$disk,format=raw,if=ide" -snapshot \
  -nic none -nographic -append 'root=/dev/sda console=ttyS0'
~~~

The root device must match the image layout: a whole-filesystem image and a partitioned disk need different root arguments. The kernel also needs the selected storage/filesystem drivers. A filename ending in ext2 does not establish its actual filesystem. An initramfs-based guest needs its intended -initrd configuration instead.

`-snapshot` directs ordinary disk writes to temporary storage; do not issue a monitor commit/save operation if the original must remain unchanged. No host directory/device passthrough is needed here. Default software emulation does not require KVM; requesting KVM instead requires its actual host support/access. A CPU model named kvm64 alone does not enable KVM.

Use the serial log to distinguish missing kernel image, root-mount panic and a guest waiting at login. At the guest prompt, an actual uname query identifies the running guest kernel. Console silence under the conditional -S workflow can mean an intentionally paused CPU. Preserve guest state only if requested. Shut down the guest normally when possible; under the default console multiplexer Ctrl-A then X exits QEMU, and is an abrupt stop.

See [QEMU invocation options](https://www.qemu.org/docs/master/system/invocation.html) for this installed version's behavior.
