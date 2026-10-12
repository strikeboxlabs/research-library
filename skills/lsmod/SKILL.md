---
name: lsmod
description: Inspect currently loaded Linux kernel modules with kmod lsmod. Use when a module file, device node or build artifact is being mistaken for evidence that a module is loaded.
---

# Read loaded module state

Read this entire SKILL.md before acting. Require access to the actual kernel's module inventory in the intended host/guest context. No conditional resources are required. Finish with the complete query status, selected module row and context; unavailable inventory is unresolved evidence.

~~~bash
lsmod --version
lsmod
status=$?
~~~

Check the full result and status before selecting a module name. This formats /proc/modules. A successful exact row establishes presence in that inventory; a matching filename under /lib/modules does not. No row does not establish that equivalent functionality is absent: it may be built into the kernel.

Keep Module, Size and Used by distinct. A zero reference count is not proof that unloading is safe, the module is harmless or a particular device works. The listing is a snapshot, not a retained history or module-file integrity check. A container may expose its host kernel's state; retain the execution context.

To correlate a device, use independently observed registration/path metadata. Readability of a device node or successful listing does not establish which ioctl operations are permitted. Loading, unloading and changing device access remain separate administration tasks.

See the packaged [kmod lsmod manual](https://manpages.debian.org/trixie/kmod/lsmod.8.en.html).
