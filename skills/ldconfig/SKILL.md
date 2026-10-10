---
name: ldconfig
description: Inspect and deliberately refresh Linux shared-library caches with ldconfig. Use when configured directories, SONAME links or writable library locations explain an unexpected dependency or privileged load.
---

# Shared-library cache and directory decisions

Read this entire SKILL.md before acting. Select cache inspection or a deliberate update; ordinary `-v` can change cache and links. For a writable-directory or privileged-load test, read [cache selection and controlled loading](references/cache-and-load-tests.md) fully first. Finish with observed cache/resolution evidence and, if requested, actual controlled execution plus restoration; directory order alone is insufficient.

Define `ldconfig_bin` as the verified installed invocation, `cache_report` and `scan_report` as fresh files. Inspect the existing cache and configured directories without rebuilding it or updating links:

~~~bash
"$ldconfig_bin" --version
"$ldconfig_bin" -p > "$cache_report"
"$ldconfig_bin" -v -N -X > "$scan_report" 2>&1
~~~

`-p` describes cached candidate libraries; the directory scan describes current inputs. Retain errors and compare them: a stale cache or unreadable directory can explain disagreement. `-N` alone still permits link updates; `-X` alone still permits cache rebuilding. `-n` restricts scanning to command-line directories and implies no cache rebuild, but can still update their links without `-X`.

Inspect `/etc/ld.so.conf` and its actual include directives, not just a guessed glob of fragments. Library architecture, ELF metadata/SONAME and the recognized `lib*.so*` filename matter. A file present in a directory is not necessarily the matching cache candidate.

For an approved refresh using the reviewed configuration and intended libraries, `"$ldconfig_bin" -v` rebuilds the cache and may update library links. Capture status/diagnostics and then inspect `-p`; already running processes do not automatically reload their libraries. Use `-X` on a refresh when link changes are deliberately excluded and the needed filename/links already exist. Default system paths and cache are image facts to verify, not paths to invent from a different machine.

Use the [option manual](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man8/ldconfig.8) and [glibc implementation](https://github.com/bminor/glibc/blob/master/elf/ldconfig.c) for installed-version differences.
