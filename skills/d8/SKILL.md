---
name: d8
description: Run a reviewed local JavaScript fixture with V8's d8 developer shell and interpret version, output and interactive-state differences. Use for engine-level JavaScript checks that do not require a browser or Node.js APIs.
---

# Run an engine fixture

Read this entire SKILL.md before acting. Require the actual trusted d8 build and a reviewed local script with understood file/process effects. No conditional resources are required. Finish with build/version, arguments, script status and relevant output; an interactive value does not establish browser behavior.

Define `d8_bin` as the verified absolute build artifact, `script` as the owned fixture and `log` as a fresh output. Inspect this build's supported flags:

~~~bash
"$d8_bin" --help
"$d8_bin" "$script" >"$log" 2>&1
status=$?
~~~

Use console.log in a reviewed fixture to print the requested result. Check final status and diagnostics before interpreting it. Ordinary interactive execution can print an expression result such as illustrative `undefined` after a successful print; that is not an execution failure. A script file avoids confusing persisted interactive variables with a fresh run.

d8 is V8's developer shell. Browser DOM APIs and Node-specific modules are not implied. Its read/load helpers access or execute local content; loading a script is execution. Pass selected script arguments after `--` when supported, and preserve their exact values with the result.

Native debug intrinsics and object layouts depend on the actual build and flags. A release/debug output from one historical engine does not establish the other's internal layout, pointer representation or protections. Keep this task to normal engine fixtures; require matching build evidence before interpreting low-level diagnostics.

See [V8's d8 guide](https://v8.dev/docs/d8).
