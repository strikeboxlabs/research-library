---
name: zip
description: Create a selected Linux source or data archive with Info-ZIP zip. Use when recursive scope, Git-metadata exclusions, stale archive members or symlink handling affects a transfer package.
---

# Package a selected tree

Read this entire SKILL.md before acting; reuse complete current context. Select the intended source tree and exclusions, create a fresh archive outside that tree, and inspect its members and integrity before handing it to a consumer. ZIP packaging does not establish source trust or executable compatibility.

Check `zip -v` for the installed implementation/options. Define `parent` as the absolute parent directory, `tree` as its selected ordinary directory name, and `archive` as a fresh absolute `.zip` path outside the tree. This Info-ZIP example omits that tree's Git metadata without deleting it:

~~~bash
umask 077
(
  cd -- "$parent" || exit
  zip -r -y "$archive" "$tree" -x "$tree/.git/*"
)
status=$?
~~~

Require zero status and inspect warnings for unreadable or skipped inputs. `-r` walks the selected tree, including dotfiles; `-x` patterns are matched by zip, so quote them against shell expansion. This pattern excludes the selected root's `.git` directory and members; inspect nested repositories, ignored credentials and generated files separately when they are relevant to the package. A Git ignore file does not itself exclude those files from zip.

On Unix, `-y` stores symlinks as symlinks rather than including the files they reference. It avoids silently pulling external linked content into the archive, but can leave links whose targets are absent or whose extraction points outside the destination. Decide which behavior the receiver requires; storing a link is not containment.

If an archive already exists, zip's normal add/update behavior can retain old members that have disappeared from the selected filesystem tree. A fresh output avoids claiming such an archive is a current exact snapshot. Do not use `-m` to prepare a transfer: it removes source files after archiving. Choose extra exclusions or a selected file list instead of deleting source metadata.

If an installed UnZip consumer is available:

~~~bash
unzip -Z -1 "$archive"
unzip -t "$archive"
~~~

Compare the member list with the intended relative tree, excluded metadata and expected files. The integrity test checks decompression/CRC, not safe member paths, authenticity or whether build scripts are trustworthy. Retain the archive and its member/integrity result; before executing transferred source, verify the expected bytes and review its execution separately.

See the [Info-ZIP zip manual](https://manpages.debian.org/bookworm/zip/zip.1.en.html) for recursion, exclusions, Unix symlinks and archive-update behavior.
