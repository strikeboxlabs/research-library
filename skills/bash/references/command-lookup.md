# Diagnose the command that this shell resolves

Require the actual Bash context and selected command name. Define `program` as that simple name, then inspect without running it:

~~~bash
type -a -- "$program"
enable -a
hash -t -- "$program"
~~~

Retain each status: an absent hash entry is not absence from PATH. Type can identify aliases, functions, builtins and disk candidates; enabled builtins normally precede disk lookup. An acquired `enable -n` statement disables the named builtin in the shell executing it, allowing a same-named disk command to be selected. It is not a permission change and does not disable every related construct; `[` and `[[` are different.

Inspect the script's interpreter, sourced files and effective environment together. A bare name can resolve differently from an absolute path. Sourcing an acquired rc file executes it in the caller's context; read it as data rather than invoking a cleanup job to diagnose lookup. A custom rc basename does not make it an automatic startup file.

Finish with the selected lookup kind/path, enabling state and unresolved execution context. A current interactive result does not establish a historical scheduled job's lookup or identity.

Reference: [Bash command search and builtins](https://manpages.debian.org/bookworm/bash/bash.1.en.html).
