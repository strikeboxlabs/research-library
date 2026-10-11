# Acquire one complete owned file

Use for a selected file and two known endpoints on a controlled path. Plain nc supplies neither peer authentication nor encryption; use an established authenticated transfer mechanism for sensitive material. Require the actual implementation on each end, the source's absolute path and a fresh destination outside any application tree.

On a receiver with verified OpenBSD-style listener syntax, define `bind_ip`, `port`, fresh `received` and `receiver_log` paths. Track this one foreground listener under the worker's overall budget:

~~~bash
umask 077
(set -C; nc -n -v -l "$bind_ip" "$port" >"$received" 2>"$receiver_log")
~~~

Use the entrypoint's alternative listener syntax if that implementation is traditional. A redirected output can be created before a bind failure; existence or nonzero size is not acquisition completion. Do not use -k to combine multiple connections into this artifact.

On a sender supporting OpenBSD-style -N, define `receiver_ip`, the same `port`, the absolute `source_file` and a fresh `sender_log`:

~~~bash
nc -n -v -N -w 10 "$receiver_ip" "$port" <"$source_file" 2>"$sender_log"
~~~

The input redirection reads that local file; a same-named file in another working directory is different evidence. -N shuts down sending after input EOF. Traditional -q behavior differs; choose its installed contract instead of deleting the EOF option reflexively. The sender's idle/connect timeout is not a total transfer deadline, and -w does not bound the receiver's initial listen wait.

Require both final statuses/logs and independent source-versus-received byte count and digest comparison, keeping the source stable during acquisition. A disconnected stream can be truncated without identifying the intended file length. A matching checksum acquired through the same untrusted path supplies no independent provenance. Keep a failed/partial capture separately and use a fresh retry output. Do not execute a received binary to determine whether transfer worked; retain its acquisition identity for static analysis.

See [OpenBSD data transfer and EOF](https://man.openbsd.org/nc#DATA_TRANSFER) and the [traditional implementation](https://manpages.debian.org/bookworm/netcat-traditional/nc.1.en.html).
