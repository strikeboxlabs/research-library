---
name: sha1sum
description: Compute or compare exact local file bytes with GNU SHA-1 checksums, distinguishing legacy consistency from trusted provenance and incomplete reads.
---

# Compare a selected legacy checksum

Read this entire SKILL.md before acting. Require the existing regular file and exact byte representation; confirm GNU coreutils with `sha1sum --version`. No conditional resources are required. Finish with input identity, digest/comparison, status and unresolved errors. SHA-1 consistency is not strong collision-resistant authenticity evidence.

Define `artifact` as the selected absolute path:

~~~bash
sha1sum --binary -- "$artifact"
~~~

Keep status and diagnostics. The digest has 40 hex digits; the mode marker and filename are separate output fields. Hash the completed archive itself when comparing package metadata, not its filename, printed hex or decoded contents. A changing file or failed producer can invalidate the intended comparison.

For a trusted GNU-format manifest with reviewed paths, define `manifest` and use `sha1sum --check --strict -- "$manifest"` from its intended base directory. Missing files, malformed records and mismatches are distinct failures. A supplied matching checksum does not independently authenticate its author or make an executable safe to install. Prefer the required stronger digest/signature for provenance tasks.

See the [GNU SHA-1 options and security limits](https://manpages.debian.org/bookworm/coreutils/sha1sum.1.en.html).
