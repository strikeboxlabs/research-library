---
name: lsb-release
description: Use lsb_release to identify the selected Linux userspace distribution, release and codename, or distinguish distribution metadata from kernel and package patch evidence.
---

# Distribution metadata

Read this entire SKILL.md before acting. Select the intended local system or container and define `lsb_release_bin` as its verified trusted executable. Finish with the returned distribution fields, command status and scope; a missing executable or unavailable field is an unresolved metadata check, not proof of another distribution.

~~~bash
"$lsb_release_bin" --help
"$lsb_release_bin" --all
metadata_status=$?
printf 'metadata_status=%s\n' "$metadata_status"
~~~

`--all` reports available LSB module information and distributor, description, release and codename. `--id`, `--description`, `--release` and `--codename` select individual fields; `--short` omits field labels. Retain the full output when comparing captures. `--version` reports supported LSB modules, not the executable's software version. A `No LSB modules are available` diagnostic can accompany valid distribution fields; evaluate the fields and status independently.

This identifies userspace metadata in the selected execution context. It does not identify the running kernel, establish installed package versions or prove that a vulnerability is fixed. A container can report its own distribution while sharing the host kernel. An upstream kernel release and a distributor's kernel package/ABI string follow different version schemes; do not compare their numbers as a patch test. Resolve package provenance and vendor patch evidence separately when that is the actual question.

Implementations differ: current Debian's minimal implementation uses os-release metadata, while older releases used a larger Python implementation. Check the selected executable's help and metadata producer when fields disagree. See the [Debian manual](https://manpages.debian.org/bookworm/lsb-release/lsb_release.1.en.html).
