---
name: cpio
description: List and extract a reviewed ordinary cpio archive with GNU cpio into a fresh directory, preserving input and distinguishing member processing from complete extraction.
---

# Selected archive copy-in

Read this entire SKILL.md before acting. Require an uncompressed ordinary archive and the permitted destination. Define `cpio_bin` as the verified trusted GNU executable and `archive` as its absolute input. Finish with the selected members, extraction status and observed output; an archive listing does not execute its contents.

~~~bash
"$cpio_bin" --version
"$cpio_bin" --list --verbose < "$archive"
list_status=$?
printf 'list_status=%s\n' "$list_status"
~~~

Review paths, member types and links before extraction. Require a controlled archive containing reviewed relative paths and a fresh empty destination under an unprivileged account. Absolute paths, parent traversal, links and device members need resolution before proceeding; --no-absolute-filenames alone is not a sandbox. Use isolation for an untrusted archive.

Define `destination` as that absolute directory:

~~~bash
(
  cd -- "$destination" || exit
  "$cpio_bin" --extract --make-directories --preserve-modification-time \
    --verbose --no-absolute-filenames --no-preserve-owner < "$archive"
)
extract_status=$?
printf 'extract_status=%s\n' "$extract_status"
~~~

This is copy-in (-i): -d creates leading directories, -m restores recorded modification times and -v lists processed names. Extraction writes files; it is separate from decompression. Avoid unconditional replacement (-u) for a fresh extraction. GNU cpio reports0 for completion and2 for errors; inspect diagnostics and actual outputs before claiming completeness. Recovered scripts/binaries remain data until separately reviewed for an intended execution. See the [GNU cpio manual](https://manpages.debian.org/bookworm/cpio/cpio.1.en.html).
