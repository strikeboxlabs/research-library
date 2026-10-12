# Retrieve a selected directory from an owned daemon

Require an established daemon/module, existing access, a stable selected source containing ordinary files/directories, and a fresh private destination. Read the entrypoint's module-listing semantics first. A module description naming EncFS is a lead about its contents, not proof of the encryption format or possession of its matching configuration.

Set `source_url` to the exact approved directory URL and `destination` to a new absolute owned directory. Review the complete recursive plan:

~~~bash
umask 077
mkdir -- "$destination" && rsync -rt --dry-run --itemize-changes -- "$source_url/" "$destination/"
~~~

Confirm the intended filenames and scope, including dotfiles. Then copy:

~~~bash
rsync -rt --itemize-changes -- "$source_url/" "$destination/"
copy_status=$?
~~~

`-r` recurses and `-t` retains file times; these arguments do not preserve ownership, exact permissions, symbolic links or special files. Resolve any required nonordinary entry separately before claiming complete backup recovery. The source trailing slash selects its contents, including `.encfs6.xml` when present; a shell `*` selection would omit ordinary dotfiles. Direct daemon transport supplies no automatic encryption.

Inspect status, diagnostics, expected file counts/sizes and an independently supplied digest or manifest. Received bytes and a successful exit do not establish a consistent snapshot of a changing tree. Hidden configuration may contain key material: retain it privately with the matching ciphertext and preserve both originals before mounting a working copy. This transfer does not decrypt anything.

On a partial copy, resolve the cause and use a fresh destination. Adding `--ignore-existing` can skip an incomplete existing file; a later zero exit would not repair it. Do not add deletion, source removal or automatic archive extraction.

Reference: [rsync manual](https://download.samba.org/pub/rsync/rsync.1).
