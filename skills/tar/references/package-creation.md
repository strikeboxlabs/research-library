# Create the archive layout the consumer expects

Select plain tar or gzip-compressed tar from the actual consumer contract; the extension alone does not choose compression. If the consumer expects a small set of files directly at archive root, define `package_root` as their actual shared directory, `member1`, `member2`, `member3` as the selected literal basenames and `archive` as a fresh absolute destination. Review their actual types and keep output outside that source directory:

~~~bash
test ! -e "$archive" && test ! -L "$archive" &&
  tar --create --verbose --file="$archive" --directory="$package_root" -- "$member1" "$member2" "$member3"
tar --list --verbose --file="$archive"
~~~

This produces uncompressed tar with those names at root, without an extra package directory. Verify each selected name/type and both final statuses against the requested manifest. If a gzip wrapper is required, add --gzip for creation/listing; neither layout nor a successful list verifies signatures, firmware authenticity or permission to deploy the bundle.

Require the selected trusted source tree, actual consumer format/layout and a fresh archive destination outside that tree. For GNU tar, define `package_parent` as the absolute parent directory, `package_name` as the selected child directory's literal basename and `archive` as a new absolute output path. Reject leading-option/ambiguous names and unexpected links/special files before packaging.

~~~bash
test ! -e "$archive" && test ! -L "$archive" &&
  tar --create --gzip --verbose --file="$archive" --directory="$package_parent" -- "$package_name"
tar --list --verbose --gzip --file="$archive"
~~~

Check creation and final listing status separately. `--create` can overwrite an existing archive; the fresh-path condition is part of this procedure, not concurrency protection against another writer. `--gzip` produces gzip-compressed tar bytes. Changing a .zip extension to .gz does not convert its format. Put output outside the source tree rather than relying on tar's self-archive exclusion.

`--directory` changes the source lookup directory, so the top-level member is `package_name/` with its files beneath. Illustratively, a package called probe_module should list `probe_module/probe_module.info` and `probe_module/probe.php`, not absolute paths, flattened files or an extra parent layer. Confirm the actual consumer contract; a correct listing does not establish that module metadata/dependencies or PHP code are valid.

If a Backdrop manual installer offers tar/tgz/gz/bz2 while ZIP support is unavailable, a real tar.gz package can preserve the same module tree without changing the server's PHP extensions. The installer browser's ZIP/dependency/remote catalog failure is distinct from the manual archive path. Read the format list shown by this site; not every installation accepts the same formats. Archive upload, extraction, module enablement and direct PHP endpoint execution are separate results.

Do not use --dereference just to make packaging succeed: following a symlink changes included content. Its short spelling `-h` does not enable compression. A file-changing warning or read error leaves an uncertain/incomplete package; reacquire a stable source before calling it ready. Keep the original archive and inspect an existing output rather than overwriting it incidentally on a retry.

See [GNU tar creation](https://www.gnu.org/s/tar/manual/html_node/create.html), [compression](https://www.gnu.org/software/tar/manual/html_node/gzip.html) and [Backdrop manual formats](https://docs.backdropcms.org/documentation/project-installer-and-updates).
