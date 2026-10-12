# Read selected files from a known NFS export

Require Linux NFS kernel support, the installed mount.nfs helper, authority to create the mount and the intended server/export/security context. Inspect the installed helper's version/help; do not install client packages to complete intake. Prepare a free, empty absolute mountpoint with the entrypoint's namespace and existing-mount checks.

An export advertisement permits no conclusion about every file's access. Establish the administrator-approved client-visible path and protocol/security requirements separately; NFSv4 paths may differ from server filesystem paths. Define `export_source` as the exact `server:/export/path` and `mountpoint` as that prepared directory. In the established privileged context, for selected reads:

~~~bash
mount -t nfs -o ro,nosuid,nodev,noexec "$export_source" "$mountpoint"
~~~

Check the immediate result, then attribute the actual source/type/options through findmnt or mountinfo as described in the entrypoint. Record the negotiated version/security context. Add `vers=N` or `sec=...` only when required by the established configuration and supported client; an old walkthrough is not a reason to downgrade either. A failed mount can leave an ordinary local directory at the mountpoint.

Select the requested file under the verified export and preserve its identity and actual read result. Presented owner names, large anonymous IDs or modes alone do not establish another user's access: server identity mapping, export policy, root squashing and file permissions remain relevant. A successful directory listing is narrower than reading all children. Do not change identity/export policy merely to make a denied file readable.

Distinguish the negotiated security flavor: `sec=sys` uses client-presented numeric identities, while supported Kerberos flavors have different authentication/protection properties. NFS is not universally unauthenticated. An export's `insecure` option relaxes the reserved-source-port requirement for applicable requests; it does not disable file permissions or mean `no_root_squash`. Root squashing is also distinct from mapping every user to an anonymous identity. Correlate numeric ownership and the effective server export with the client's actual security context before explaining a denial. See [exports security and identity mapping](https://man7.org/linux/man-pages/man5/exports.5.html).

`ro` bounds writes through this mount, not other writers, server logging or file consistency. `noexec` does not make untrusted input safe for an interpreter. For application/database recovery, obtain a consistent snapshot or retain the live-file limitation. An unresponsive hard-mounted server can stall reads; preserve the network/kernel diagnosis rather than blindly switching to soft timeouts, which have integrity risks.

Leave the mounted tree, close owned handles and unmount only this created mountpoint using the entrypoint's cleanup. Verify disappearance and retain busy/unresponsive errors; do not force or lazily detach unrelated mounts.

See [the NFS client manual](https://manpages.debian.org/bookworm/nfs-common/nfs.5.en.html) and [mount.nfs helper contract](https://manpages.debian.org/bookworm/nfs-common/mount.nfs.8.en.html).
