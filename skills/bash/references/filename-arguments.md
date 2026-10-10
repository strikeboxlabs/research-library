# Keep shell filenames separate from application syntax

Inspect the actual interpreter, directory, glob options and child argv. Bash expands an unquoted `*` before running a program; double-quoting the entire `*` instead passes one literal asterisk. Quoting an array preserves each resulting name but cannot prevent the child from interpreting a name as an option or listfile.

For a selected owned directory, define `input_dir` as its absolute path and inspect the arguments without launching the backup or cleanup job:

~~~bash
(
  cd -- "$input_dir" || exit
  shopt -s nullglob
  inputs=(./*)
  printf 'arguments=%s\n' "${#inputs[@]}"
  printf '<%s>\n' "${inputs[@]}"
)
~~~

`./` makes ordinary leading `-` or `@` filenames less likely to become child syntax. Use the child program's actual end-of-options/listfile rules as well; `--` behavior is implementation-dependent. Display output is not an unambiguous serialization of names containing newlines. Preserve exact argv or NUL-separated names when reconstructing a disputed invocation.

Default `*` omits dotfiles. With no matches, ordinary Bash leaves the literal pattern; nullglob removes it, while failglob fails expansion. An empty array therefore needs an explicit skip/result rather than accidentally invoking a child that defaults to all files. Set dotglob only when hidden entries are intended; shell options and the working directory belong to this invocation, not the user's interactive shell.

A privileged process receiving writable filenames can expose a second parser boundary even when shell injection is absent. Reproduce that boundary with owned marker names/data and the selected child, retaining status and resulting artifact/log. It does not follow that a symlink's content was archived, that a process was root, or that a test bypassed the whole application's policy.

Do not rerun a source backup script to test one parsing question: its xargs/rm/truncate phases can delete inputs or erase evidence. Its cleanup wildcard can omit hidden files; fixed text listings also lose pathname boundaries. Select the harmless phase needed for the task and establish any later change separately.

Reference: [Bash filename expansion](https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html); installed Bash help/options establish local behavior.
