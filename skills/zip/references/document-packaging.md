# Repackage an owned WordprocessingML document tree

Require a reviewed benign document tree and its intended application/format. ZIP bytes alone do not make a valid DOCX. Confirm the content-type declarations, package relationships and referenced document parts, preserving their relative paths. A usual WordprocessingML tree includes `[Content_Types].xml`, `_rels/.rels` and `word/document.xml`; use the actual relationships rather than fabricating missing parts.

Define `package_root` as the absolute owned package directory and `archive` as a fresh absolute `.docx` output outside it. Resolve unexpected links/special files and unrelated inputs before packaging. With Info-ZIP:

~~~bash
umask 077
test ! -e "$archive" && test ! -L "$archive" && (
  cd -- "$package_root" || exit
  zip -r "$archive" .
)
status=$?
~~~

Check status and warnings. Starting inside the package root retains nested part paths without wrapping them in the source directory's name. `*` is shell-expanded and omits dotfiles; `-j` flattens paths and breaks relationships. A pre-existing archive can retain stale members, so keep a fresh destination outside the input tree.

If an installed UnZip consumer is available, list and test:

~~~bash
unzip -Z -1 "$archive"
unzip -t "$archive"
~~~

Confirm expected root-relative parts, no enclosing directory and successful integrity status. CRC/decompression checks do not validate XML, relationships, document rendering or a converter's acceptance. Use the intended document reader and retain its actual result before calling the DOCX usable; an HTTP callback from a converter is not that result. Do not execute embedded content to verify packaging.

References: [Info-ZIP recursion and member paths](https://manpages.debian.org/bookworm/zip/zip.1.en.html), [WordprocessingML package structure](https://learn.microsoft.com/en-us/office/open-xml/word/structure-of-a-wordprocessingml-document).
