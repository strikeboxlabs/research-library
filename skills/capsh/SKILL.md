---
name: capsh
description: Decode a captured Linux capability mask or inspect the current execution context's capability sets, securebits and identity with libcap capsh. Use when mask names, container root or a bounding-set entry are being treated as proof of an allowed operation.
---

# Read capability state in the selected context

Read this entire SKILL.md before acting. Establish which session/container executes the inspection and confirm that the selected capsh executable is the intended libcap tool. No conditional resources are required. Finish with the complete returned state, status and namespace/context limits; a capability listing is not execution evidence for a privileged operation.

Use `capsh --help` to check this installation's inspection options. Run the inspection under the existing task identity, without adding sudo or changing capability sets:

For a captured hexadecimal mask, define `mask` as its complete hex digits and retain the originating field/process/time separately:

~~~bash
capsh --decode="$mask"
~~~

`--decode` interprets a hexadecimal capability vector, even when its digits look decimal; it does not inspect or change a process. The same names decoded from CapEff, CapPrm or CapBnd have different operational meanings. A mask in a source-code test is requested logic, not observed state. A nonzero bitwise intersection tests whether any selected bit is present; it does not establish that every required bit is present. Preserve the actual comparison and successful state acquisition before accepting a source comment that says it checks all capabilities.

For the current process's state:

~~~bash
capsh --print
status=$?
~~~

Retain stdout, stderr and `status`. Check the reported UID/GID, Current capabilities, bounding set, securebits and ambient state when this version shows it. Missing fields in older output are unavailable evidence, not zero-valued sets. The state belongs to this capsh process at this time; executable attributes or a different launcher can affect what it inherits. It does not enumerate every process or the container's complete configured policy.

Current capability text distinguishes **effective**, **permitted** and **inheritable** flags (`e`, `p`, `i`). Effective bits participate in the relevant privilege checks; permitted bits define what that thread can hold effective. Inheritable and ambient state affect transitions under their rules. The bounding set limits certain capability acquisition during execution; a name present there is not proof that the same bit is presently effective. Preserve the whole text rather than selecting a capability name without its set/flags.

UID zero inside a container does not establish host authority. Capabilities are scoped through user namespaces, and operations can additionally be restricted by seccomp, mandatory access control, kernel configuration and resource visibility. A capability present in a child user namespace does not automatically authorize the equivalent host operation. Keep deployment-provided namespace/policy evidence separate from this process snapshot.

For example, **CAP_SYS_MODULE** concerns kernel-module loading/unloading. Its appearance calls for review of the effective set and isolation policy; it does not prove that a module load occurred, that a compatible build exists or that all other enforcement allows it. Diagnose an actual denial from the requested operation's existing evidence rather than loading a module to test this inspection.

**CAP_DAC_READ_SEARCH** concerns bypassing discretionary file-read and directory read/search checks, and the privileged check for `open_by_handle_at`. It does not grant the separate general file-write override of CAP_DAC_OVERRIDE. Its effective presence deserves an isolation-policy review, but does not alone establish host filesystem visibility, a usable file handle or a successful container escape. Retain the operation's existing result and namespace/mount evidence separately.

Options are evaluated in order. Adding capability/identity-changing flags or a shell execution separator changes the task; do not copy a longer wrapper merely to print state. An unknown option or failed inspection leaves a capability gap, not an empty successful inventory.

References: [libcap capsh manual](https://manpages.debian.org/bookworm/libcap2-bin/capsh.1.en.html), [Linux capability sets and transitions](https://manpages.debian.org/bookworm/manpages/capabilities.7.en.html), [user namespaces](https://manpages.debian.org/bookworm/manpages/user_namespaces.7.en.html).
