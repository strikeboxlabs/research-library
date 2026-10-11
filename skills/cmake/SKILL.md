---
name: cmake
description: Configure and build an existing reviewed CMake project in a separate build directory. Use when source/build roots, cached toolchains or missing dependencies make a walkthrough's build command ambiguous.
---

# Configure before building the selected project

Read this entire SKILL.md before acting. Require reviewed project/build scripts, dependencies and an available compiler/native build tool. Select explicit source/build roots, check configuration before building, and finish with actual diagnostics and artifact identity. No conditional resources are required; a successful build is separate from running or installing its outputs.

Confirm `cmake --version`. For CMake3.13+ define `source_dir` as the reviewed project root containing CMakeLists.txt and `build_dir` as a fresh owned path outside its source tree:

~~~bash
cmake -S "$source_dir" -B "$build_dir"
~~~

Only after configuration succeeds:

~~~bash
cmake --build "$build_dir"
~~~

Configuration creates the build tree/cache and can execute project-defined commands or fetch dependencies. The build invokes the selected native generator and project build steps. Inspect those inputs before either phase; configuration is not passive source inspection. A missing submodule/header/compiler/generator is a specific prerequisite, not permission to install arbitrary dependencies or erase a cache.

The historical `cmake ..` form uses the current directory as build tree and resolves `..` from there; it is not equivalent when invoked from another directory. An existing CMakeCache.txt can preserve a different source/toolchain/generator. Choose a new build tree for a deliberately changed configuration rather than mixing it with an unrelated previous build.

Match the project's documented options and single/multiple configuration generator. Add `--config` only for the actual selected configuration when needed. Zero build status establishes completion of those build steps, not all expected binaries, protocol behavior or installation. Inspect the actual output paths and formats before a separately intended launch. `cmake --install` is an additional mutating operation and is not part of this build-only task.

Reference: [CMake configure/build command modes](https://cmake.org/cmake/help/latest/manual/cmake.1.html).
