---
name: bmap
description: Inspect a regular file's trailing filesystem slack with Daniel Ridge's Linux bmap. Use when logical file reads miss residual bytes and the original block allocation is available in an authorized forensic environment.
---

# Read trailing file slack

Identify this legacy filesystem block-mapping utility using `bmap --version` and `bmap --help`; it is different from `bmaptool`, which creates block maps and copies images. Compatibility depends on the build, architecture, filesystem block-mapping support and access to the correct underlying device. A successful build alone does not verify those conditions.

Define `target` as an absolute regular-file path in an already prepared, authorized filesystem clone preserving the original block allocation. An ordinary copied file or an image file treated as the target does not represent the original file's slack. Preparing/mounting the forensic clone is a separate task. The reviewed implementation rejects symlinks and requires raw-device access; a permission or mapping error leaves the read unresolved.

Define `slack` and `log` as fresh private files on a separate output filesystem:

~~~bash
umask 077
if bmap --mode=slack --log-thresh=info "$target" >"$slack" 2>"$log"; then
    wc -c -- "$slack"
    sha256sum -- "$slack"
else
    printf '%s\n' 'Slack read failed; inspect diagnostics and retain output as incomplete.' >&2
    false
fi
~~~

Inspect the command status and diagnostic log before using the bytes. This mode reads from the logical end of the file to the end of its last allocated filesystem block. It does not read process memory or enumerate all free space. **Illustrative:** a 52-byte file in one 4096-byte block leaves 4044 trailing bytes; a block-aligned file has no such tail.

The old implementation does not robustly check every raw read/write return value and can report success after some failures. A zero status or expected output length alone does not validate recovery; corroborate mapping, diagnostics and meaningful bytes with the forensic acquisition. Empty or all-zero output does not prove that the volume contains no residual data. Stop on unsupported mapping or seek/read errors instead of substituting another device.

Keep raw bytes and their hash; a readable string is a lead, not proof of its owner, age or deliberate concealment. Stay with `--mode=slack`: `putslack`, `wipeslack` and `wipe` modify the source. The optional `--outfile` appends in the reviewed implementation, so the example uses separate shell redirection to fresh files.

See the [source copy and architecture note](https://github.com/CameronLonsdale/bmap), [mode and I/O implementation](https://github.com/CameronLonsdale/bmap/blob/master/bmap.c) and [diagnostic stream implementation](https://github.com/CameronLonsdale/bmap/blob/master/mft/log.c) when checking the installed build.
