# Inventory approved SMB share metadata

Require one owned host whose readable shares are approved for recursive metadata inventory, a known login pair and a fresh private output directory. The `spider_plus` module discovers shares and starts at readable share roots; it is not a selected-file download or a guaranteed one-share operation. Use a narrower client if host-wide discovery exceeds the task.

Reuse the verified `nxc_bin`, `target`, `domain`, one-line `users_file` and `passwords_file` inputs from the entrypoint. Inspect this installed module's options and source when defaults differ; define `output_dir` as a fresh absolute private directory. For its metadata-only default:

~~~bash
umask 077
mkdir -- "$output_dir" || exit 1
"$nxc_bin" smb "$target" -d "$domain" -u "$users_file" -p "$passwords_file" \
  --no-bruteforce -M spider_plus -o "OUTPUT_FOLDER=$output_dir"
status=$?
~~~

Omit download-related module keys entirely. In the reviewed implementation, the presence of any option key containing `DOWNLOAD` enables downloading—even `DOWNLOAD_FLAG=False`. Inspect the startup settings immediately and require `DOWNLOAD_FLAG: False`; a boolean-looking value is not a reliable disabling syntax.

The default exclusion filter covers selected share/folder/file names. Current code tests share exclusions by exact name and child names by substring; these are not strong scope controls for unknown future shares. Extension exclusions and the maximum file size apply after metadata recording, to downloads, so a large executable's metadata can appear even when a small download limit is printed. Metadata includes names, sizes and formatted times, not verified file contents. Do not interpret `*_epoch` field names as numeric epoch values without inspecting the JSON.

Retain startup settings, share/path association, actual output filenames and traversal errors/statistics. A saved JSON report can contain partial data after denied paths or timeouts. Presence of a filename does not establish file-read permission; absence can reflect filters, unreadable paths or incomplete traversal. Inspect selected content only through a separately authorized transfer and verify its bytes. Keep metadata/transcripts private and report what was traversed, filtered or unresolved. See the [module implementation](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/modules/spider_plus.py) for version-specific behavior.
