---
name: insmod
description: Insert an explicitly approved, compatible local kernel module with kmod insmod and distinguish insertion, dependency, signature and initialization failures. Use for a selected controlled Linux guest administration task.
---

# Insert a selected approved module

Read this entire SKILL.md before acting. Require the trusted module artifact, a compatible running kernel, its prerequisites and explicit authorization to change that kernel's loaded state. No conditional resources are required. Finish with insertion status and current module/initialization evidence; acquiring or compiling a .ko is not loading it.

Define `module_file` as the exact absolute approved artifact in the intended host/guest. Preserve its identity and the observed kernel release. In an already authorized administrative session:

~~~bash
insmod --version
insmod "$module_file"
status=$?
~~~

Check status, diagnostics and the kernel's available log for initialization/linking details. Do not treat a terse userspace error as a complete cause. insmod inserts a file directly; it does not resolve dependencies like modprobe. Missing symbols need compatible prerequisites, a format/version error needs the correct build, and a rejected signature needs the approved signing/trust process.

Avoid force options that bypass version/vermagic checks. A taint or signature-verification message can coexist with a successfully loaded module on one policy configuration; under another policy loading may be rejected. Check actual status and loaded-state evidence rather than generalizing from the message alone.

Use an actual complete lsmod query to confirm the selected module, then verify the requested ordinary initialization effect separately. A device path alone can be stale or unrelated, and module presence does not establish that every operation works. Account for partial effects and the task's planned cleanup; unloading or repeatedly retrying a failing module is a separate decision.

See the packaged [kmod insmod manual](https://manpages.debian.org/trixie/kmod/insmod.8.en.html).
