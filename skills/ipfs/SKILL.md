---
name: ipfs
description: Inspect a local Kubo IPFS repository and recover selected UnixFS files offline. Use when distinguishing block inventories from filenames, resolving CID codecs or diagnosing missing local content without fetching from peers.
---

# Recover selected local content with Kubo

Use the Kubo `ipfs` executable. Check `ipfs version` and local help for the repository version and options. IPFS is a content-addressed system; it does not require a blockchain. A CID identifies encoded content, not its author, confidentiality or filename.

Define `repo` as an existing, authorized repository working copy with its matching configuration and block store. Work with a consistent copy whose daemon is not running; Kubo can lock/write local repository metadata even for read commands. Set the repository explicitly rather than opening the worker's default store. On lock or repository-version errors, stop and resolve the copy/version mismatch; do not initialize, migrate or garbage-collect the evidence to make a read succeed.

Define `inventory` and `inventory_errors` as fresh private files:

~~~bash
umask 077
export IPFS_PATH="$repo"
ipfs --offline --timeout=30s refs local >"$inventory" 2>"$inventory_errors"
~~~

Keep the exit status and errors. A timeout can leave a partial inventory. This lists stored blocks, including chunks and metadata; it is not a file catalogue or proof that complete files are present. Current Kubo reports these keys as CIDv1 with the raw codec. A historical loop feeding every result into `ipfs ls` can therefore fail or interpret DAG metadata as raw bytes. Do not guess another codec merely to force a parse.

Locate original root CIDs from an acquisition manifest, known links, local pins or the mutable filesystem (MFS):

~~~bash
ipfs --offline --timeout=30s pin ls --type=recursive
ipfs --offline --timeout=30s files ls -l /
~~~

These are separate views. Pins identify retention intent; MFS supplies its current names; neither enumerates every historical cached file. An empty MFS root is compatible with a nonempty block store. For a selected MFS path, `ipfs --offline files stat --hash "$mfs_path"` gives its CID, where `mfs_path` is the actual path just observed.

## Follow one directory to the actual file bytes

Define `directory_cid` as a verified UnixFS directory CID, and retain its listing and errors:

~~~bash
ipfs --offline --timeout=30s ls "$directory_cid"
~~~

Choose the relevant child by name and CID, keeping that parent/child relationship. A displayed directory size is not necessarily the size of a recovered file. Define `file_cid` as the selected file CID, `artifact` as a fresh output file and `errors` as its new error log:

~~~bash
if ipfs --offline --timeout=30s cat "$file_cid" >"$artifact" 2>"$errors"; then
    wc -c -- "$artifact"
    sha256sum -- "$artifact"
else
    printf '%s\n' 'Incomplete local retrieval; keep output as partial evidence.' >&2
    false
fi
~~~

Use this for a selected file of understood size. For an unknown/large file, start with `cat --length=65536` into a separate preview; a successful capped read proves only that prefix. Retrieve the complete file only when its size and scope are understood. Missing blocks offline leave content incomplete; they do not prove the file never existed. A directory error calls for `ls`, not repeated `cat`. Preserve errors instead of discarding stderr in an enumeration loop.

Ordinary online commands may fetch absent blocks from peers. Keep `--offline` for local-only inspection, and do not start a daemon or use an HTTP gateway as an automatic repair. Parse recovered mail, keys or archives with their own readers; names and a successful `cat` do not establish authenticity or permission to execute content.

Use the [Kubo CLI reference](https://docs.ipfs.tech/reference/kubo/cli/) for version-specific options, [refs implementation](https://github.com/ipfs/kubo/blob/master/core/commands/refs.go) for inventory semantics and [UnixFS retrieval examples](https://docs.ipfs.tech/how-to/kubo-basic-cli/) for directory/file distinctions.
