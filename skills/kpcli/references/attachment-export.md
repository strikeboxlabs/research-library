# Export one selected nonsecret attachment

Use this for an owned document or other nonsecret attachment whose database unlock factors are already known. Establish the exact entry, requested attachment, supported database generation and a fresh destination in a private local directory. This task does not require displaying the entry password. KDB and KDBX/backend combinations differ in attachment support; do not infer multiple-attachment support merely from a suffix.

Open the working copy with the entrypoint's `--readonly --histfile /dev/null` session and use `cd`/`ls` to select the entry. Confirm `help attach` in the installed version. Invoke `attach` with the displayed entry number or its kpcli path, for example the following **illustrative interactive input** after entry 0 has been independently selected:

~~~text
attach 0
~~~

Review the attachment names and displayed byte counts, then choose the export menu action `e`. Select the required attachment by its displayed number when there are several. Supply a complete absolute destination filename in the fresh private directory, rather than accepting the attachment's default name or giving an existing directory. The implementation can append the database-supplied attachment name to a directory path. A deliberate filename avoids inheriting that path and keeps an existing artifact out of the overwrite branch. If an overwrite prompt appears, decline it and choose a fresh destination.

The read-only database mode prevents attachment addition/deletion but permits export to the host filesystem. Export does not mark the database changed; use `quit` without saving. Keep the original database unchanged. A `Saved ...` message records the attempted write, not independently verified byte integrity. On the selected Linux host, define `exported` as the complete chosen output path and inspect it without executing its contents:

~~~bash
stat --format='%s bytes' -- "$exported"
sha256sum -- "$exported"
~~~

Compare the length with the selected attachment's displayed count and retain the digest for any subsequent authorized transfer. A digest without a trusted comparison value fingerprints the artifact; it does not authenticate it. Investigate a mismatch using the same database copy and backend before modifying any bytes. Do not strip whitespace or repair a document based on a writeup's unsupported explanation. Exported attachments can contain executable content; file creation does not require running it.

Finish with the selected entry/attachment identity, actual local path, size and digest, database-preservation result, and any unresolved format or write error. Keep document contents and unrelated credentials out of the result.

See [the kpcli attachment implementation](https://sources.debian.org/src/kpcli/4.1.3-1/kpcli-4.1.3.pl/) for menu, destination handling and version-dependent database behavior.
