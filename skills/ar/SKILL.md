---
name: ar
description: List an acquired GNU ar archive and extract one selected ordinary member into a fresh private directory. Use for Debian package contents without installing the package or confusing archive bytes with loaded libraries.
---

# Extract a selected archive member

Read this entire SKILL.md before acting. Require the acquired archive, full member listing, a unique selected ordinary basename and a new private output directory. No conditional resources are required. Finish with the archive/member identity, extraction status and resulting bytes; this does not install or execute package content.

Confirm `ar --version` and installed help. Define `archive` as the absolute local archive path, then list all members:

~~~bash
ar t "$archive"
status=$?
~~~

Check status and the full list before choosing `member`. A filtered listing can hide duplicate names. This procedure requires one unique basename without path separators, leading options or traversal components; repeated/path-bearing names need an explicitly supported selection strategy. Thin archives refer to external files and cannot be extracted with `x` as ordinary self-contained archives.

Set `output_dir` to a new absolute directory beneath the owned working area. Extract only the selected member:

~~~bash
umask 077
mkdir -- "$output_dir" && (
  cd -- "$output_dir" || exit
  ar x "$archive" "$member"
)
status=$?
~~~

Require successful status and inspect the resulting regular file before using its format-specific reader. A fresh directory avoids overwriting an existing member. Extraction does not authenticate the archive or prove the extracted library matches a running process.

A Debian `.deb` contains `debian-binary`, control and data tar members. Select the exact observed data-member name: compression can vary, so do not assume `data.tar.xz`. Reading/extracting these members does not run maintainer scripts or install their filesystem contents. Keep package/build metadata separate from independently observed runtime library identity.

References: [GNU ar operations](https://sourceware.org/binutils/docs/binutils/ar-cmdline.html), [Debian package format](https://manpages.debian.org/bookworm/dpkg-dev/deb.5.en.html).
