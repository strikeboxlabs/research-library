---
name: shocker
description: Use a reviewed Linux Shocker file-handle proof of concept for one authorized container-isolation test. Distinguish the modified two-argument build, filesystem/capability prerequisites and truncated text recovery from a complete host-file read.
---

# Match the installed implementation first

Read this entire SKILL.md and [file-handle testing](references/file-handle-testing.md) before acting. This package supports the modified Shocker variant that accepts a selected absolute file path and fresh output path. Establish its reviewed source/build identity, mount anchor, effective capability and test scope first. Finish with observed status, recovered bytes and explicit completeness limits; a success banner or container UID 0 is insufficient.

Shocker is a historical proof of concept, not a standardized CLI. The original fixed-file example and modified builds can have different arguments and output handling. Do not assume `--help` is implemented: an unchecked positional-argument parser can interpret it as a path or crash. Locate the trusted installed build during the Linux environment pass and match its source before using the reference's invocation. An unavailable/mismatched binary is a specific prerequisite gap, not permission to fetch or execute arbitrary source.

The mechanism guesses filesystem file handles and opens them through a visible mount. It is conditional on kernel/filesystem and isolation configuration; adding capabilities does not guarantee that an arbitrary host path can be opened. See [the Linux file-handle API](https://manpages.debian.org/bookworm/manpages-dev/open_by_handle_at.2.en.html).
