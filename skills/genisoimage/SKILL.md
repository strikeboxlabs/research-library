---
name: genisoimage
description: Build an ISO9660 image from an owned selected directory and verify its contents and extensions. Use when suffixes, Rock Ridge metadata or Apple extensions obscure the actual format.
---

# Build the intended filesystem image

Read this entire SKILL.md before acting. Require a trusted installed builder, stable reviewed input and an authorized output path. Establish the consumer's format requirements first. Finish with builder status, image metadata and checked content; file creation alone is not compatibility.

Define `source_dir` as a bounded absolute directory, `image` as a fresh output file outside it, and `volume` as the approved identifier. Review effective .genisoimagerc settings and input names, links and confidential metadata.

~~~bash
genisoimage -version
genisoimage -R -V "$volume" -o "$image" "$source_dir"
~~~

Check status/diagnostics; failure can leave incomplete output. Rock Ridge retains POSIX names, modes, ownership and symlinks. Choose normalized metadata only for a consumer/task requirement. Adding `-f` follows links and changes input scope. Keep the input stable or report snapshot uncertainty.

If the trusted matching isoinfo utility exists, inspect without mounting:

~~~bash
isoinfo -d -i "$image"
isoinfo -R -f -i "$image"
~~~

Check both statuses. Compare descriptor/extensions and the full selected namespace listing with the expected manifest. Verify the intended consumer when required. This listing is not a content checksum or parser-safety verdict. Missing verification remains a gap.

A .dmg suffix can contain ISO9660. `-apple` adds Apple extensions, distinct from HFS hybrid creation and an Apple UDIF container. `-D` suppresses deep-directory relocation and can violate ordinary ISO9660 constraints; `-no-pad` removes normal padding. Select these only for verified consumer needs. Strings output cannot establish absence of compressed or structurally encoded metadata.

See [builder format/options](https://manpages.debian.org/bookworm/genisoimage/genisoimage.1.en.html) and [isoinfo](https://manpages.debian.org/bookworm/genisoimage/isoinfo.1.en.html).
