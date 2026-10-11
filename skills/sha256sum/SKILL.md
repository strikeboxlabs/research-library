---
name: sha256sum
description: Compute and verify exact local file-byte SHA-256 checksums with GNU coreutils, retaining manifest paths, read status and independent trust limits.
---

# Identify or compare selected file bytes

Read this entire SKILL.md before acting. Require an existing regular file and completed byte representation; confirm GNU coreutils with `sha256sum --version`. No conditional resources are required. Finish with input identity, digest/comparison, status and unresolved errors. A checksum does not establish who supplied the file.

Define `artifact` as the selected absolute path:

~~~bash
sha256sum --binary -- "$artifact"
~~~

Retain read status and diagnostics. The digest has 64 hex digits; mode marker and filename are separate fields. Hash the actual completed archive when comparing package metadata. Hashing its decoded payload, hexadecimal text or a stream with an added newline answers a different question. A file changing during the read needs a coherent repeat capture.

For an existing trusted GNU-format manifest, review its member paths, define `manifest` and use `sha256sum --check --strict -- "$manifest"` from the intended base directory. A mismatch, missing input or malformed record leaves verification incomplete. A matching digest protects consistency with that reference; authenticate the reference separately. Replacing both file and manifest can preserve a match without preserving trusted provenance.

See the [GNU SHA-256 invocation](https://manpages.debian.org/bookworm/coreutils/sha256sum.1.en.html).
