---
name: ninja
description: Build a selected target from an existing generated Ninja graph and diagnose generator, compiler or stale-output failures. Use when GN or CMake has already configured a trusted build directory.
---

# Build a generated target

Read this entire SKILL.md before acting. Require a reviewed source tree, its generated build.ninja and the intended configuration/compiler. No conditional resources are required. Finish with the target, status and resulting artifact identity; compilation is separate from running tests or installing the program.

Define `build_dir` as the absolute generated directory, `target` as its actual target, `jobs` as a chosen positive concurrency limit and `build_log` as a fresh log. Inspect the installed implementation and graph:

~~~bash
ninja --version
ninja -h
ninja -C "$build_dir" -t targets all
ninja -C "$build_dir" -t query "$target"
~~~

Check statuses and use the graph's exact target name. Ninja consumes a generated graph; it does not choose debug/release mode or discover missing compiler dependencies. Configure those through the project's generator first. A missing build.ninja means the directory or generation step is wrong, rather than a reason to create an improvised file.

~~~bash
ninja -C "$build_dir" -j "$jobs" "$target" >"$build_log" 2>&1
status=$?
~~~

Inspect the first consequential failed command and its output. `-C` changes the build directory; `-j` bounds parallel commands. With no explicit target, graph defaults determine the work. Build rules can execute generators and other programs; inspect unfamiliar inputs before any build. `-t commands` displays commands without establishing that they ran.

Zero status or illustrative `no work to do` can describe an existing output. Check that artifact against the selected source/configuration; an old file left after failure is not a completed rebuild. Missing headers, libraries, tools and malformed graph inputs need their own repair. Avoid deleting the build tree or invoking clean merely to obtain a fresh-looking log.

See the [Ninja manual](https://ninja-build.org/manual.html#_running_ninja) and [graph tools](https://ninja-build.org/manual.html#_extra_tools).
