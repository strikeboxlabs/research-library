# Backup arguments, listfiles and links

Establish the actual 7-Zip/p7zip version, archive type, input directory, invocation identity and log redirections. The shell expands an unquoted `*` first; 7-Zip then interprets arguments. An argument starting `@` can name a text listfile, whose lines become archive input paths. Quoting a shell expansion preserves argument boundaries but does not disable this application's parsing.

`--` in current 7-Zip stops switch **and @listfile** parsing. Older p7zip/7-Zip can differ: observed p7zip 16.02 processed a listfile even after that switch. Confirm the installed implementation with owned data rather than claiming the old behavior universally. `-spd` disables 7-Zip wildcard matching, not shell expansion or every listfile mechanism. `-scsUTF-8` selects listfile encoding; a text list is not a NUL-delimited find result.

## Create and verify a selected archive

Define `input_dir` as the reviewed absolute tree, `output_archive` as a fresh absolute path outside that tree, and `sevenzip` as the verified executable:

~~~bash
(cd -- "$input_dir" && "$sevenzip" a -t7z "$output_archive" -- .)
"$sevenzip" l -slt "$output_archive"
"$sevenzip" t "$output_archive"
~~~

Check creation status before accepting the listing/test. `a` can update an existing archive, hence the fresh destination. Explicit `-t7z` determines the format even if someone names the file .zip; inspect the actual type. Selecting `.` requests that tree, including hidden entries; bare `*` omits ordinary dotfiles in Bash. For individually selected operands, use reviewed `./name` paths to prevent leading `@`/`-` names becoming syntax. An intentionally used `@listfile` belongs before the modern `--`, with reviewed paths and encoding.

Creation warnings or unreadable/skipped inputs can leave a readable but incomplete archive. Retain both stdout/stderr and status; test success verifies the produced archive, not that every intended source was included. Password/encryption choices must match the job's requirements. `-pPASSWORD` can expose the value in argv; use the installed implementation's prompt/approved input method and confirm encrypted-format/header behavior separately.

`-snl` requests storing supported symlinks as links; format/platform/version support differs. Inspect the actual resulting members before using it as a backup guarantee. It does not prevent the CLI from opening an intentionally interpreted listfile, including one reached through a symlink under the process's file permissions. Filename control, symlink storage and listfile reads are separate questions.

## Reproduce listfile interpretation with owned marker data

For an authorized parsing/identity reproduction, use a disposable unprivileged directory, a fresh archive outside it and **only a public owned list**. Set `fixture_dir`, `output_archive`, `stdout_file` and `stderr_file` to fresh absolute workspace paths. Do not substitute a sensitive system file or unrelated privileged job:

~~~bash
mkdir -m 700 "$fixture_dir" &&
printf '%s\n' 'MISSING_DEMO_ENTRY' >"$fixture_dir/list-lines" &&
ln -s list-lines "$fixture_dir/listfile" &&
touch "$fixture_dir/@listfile" &&
(cd -- "$fixture_dir" && "$sevenzip" a -t7z -snl "$output_archive" -- *) >"$stdout_file" 2>"$stderr_file"
status=$?
printf 'archive-status=%s\n' "$status"
~~~

Inspect the two logs and archive listing. On the old behavior, a missing-file diagnostic containing the **illustrative** `MISSING_DEMO_ENTRY` shows that list text was interpreted as a path. It does not prove that file was archived, or that the complete source list was disclosed. On modern behavior, `@listfile` after `--` is a literal member; the old marker diagnostic should not appear. A deliberately interpreted baseline can supply `@listfile` before `--` with a separate fresh output. Compare it with `-- ./*`; the leading `./` avoids ambiguous filename syntax even with older parsers.

Reproduce only the selected parser condition; do not run the source's whole backup/cleanup script. Another identity must actually be observed if identity is the question. Timestamps and file ownership alone do not identify a cron writer. An error log can leak missing-path strings while the archive is still encrypted; encryption is not log protection. Immediate log truncation or a fast consumer can erase this evidence, so capture streams during the owned reproduction. Preserve or remove only the fixture's own artifacts according to the task.

References: [upstream parser](https://github.com/ip7z/7zip/blob/main/CPP/7zip/UI/Common/ArchiveCommandLine.cpp), [maintainer explanation of -- and listfiles](https://sourceforge.net/p/sevenzip/bugs/2221/), [7-Zip](https://7-zip.org/).
