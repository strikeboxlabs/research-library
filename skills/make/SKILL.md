---
name: make
description: Build a selected existing Linux tool with GNU make and interpret configuration, compiler or stale-artifact failures. Use when a reviewed Makefile or configure script controls the required binary and features.
---

# Build an existing configured tool

Read this entire SKILL.md before acting; reuse complete current context. Use reviewed source/build instructions, select the intended target and bounded parallelism, and require both build completion and the expected artifact. For an Autotools project or feature missing from a produced binary, read [configured builds](references/configured-builds.md) fully before configuration or rebuilding. An installed working binary does not need a source build.

Check `make --version` for the implementation. Define `build_dir` as the existing absolute configured build directory, `target` as the actual project's intended target, `jobs` as a positive chosen worker count, and `build_log` as a fresh private log:

~~~bash
make -C "$build_dir" -j "$jobs" "$target" > "$build_log" 2>&1
status=$?
~~~

Check status before using the expected artifact. If the build instructions rely on the default target, omit the final target argument rather than guessing a binary name. `-C` selects the directory; `-j` limits parallel jobs, not compilation attempts or output size. Parallel log order need not be causal order.

A successful build can say a target is already up to date. Confirm the selected revision, configured options and expected artifact path; an old binary left by a failed rebuild is not the new result. Stop at the first consequential configure/compiler/linker error rather than treating the final `make: ***` line as its cause. Missing headers and missing libraries are different prerequisites; neither is fixed by blind retries or automatically installing tools.

Makefiles are programs. `make -n` prints much of the work but is not a passive inspection of untrusted source: recursive/`+` recipes, included-makefile rebuilding and expansion-time functions can execute. `make -q` reports 0 for up to date, 1 for work needed and 2 for an error, with similar recursive-recipe caveats. Read source as text before executing any make mode.

Finish with the selected target, build status and resulting artifact/feature evidence. Installation, service startup and running the produced program are separate actions; a build is not proof that it works on another architecture or image.

See GNU make's [execution-mode caveats](https://www.gnu.org/software/make/manual/html_node/Instead-of-Execution.html) and [manual](https://www.gnu.org/software/make/manual/make.html).
