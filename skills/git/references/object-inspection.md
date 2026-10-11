# Read acquired Git objects without a checkout

Use this when a preserved object store exists but worktree files or refs are incomplete. Define `repo` as an isolated acquired repository and `oid` as a complete observed object ID, not an assumed hash from a filename. Establish repository object format and inspect the type before content:

~~~bash
git -C "$repo" rev-parse --show-object-format
git -C "$repo" cat-file -t "$oid"
git -C "$repo" cat-file -s "$oid"
git -C "$repo" cat-file -p "$oid"
~~~

Check each result separately. A commit's content names its tree and parents. A tree lists modes, names and child IDs. A blob holds file bytes; its ID does not encode a pathname. Follow only the selected acquired IDs and record missing children rather than claiming the whole source tree was recovered. For a selected tree, `git -C "$repo" ls-tree -z "$oid"` provides NUL-framed entries without extracting or following stored links.

An ordinary symbolic `HEAD` contains a ref name; detached `HEAD` can contain an object ID. Loose refs, packed refs and the available object store must be considered separately. SHA-1 and SHA-256 repositories use different object IDs; do not invent a compatible repository from a truncated screenshot.

Preserve compressed loose-object bytes as binary. Raw zlib bytes are not a file's plaintext. JSON/hex transport needs validated field type, complete even-length hex and independent length/digest checks before using Git's parser. A pretty-printed tree or commit is metadata, not a file to execute. Packed objects need their corresponding pack/index context rather than an assumed loose-object pathname.

Complete a selected file read with its containing tree/path, blob ID, byte count and any integrity/coverage gap. Git accepting an object does not establish trusted application code, current account authority or complete history. See [cat-file](https://git-scm.com/docs/git-cat-file), [repository layout](https://git-scm.com/docs/gitrepository-layout) and [tree listings](https://git-scm.com/docs/git-ls-tree).
