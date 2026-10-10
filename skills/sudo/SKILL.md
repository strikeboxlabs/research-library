---
name: sudo
description: Interpret sudo policy, RunAs identities, helper paths, environment handling and sudoedit on Linux. Use when a permitted command behaves differently under sudo or a walkthrough overstates privilege from a policy listing.
---

# Understand the permitted operation

Read the effective listing before selecting an elevated command:

~~~bash
sudo -l
sudo -ll
~~~

Listing may require authentication. For unattended inspection, `sudo -n -l` fails instead of prompting; that failure does not by itself mean no policy entry exists. Record the target RunAs user/group, command path, argument restrictions and tags together. `(dev_admin : dev_admin)` is a permitted target identity, not a root grant.

An additional PAM prompt can be a separate authentication requirement, not another request for the account password. Inspect readable `/etc/pam.d/sudo` and its included stacks when diagnosing it. A failed `required` module can still allow later prompts before the stack rejects authentication. Keep authentication failure distinct from sudo policy denial; an interrupted challenge does not establish the effective policy. Diagnose the configured requirement without editing PAM to bypass it.

`NOPASSWD` affects authentication for matching entries; it does not grant arbitrary commands. `SETENV` changes environment restrictions for the matching operation. `env_reset` and `secure_path` can explain why a program works normally but finds different variables or executables under sudo.

A sudoers command entry with no argument specification permits any arguments; an explicit `""` argument specification permits none. Thus a path-only daemon grant can include options selecting a different configuration. For Nginx, inspect permitted `-c`/`-g` inputs, included files and module paths: configuration controls worker identities, listeners and file operations. Record that authority without launching a replacement privileged service. A configuration-test flag does not make arbitrary module/configuration loading passive.

In command-argument patterns, sudoers wildcards can match whitespace and span arguments; `*` is not necessarily one filename. That policy pattern differs from typing an unquoted `*` in the invoking shell, which can expand filenames before sudo receives the arguments. Use explicit documented arguments when assessing a permitted operation. Interpret the actual permitted operation, including options. Package installers can execute hooks, and backup tools may execute a password-helper command. Build/runtime commands such as `dotnet run` can execute a selected project's build logic and application. `iptables-save -f` writes the selected file with the program's privileges, unlike redirection performed by the invoking shell. Restricting the executable name alone does not make its subcommands passive inspection. Preserve the effective policy and program semantics together before drawing a privilege conclusion.

A grant for an interpreter plus one exact script path does not grant arbitrary `python -c` execution, but the permitted script can still consume caller-controlled data through stdin, prompts, files or configuration. Follow that data into the script's actual operations. Root ownership of the script does not make its inputs trusted. An `eval` of file content happens before a later result check, so a final "invalid input" message does not establish that no earlier effect occurred. Preserve the exact policy, source locations and input path; separate that review from running the elevated script.

For a helper path such as `./check.sh`, inspect the process working directory, not just PATH or the parent script's location. Sudo normally preserves the invoking directory, but `CWD`/`runcwd`, login mode, the wrapper's own directory changes or a subprocess `cwd` can alter it. A slash-containing relative path is not resolved through `secure_path`. Establish the helper's resolved location and who can modify it; a repository copy is a lead until matched to deployed code. An argument list with `shell=False` does not make a caller-controlled executable path trustworthy. See [Python subprocess path resolution](https://docs.python.org/3/library/subprocess.html#popen-constructor) for that distinction.

With an explicit interpreter invocation, the target identity must be able to read the script; the script's execute bit alone does not provide the unprivileged caller with readable Python source. Keep file-mode observations separate from the interpreter and RunAs policy.

A permitted executable may launch helpers by name. A Forge trace showing a `git` command is a lead about helper invocation, not proof that a caller-controlled PATH survives sudo or that a replacement would run. Check `secure_path`, RunAs identity, environment permissions, helper search directories and the exact target version together. Application trace logging is not a complete syscall trace. Do not generalise a local build's behavior to an unreadable privileged binary or execute a modified helper to establish the policy finding.

`sudo -E` asks policy to preserve the **exported environment** and can be denied. A shell-only assignment such as `PYTHONPATH=/some/path` on its own need not be exported, so a following `sudo -E` failure does not prove that variable preservation is universally broken. Distinguish shell export state, sudo filtering and the target program's own startup rules. Preserve only the variable actually needed; inspect the permitted wrapper's imports, config and child commands before changing their environment.

For `SETENV` wrappers, inspect the environment consumed by every child as well as the wrapper itself. An absolute executable path fixes lookup but not its runtime configuration. Clearing `PERL5LIB`/`PERLLIB` alone does not address Perl startup options or debugger configuration; inspect `PERL5OPT`, `PERL5DB`, invocation and taint-mode conditions using [perlrun](https://perldoc.perl.org/perlrun). A curl child can similarly consume proxy settings. Record which settings survive and which operations occur before a later guard. A `NOSAVE` branch after network retrieval and XML parsing skips the later write, not those preceding operations. Review the code without invoking the elevated wrapper just to test that conclusion.

For an authorized edit, define `run_as` as the permitted target user and `file` as the exact allowed absolute path:

~~~bash
sudoedit -u "$run_as" -- "$file"
~~~

`sudoedit` edits temporary copies as the invoking user, then uses privilege to copy changes back. It is different from launching an editor itself under sudo. A saved editor buffer does not prove the final copy-back succeeded; inspect errors and the resulting file. File/path safety checks can reject an otherwise listed edit.

When evaluating a historical sudo vulnerability, inspect the installed distribution package and its advisory/patch status. The upstream-looking string from `sudo --version` alone does not establish that a distro build is vulnerable. Record observed policy and behaviour separately from an exploitation hypothesis.


For a permitted `git pull`, include the working directory in the policy assessment. The chosen repository can supply local configuration and executable hooks, so an exact executable/subcommand restriction alone does not establish a passive update. A Linux `post-merge` hook may run after a successful merge-path update, including a fast-forward; an already-current checkout or conflicted merge is different. Inspect the selected repository, effective hook path, script and ownership checks before concluding that a listed grant permits execution of a particular hook. A GitLab webhook merely explains what launched the local command; it is not that local hook. Do not invoke the elevated pull just to discover its effects.

Consult the [sudoers policy manual](https://github.com/sudo-project/sudo/blob/main/docs/sudoers.man.in) for command matching and [Git's hook events](https://git-scm.com/docs/githooks) for the permitted program's behavior.
