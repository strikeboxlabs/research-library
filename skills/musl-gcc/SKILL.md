---
name: musl-gcc
description: Build a reviewed C utility against musl with its GCC wrapper. Use when static linking, compiler provenance or libc and target-architecture mismatches affect an owned Linux artifact.
---

# Select the musl toolchain before compiling

Read this entire SKILL.md before acting. Require the installed wrapper, backend compiler, matching musl headers/libraries and reviewed C source. No conditional resource is required. Finish with the source/build identity, diagnostics and inspected artifact; compilation alone does not establish target execution or universal portability.

Define `compiler` as the verified musl-gcc executable and `source`/`output` as the reviewed C file and a fresh absolute output path. Check its package/wrapper configuration and backend before compiling:

~~~bash
"$compiler" --version
"$compiler" -dumpmachine
"$compiler" -Wall -Wextra -Og -g -static "$source" -o "$output"
status=$?
~~~

musl-gcc wraps GCC using a specifications file selecting musl include/library paths. Its --version output identifies the backend compiler; do not report that string as the musl libc version. The target triple and matching libraries determine architecture. This wrapper does not turn native GCC into an arbitrary cross compiler or supply every third-party dependency.

Require successful status and retain warnings. Missing headers/static archives and glibc-specific interfaces need matching dependencies or source review, rather than mixing glibc objects into the musl build. Do not remove stack protection or other checks merely because a historical command did so. `-static` requests static linking; inspect the result with the installed file/readelf tools for architecture, interpreter and dynamic dependencies before transferring it.

A static Linux executable still depends on its CPU and kernel ABI and on the program's filesystem, configuration and external-service assumptions. It is not portable to every operating system. Run only the separately approved owned program in the selected fixture, and retain its actual result independently of the build.

See the [musl-gcc wrapper manual](https://manpages.debian.org/unstable/musl-tools/musl-gcc.1.en.html) and [GCC linking options](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html) for the installed generation's contract.
