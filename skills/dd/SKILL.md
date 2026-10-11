---
name: dd
description: Acquire a selected offline block-device image or extract exact byte ranges from regular image files with GNU dd. Use when source identity, consistency, measured offsets or short-copy results matter.
---

# Copy an explicitly measured extent

Read this entire SKILL.md before acting. For a regular-file extent, establish the format, measured byte range and fresh regular-file destination, then use the procedure below. For acquisition from an identified offline block source, read [block-device acquisition](references/block-device-acquisition.md) completely before that procedure. Finish with status, exact size, identity and consistency limits; a short copy or missing prerequisite remains incomplete.

Use ordinary file copying for a whole file. `dd` earns its place when a format identifies an exact byte range. Define `image` as an existing regular working file, `output` as a new regular-file destination, `offset` as a nonnegative byte offset and `length` as the positive number of bytes required. Verify the range against the source length and actual format first.

~~~bash
dd --version
dd --help
stat -c '%s' -- "$image"
test -f "$image" && dd if="$image" of="$output" bs=1M skip="${offset}B" count="${length}B" iflag=fullblock conv=excl status=progress &&
stat -c '%s' -- "$output"
~~~

These are GNU options, and the byte-suffix operands require support in the installed release. The `B` suffix makes skip/count byte-based despite the larger transfer buffer. Older GNU releases can reject that spelling as an invalid number. For a bounded small extent on such a release, use `bs=1 skip="$offset" count="$length"` instead of the three corresponding operands above; input-block units then equal bytes. The single-byte buffer can be slow for large ranges. Do not simply remove the suffix while retaining bs=1M: that changes the selected range by the buffer multiplier. `iflag=fullblock` handles short reads when counting blocks; it does not invent missing input. `conv=excl` refuses an existing destination instead of truncating it. Check the command status and require the resulting size to equal `length`: reaching EOF early can finish successfully with fewer bytes.

The Arkham LUKS example's `bs=512 count=4097` copies 2,097,664 bytes. That happens to include one sector beyond a 4096-sector payload offset; it is not a universal LUKS header size. A consuming tool may also require keyslot material or encrypted payload bytes. Derive its requirements from the actual image and parser, or retain the complete image copy. A header backup is not automatically a valid cracking input.

Do not apply this file-to-file procedure to a block-device destination. Avoid `conv=noerror,sync` for routine extraction: it continues after read errors and pads data, changing how bytes should be interpreted. Keep the original, byte range, resulting size and checksum with the derived artifact so a later parser failure can be traced to acquisition versus format support.

See [GNU dd](https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html), [the packaged option manual](https://manpages.debian.org/bookworm/coreutils/dd.1.en.html) and [the LUKS consuming parser](https://github.com/hashcat/hashcat/blob/master/src/modules/module_14600.c) for range and artifact requirements.
