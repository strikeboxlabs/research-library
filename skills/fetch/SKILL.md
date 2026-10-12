---
name: fetch
description: Acquire an approved V8 workspace with Chromium depot_tools fetch, including its dependency layout. Use when a plain Git clone omits the metadata needed for the intended build.
---

# Acquire a V8 workspace

Read this entire SKILL.md before acting. Require the intended trusted depot_tools installation, Git, its supported Python/bootstrap environment and approval to acquire the project's dependencies and run its setup. No conditional resources are required. Finish with the workspace, observed revision and acquisition/setup status; source acquisition is separate from a build.

The tool here is depot_tools `fetch`, not another executable with the same name. Its wrappers can bootstrap runtimes or update themselves. Resolve that installation before calling its help. Define `fetch_bin` as its verified invocation and `workspace` as a fresh absolute directory with sufficient space:

~~~bash
"$fetch_bin" --help
mkdir -- "$workspace" && (
  cd -- "$workspace" || exit
  "$fetch_bin" v8
)
status=$?
~~~

Check the final status and retained diagnostics. Inspect the actual created .gclient and v8 checkout rather than assuming a failed command left nothing. Fetch wraps gclient and the project's acquisition configuration; it can download dependencies and invoke setup, so this is not passive inspection of an arbitrary project.

For this V8 configuration, record the created checkout's HEAD and local changes before selecting a requested revision. A detached HEAD can be expected; do not invent a branch or pull to change that state. Selecting another revision also requires its corresponding dependency synchronization. Do not reuse or erase a partially populated workspace blindly.

See [V8 source acquisition](https://v8.dev/docs/source-code) and [depot_tools behavior](https://chromium.googlesource.com/chromium/tools/depot_tools/+/main/README.md). Installation and system build dependencies remain separate actions.
