---
name: nimble
description: Inspect and provision selected dependencies for an existing Nim tool using Nimble. Use when a Linux build needs Nim packages and package identity, versions or user installation context explain failures.
---

# Resolve the intended Nim dependencies

Read this entire file before acting. Inspect the tool's package requirements and installed Nim/Nimble versions. Finish with the selected versions and resulting package/build evidence; installation success does not establish that a tool's generated artifact works.

~~~bash
nimble -v
nimble list --installed
~~~

Use the installation context belonging to the worker/build identity. A package installed under a different user or Nimble directory may not be available to this build. The installed package list describes local versions; a registry search result does not prove installation.

When dependency installation is an authorized task, define `package_spec` as the reviewed name/version specification and install that selection:

~~~bash
nimble install "$package_spec"
~~~

For example, the syntax `package@VERSION` selects a version; substitute a real requirement instead of inventing a pin. An unpinned installation can select a newer release than the source project used. Review package origin and build hooks; installation can fetch dependencies and compile code. It is a separate state-changing operation, not a routine side effect of reading this skill.

For a reviewed local project with a `.nimble` definition, run `nimble install --depsOnly` from that project directory when only its dependencies should be installed. It still installs missing dependencies into the active Nimble package store. Leaving out the package name without `--depsOnly` can install the current project itself.

A missing import calls for comparing the exact module name, selected dependency version and compiler search context. Installing more similarly named packages does not diagnose an incompatible API. If compilation reaches a C compiler/linker error, Nimble dependency resolution may already have succeeded; inspect the subsequent build stage.

Lockfile and command features vary with the bundled Nimble version. Use the [official package guide](https://nim-lang.github.io/nimble/use-packages.html) with the installed help rather than assuming the latest development documentation matches the image. Preserve the resulting dependency selection for reproducible builds.
