---
name: capsh
description: Inspect the current Linux execution context's capability sets, securebits and identity with libcap capsh. Use when container root, a bounding-set entry or a capability name is being treated as proof of an allowed operation.
---

# Read capability state in the selected context

Read this entire SKILL.md before acting. Establish which session/container executes the inspection and confirm that the selected capsh executable is the intended libcap tool. No conditional resources are required. Finish with the complete returned state, status and namespace/context limits; a capability listing is not execution evidence for a privileged operation.

Use `capsh --help` to check this installation's inspection options. Run the inspection under the existing task identity, without adding sudo or changing capability sets:

~~~bash
capsh --print
status=$?
~~~

Retain stdout, stderr and `status`. Check the reported UID/GID, Current capabilities, bounding set, securebits and ambient state when this version shows it. Missing fields in older output are unavailable evidence, not zero-valued sets. The state belongs to this capsh process at this time; executable attributes or a different launcher can affect what it inherits. It does not enumerate every process or the container's complete configured policy.

Current capability text distinguishes **effective**, **permitted** and **inheritable** flags (`e`, `p`, `i`). Effective bits participate in the relevant privilege checks; permitted bits define what that thread can hold effective. Inheritable and ambient state affect transitions under their rules. The bounding set limits certain capability acquisition during execution; a name present there is not proof that the same bit is presently effective. Preserve the whole text rather than selecting a capability name without its set/flags.

UID zero inside a container does not establish host authority. Capabilities are scoped through user namespaces, and operations can additionally be restricted by seccomp, mandatory access control, kernel configuration and resource visibility. A capability present in a child user namespace does not automatically authorize the equivalent host operation. Keep deployment-provided namespace/policy evidence separate from this process snapshot.

For example, **CAP_SYS_MODULE** concerns kernel-module loading/unloading. Its appearance calls for review of the effective set and isolation policy; it does not prove that a module load occurred, that a compatible build exists or that all other enforcement allows it. Diagnose an actual denial from the requested operation's existing evidence rather than loading a module to test this inspection.

Options are evaluated in order. Adding capability/identity-changing flags or a shell execution separator changes the task; do not copy a longer wrapper merely to print state. An unknown option or failed inspection leaves a capability gap, not an empty successful inventory.

References: [libcap capsh manual](https://manpages.debian.org/bookworm/libcap2-bin/capsh.1.en.html), [Linux capability sets and transitions](https://manpages.debian.org/bookworm/manpages/capabilities.7.en.html), [user namespaces](https://manpages.debian.org/bookworm/manpages/user_namespaces.7.en.html).
