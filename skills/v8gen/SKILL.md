---
name: v8gen
description: Generate a selected V8 GN build configuration with the checkout's v8gen helper. Use when debug and release output directories or architecture choices need to be established before compilation.
---

# Generate V8 build inputs

Read this entire SKILL.md before acting. Require the trusted V8 revision, synchronized dependencies, build prerequisites and that revision's tools/dev/v8gen.py. No conditional resources are required. Finish with generation status, actual output directory and effective configuration; generation alone produces no tested runtime.

Define `v8_dir` as the absolute checkout and `configuration` as a name supported by its own helper. Run from the source root:

~~~bash
(
  cd -- "$v8_dir" || exit
  ./tools/dev/v8gen.py --help
  ./tools/dev/v8gen.py list
)
~~~

Check the applicable help/list results before choosing the configuration and any helper options. The launcher/interpreter must match the checkout; an old writeup is not evidence that a current revision supports its configuration name or Python environment.

~~~bash
(
  cd -- "$v8_dir" || exit
  ./tools/dev/v8gen.py "$configuration"
)
status=$?
~~~

Inspect status, diagnostics, generated GN arguments and the actual build.ninja path. Output-directory spellings vary between workflows; do not guess out/ versus out.gn/ or reuse another configuration's d8. Resolve missing toolchain/dependency or unknown-configuration errors before compiling. Building that graph and running the produced binary are separate steps; preserve source revision and effective build options with their results.

See [V8's manual GN workflow](https://v8.dev/docs/build-gn#generate-build-files-using-v8gen).
