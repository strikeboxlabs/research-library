# One selected file, with implementation-specific evidence

For the reviewed two-argument variant, establish `shocker_bin` as the trusted executable, `authorized_file` as the exact scoped absolute path, and `output_file` as a fresh private path. Confirm in source that the binary opens a mount anchor (the demonstrated variant uses `/etc/hostname`), expects an eight-byte type-1 handle with a guessed root inode, walks path components and then writes the selected file's contents. A different anchor/filesystem/handle layout needs a different reviewed implementation; changing a constant blindly is not portability.

`open_by_handle_at` requires `CAP_DAC_READ_SEARCH` and a descriptor into the applicable mounted filesystem. Root inside a container is not equivalent to that capability in the required namespace. The syscall may be denied by policy, and unsupported or stale handles fail separately. The program's guessed handle search can be lengthy; agree a bounded run and preserve diagnostics rather than escalating permissions or broadening the requested file automatically.

In an explicitly authorized disposable fixture, after reviewing this build's prompt and output handling:

~~~bash
umask 077
"$shocker_bin" "$authorized_file" "$output_file"
status=$?
~~~

The demonstrated build waits for one input byte before its attempt. Supply Enter only to that identified prompt; keep the run attached or use a harness duration bound. Do not assume a matching command accepts noninteractive stdin or reports a reliable exit code without source review. A line such as **illustrative** `Found handle ...` establishes a candidate step; it is not complete recovery.

The demonstrated modified code performs one read of at most 4095 bytes and writes with text `%s` semantics. Thus larger files are truncated and embedded NUL bytes terminate output; unchecked read/open/write errors can invalidate even a success banner. Inspect actual output length/content and compare a known owned fixture to establish what was returned. Report a recovered prefix as a prefix, not a full file. Preserve failures such as permission denial, unsupported filesystem and stale/invalid handle distinctly. A real isolation conclusion requires correlated mount/capability and known host-fixture evidence, not a guess that any `/root/...` path is the host's.

When building reviewed historical C, missing declarations for `open_by_handle_at` or `fdopendir` need the appropriate headers and feature-test macros before headers; an implicit integer return can corrupt pointers. Do not suppress those diagnostics to reproduce a screenshot. The eight-byte handle assumptions and filename comparison in this old example are additional implementation limits. This package supplies no executable proof-of-concept source and installs no tool. The later controlled-image pass can replace this narrow procedure with verified invocation facts for the actual installed version.
