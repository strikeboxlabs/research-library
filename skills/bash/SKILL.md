---
name: bash
description: Diagnose Bash startup, restricted sessions, pattern comparisons, data reparsing, environment inheritance and redirection-order mistakes in scripts or scheduled jobs. Use when shell context or quoting changes a command's meaning.
---

# Bash execution context

Determine which shell actually runs the command; `$SHELL` identifies a preferred login shell, not necessarily the current interpreter. Within Bash, these inspect the current context:

~~~bash
printf 'Bash=%s flags=%s\n' "$BASH_VERSION" "$-"
shopt login_shell
~~~

An `i` in `$-` indicates interactive mode. For ordinary Bash invocation:

| Context | Startup behaviour to check |
|---|---|
| Login | `/etc/profile`, then the first readable user file among `.bash_profile`, `.bash_login`, `.profile`. |
| Interactive non-login | `.bashrc`; system rc files also depend on distribution/build and explicit sourcing. |
| Noninteractive script | The file named by exported `BASH_ENV`, when set. Do not assume interactive rc files were read. |

Remote-shell detection, invocation as `sh`, POSIX mode and explicit startup-suppression options change these rules. Inspect the real invocation and actual files. A user's `.bashrc` does not generically override `/etc/bash.bashrc` by precedence. A cron job does not become an interactive Bash merely because the user's login shell is Bash.

When effective and real IDs differ, Bash normally resets its effective user ID unless invoked with `-p`. Privileged mode preserves an already obtained identity; it does not grant root to an ordinary process. It also changes environment/startup handling. Inspect actual IDs and invocation when comparing behavior; a setuid-looking permission string or a root-shaped prompt alone is insufficient evidence of effective privilege.

Invoking `sh script` uses that interpreter regardless of a Bash shebang. Bash's combined-output `>&file` redirection and `/dev/tcp/host/port` handling are not portable POSIX sh features; even Bash builds can differ in network-redirection support. Bash handles that path specially while opening a redirection; it is not a kernel-provided TCP file. Check the actual command, not only the script's first line, when diagnosing a copied snippet.

`source file` executes shell code in the current shell: it can change variables, functions, directory and subsequent execution. A virtualenv activation file is executable shell input, not passive settings. Its owner does not become the executing identity; a privileged process sourcing a writable file executes that code in its own context.

A plain assignment creates/updates a shell variable; `export NAME=value` exposes it to child processes. `NAME=value command` supplies it for that command. If a variable was already exported, reassignment retains that attribute. Sudo or an application can then apply additional filtering.

Redirections run left to right. `command 2>&1 >/dev/null` discards stdout but leaves stderr pointing at the original stdout. To capture both streams, define `log` as a fresh file and redirect `command >"$log" 2>&1`. Check the command's exit status as well as its log; silence is not success. Use `bash -n script` to check syntax, remembering that it does not validate runtime paths, permissions or behaviour.


## Separate pattern matching from literal equality

In `[[ left == right ]]`, an unquoted right-hand expansion is a glob pattern. Quoting the left side alone does not change that. This harmless example distinguishes a pattern match from an exact value:

~~~bash
expected='build-42'
supplied='build-*'
if [[ $expected == $supplied ]]; then
  printf 'Pattern matched\n'
fi
if [[ $expected == "$supplied" ]]; then
  printf 'Literal match\n'
else
  printf 'Values differ\n'
fi
~~~

The results are `Pattern matched` and `Values differ`. Quote the entire right-hand expansion when the requirement is literal equality. `nocasematch` can still make this comparison case-insensitive; inspect it when case matters. Inside `[[ ]]`, the pattern behavior is separate from word splitting and filename expansion. `=~` uses a regular expression instead.

Trace where the compared input goes next. A successful input gate does not mean a child uses that input: a script can compare a supplied value, then pass a different value read from a file to the next command. Test comparison semantics with public strings before drawing conclusions about real credentials. For literal line input, `IFS= read -r` preserves surrounding whitespace and backslashes; `read -s` suppresses terminal echo but does not change comparison rules.

## Keep values out of a new command string

Quoted parameter expansion passes its value as data; Bash does not recursively execute shell syntax contained in that value. A later `bash -c` or `eval` introduces a new parsing step. Thus interpolating a certificate subject or filename into a double-quoted `bash -c` string can still turn its contents into code in the child. Outer quoting preserves the string as one argument; it does not make the child's source safe.

For an already authorized move, define `source_file` and `destination_file` as the selected complete paths and invoke directly:

~~~bash
mv -- "$source_file" "$destination_file"
~~~

If a child Bash is actually needed, keep its program fixed and pass values positionally:

~~~bash
bash -c 'mv -- "$1" "$2"' bash "$source_file" "$destination_file"
~~~

The first argument after the program becomes `$0`; the placeholder `bash` keeps the paths in `$1` and `$2`. This prevents reparsing their contents. It does not validate destination authority, prevent overwriting or stop path traversal. Derive the destination from an approved directory and a validated filename independently; a certificate CN is neither a safe filename nor a trusted shell expression.

The same extra parsing occurs when `xargs -I {}` substitutes a value inside a fixed-looking `sh -c` program: the original shell's single quotes are already gone when xargs performs replacement. Keep replacement data outside the program string, or invoke the operation directly without a child shell. Quoting the outer variable alone does not repair later program construction. Separately, a cleanup path such as `"$directory/*"` contains a quoted, literal asterisk; it does not expand to the directory contents. Diagnose these two expansion stages independently, and inspect the concrete paths before any cleanup.

When reading process telemetry, preserve argument boundaries if available. A printed `bash -c script path` can hide whether `path` belongs inside the command string or becomes `$0`. Correlate it with the caller's source before deciding what the script received. `bash -n` cannot prove that dynamic values remain data.

See Bash's [invocation, expansion and job-control manual](https://man7.org/linux/man-pages/man1/bash.1.html).

## Restricted shell or missing command path

Inside an identified Bash session, inspect its mode and lookup context with builtins:

~~~bash
shopt restricted_shell
printf 'PATH=%s\n' "$PATH"
type -a ls
~~~

`restricted_shell on` identifies Bash's restricted mode. A short PATH alone does not. Read the exact error: an unavailable `ls` may trigger a command-not-found handler whose slash-containing path is then rejected. That does not prove `ls` itself is a specifically forbidden command or that no permitted listing utility exists.

Restricted Bash rejects actions including `cd`, changing PATH, slash-containing command names and output redirection. Do not try ordinary PATH repair inside that mode and misdiagnose the failure as permissions. Restrictions constrain the shell; they do not remove other programs' file access or subprocess features. If a separately authorized child shell is already running, recheck its interpreter, identity and PATH: the path can remain limited, and another startup file can reset it. A changed prompt or a pseudo-terminal does not establish new privileges or removal of restrictions.

The Bash manual's [restricted-shell rules](https://man7.org/linux/man-pages/man1/bash.1.html#RESTRICTED_SHELL) distinguish these failures from filesystem permissions and ordinary command lookup.
