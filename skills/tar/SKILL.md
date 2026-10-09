---
name: tar
description: Inspect GNU tar backups and extract selected members into a new directory. Use when member names, compression, ownership or SQLite sidecar files make a quick extraction misleading.
---

# Inspect before restoring files

Define `archive` as an existing absolute local path. Inspect actual member names and types before choosing an extraction:

~~~bash
tar --version
tar --list --verbose --file="$archive"
~~~

GNU tar normally recognizes compression when reading an archive file; a filename ending in `.tar.gz` alone does not prove its format. An early listing followed by a decompression/truncation error is incomplete coverage. Check the final status. For stream input, confirm the required decompressor/options separately.

An extraction that ends in unexpected EOF may already have written useful members. Preserve the original and label the output partial; do not suppress the error or overwrite it during retries. If a recovered member is itself an archive, test/list that inner file independently. An intact inner archive does not prove the outer archive was complete or that other members survived. If practical, re-acquire the original and compare before accepting recovered evidence.

Define `member` as an exact observed member name, including any leading `./`, and `destination` as a new absolute directory. Extract as an ordinary user:

~~~bash
umask 077
mkdir -m 700 "$destination" && tar --extract --file="$archive" --directory="$destination" --no-same-owner --no-same-permissions --keep-old-files -- "$member"
~~~

The selection uses the archive name, not the destination pathname. Selecting a directory normally includes its descendants. Specify explicit filenames when only a few files are needed; a guessed basename can yield `Not found in archive` even when the file exists deeper inside it.

`--keep-old-files` returns an error on collisions; do not call that a complete extraction or rerun with overwrite enabled reflexively. `--no-same-permissions` applies the current umask; it does not remove every executable bit. Inspect paths, symlink/hardlink targets and file types before using the output. Avoid `--absolute-names`, extracting into an application tree or running scripts from the backup merely to understand them.

A SQLite database inside a backup may have same-basename `-wal` and `-shm` files. Retain that coherent captured set instead of selecting only the main database and claiming it contains the latest committed data. Archive extraction does not establish that the backup was taken consistently while its application was writing.

Record the archive identity, selected names, extraction status and resulting files. Missing members, permission errors and a corrupt archive require different next steps.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Artificial pp. 8, 11; Awkward pp. 17–18. Sources: [GNU extraction](https://www.gnu.org/software/tar/manual/html_section/extract.html), [option semantics](https://www.gnu.org/software/tar/manual/html_node/Option-Summary.html), [SQLite WAL files](https://sqlite.org/wal.html).
