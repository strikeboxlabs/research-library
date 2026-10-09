---
name: dd
description: Extract exact byte ranges from regular image files with GNU dd. Use when a format supplies offsets, a walkthrough hardcodes a header size, or a successful copy may still be shorter than requested.
---

# Copy an explicitly measured extent

Use ordinary file copying for a whole file. `dd` earns its place when a format identifies an exact byte range. Define `image` as an existing regular working file, `output` as a new regular-file destination, `offset` as a nonnegative byte offset and `length` as the positive number of bytes required. Verify the range against the source length and actual format first.

~~~bash
dd --version
stat -c '%s' -- "$image"
test -f "$image" && dd if="$image" of="$output" bs=1M skip="${offset}B" count="${length}B" iflag=fullblock conv=excl status=progress &&
stat -c '%s' -- "$output"
~~~

These are GNU options. The `B` suffix makes skip/count byte-based despite the larger transfer buffer. Without it, skip/count normally use input-block units. `iflag=fullblock` handles short reads when counting blocks; it does not invent missing input. `conv=excl` refuses an existing destination instead of truncating it. Check the command status and require the resulting size to equal `length`: reaching EOF early can finish successfully with fewer bytes.

The Arkham LUKS example's `bs=512 count=4097` copies 2,097,664 bytes. That happens to include one sector beyond a 4096-sector payload offset; it is not a universal LUKS header size. A consuming tool may also require keyslot material or encrypted payload bytes. Derive its requirements from the actual image and parser, or retain the complete image copy. A header backup is not automatically a valid cracking input.

Do not apply this file-to-file procedure to a block-device destination. Avoid `conv=noerror,sync` for routine extraction: it continues after read errors and pads data, changing how bytes should be interpreted. Keep the original, byte range, resulting size and checksum with the derived artifact so a later parser failure can be traced to acquisition versus format support.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Arkham p. 5. Sources: [GNU dd](https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html), [Hashcat LUKS binary parser](https://github.com/hashcat/hashcat/blob/master/src/modules/module_14600.c).
