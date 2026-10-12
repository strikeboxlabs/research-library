---
name: luvit
description: Run one reviewed ordinary Lua file with an installed Luvit runtime. Use when a script expects Luvit modules or when runtime identity, working-directory resolution and event-loop completion need clarification.
---

# Run the selected Luvit file

Read this entire SKILL.md before acting. Select a trusted installed runtime and one reviewed ordinary Lua file, including its required modules and intended effects. No conditional resources are required. Finish with the runtime identity, working directory, status, output and observed task result; an unfinished event loop is not completion.

Set `luvit_bin` to the verified absolute executable, `script_parent` to its trusted working directory and `script_name` to the selected basename that does not begin with a hyphen. Confirm the installed interface before execution:

~~~bash
"$luvit_bin" --version
"$luvit_bin" --help
(cd -- "$script_parent" && "$luvit_bin" "$script_name")
status=$?
~~~

Run as the ordinary account selected for the task. Luvit interprets executable Lua and loads modules; reviewing only the entry file does not establish the effects of its dependencies. Resolve missing modules against that project's installed dependency layout rather than replacing Luvit with an arbitrary Lua interpreter. Preserve stdout, stderr and status separately. A successful launch does not prove the script produced its intended artifact or service result; inspect that result before reporting success.

The script resolves relative to the working directory. With no script, the CLI can enter an interactive REPL and write history; do not omit the file during a batch task. A script that keeps active event-loop handles may remain running after its initial output. Use the task's agreed runtime limit and cleanup procedure, and record an interrupted run as incomplete.

For CLI parsing and event-loop behavior, consult the installed version alongside upstream [main.lua](https://github.com/luvit/luvit/blob/master/main.lua) and [init.lua](https://github.com/luvit/luvit/blob/master/init.lua).
