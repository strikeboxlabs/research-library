# Read a selected tree through a CIFS mount

Require Linux CIFS kernel support, the installed `mount.cifs` helper, the intended account/share and authority to create the mount. Establish a free, empty absolute mountpoint using the entrypoint's existing-mount checks. A successful smbclient session does not configure the kernel mount's identity.

Define `share_source` as the exact `//server/share`, `mountpoint` as that prepared directory and `credential_file` as an existing private file readable only by its intended owner/mounting authority. Its content uses the helper's `username=`, `password=` and optional `domain=` fields; do not put passwords in argv. Use a credential-file path without commas or line breaks because `-o` is a comma-separated option list. Check installed helper documentation before selecting dialect/security options; do not infer them from an old walkthrough.

In the established privileged context:

~~~bash
mount -t cifs "$share_source" "$mountpoint" -o "ro,nosuid,nodev,noexec,credentials=$credential_file"
~~~

Check the immediate exit status and attribute the resulting source/type/options with `findmnt` or mountinfo as described in the entrypoint. Read only the requested relative subtree. `ro` applies to this mount; it neither freezes other writers nor prevents server-side access logging. `noexec` does not make untrusted source safe to feed to an interpreter. Server/share/file ACLs still govern actual access, separately from presented Linux ownership/modes; one root directory listing does not establish access to all children.

On failure, preserve the helper/kernel diagnostic and distinguish missing support/authority, authentication, name resolution and selected-directory access. A directory that remains after failed mounting may be the pre-existing local directory, not the remote tree. After the task, leave the mounted tree and unmount only the mount created here using the entrypoint's cleanup procedure; verify its disappearance and account for any busy handles. Keep credential-file retention/removal aligned with its existing owner and purpose.

See the [kernel CIFS usage guide](https://cdn.kernel.org/doc/html/latest/admin-guide/cifs/usage.html) and the installed `mount.cifs(8)` manual for version-specific authentication, dialect and identity-mapping behavior.
