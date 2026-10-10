---
name: showmount
description: Query an NFS server's advertised exports with showmount. Use to distinguish MOUNT-service discovery from NFSv4 availability, current client sessions and actual file permissions.
---

# Inspect an NFS export advertisement

Define `server` as one approved NFS host and `listing` as a fresh local output file. Check the nfs-utils entrypoint, then query its MOUNT service:

~~~bash
showmount --version
showmount --exports "$server" >"$listing"
~~~

Check the exit status and diagnostic output before interpreting the file. An **illustrative** row `/srv/backups *` advertises that export to all client hosts in this listing; it does not prove readable contents, write access, a particular security flavor or disabled root squashing. Retain the exact export path and reported client restriction, then verify server/version/security context before a separately authorized mount.

An empty list, RPC timeout or unavailable MOUNT service does not prove NFS is absent. NFSv4-only servers need not expose that service, and their client-visible paths can differ from server filesystem paths. Use a known NFSv4 export from server configuration or the administrator instead of guessing exports or downgrading the server.

Bare `showmount` reports recorded clients; `-a` includes client/directory pairs. Those records are implementation-dependent and may be stale. Sorted, deduplicated output cannot count multiple mounts or prove a client is currently active. State the observation as an advertisement or recorded mount entry, not a live connection inventory.

Use the [nfs-utils showmount manual](https://man7.org/linux/man-pages/man8/showmount.8.html) for discovery limits and [export policy documentation](https://man7.org/linux/man-pages/man5/exports.5.html) when interpreting access restrictions.
