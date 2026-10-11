# Retrieve a selected FTP subtree

Require an approved FTP directory URL with a trailing slash and a fresh local destination. Confirm GNU Wget. Anonymous access being available does not expand the selected subtree. Define `ftp_url`, `mirror_dir` and `transfer_log`:

~~~bash
wget --mirror --no-parent --timeout=20 --tries=2 \
  --directory-prefix="$mirror_dir" --output-file="$transfer_log" \
  -- "$ftp_url"
status=$?
~~~

`--mirror` enables recursion, timestamps, unlimited depth and retained FTP listings. `--no-parent` constrains upward traversal; it does not cap the number of files below the selected directory. If the task requires a depth limit, choose explicit recursion/depth instead of this mirror preset. Do not use `-O` to combine multiple files into one output.

Review the log and retained `.listing` files against the requested inventory. A successful transfer of one shown file does not prove the entire mirror is complete. File-data connections are separate from FTP login; a successful login followed by a stalled listing/download can indicate a passive-mode/firewall problem. Retain that distinction before changing connection mode. Timestamp matching is an update optimization, not content authentication; use independently supplied digests when available.

Reference: [GNU Wget packaged manual](https://manpages.debian.org/bookworm/wget/wget.1.en.html).
