---
name: javac
description: Compile a selected Java CLI source with a controlled output directory, dependency classpath and target release. Use when a walkthrough assumes an older JDK or compiler success is mistaken for runtime compatibility.
---

# Compile the selected source for its runtime

Read this entire SKILL.md before acting. Select the trusted compiler, reviewed source/dependencies and intended target runtime, then inspect errors and newly produced classes. Compilation does not run the application's main method or establish its operational result.

Define `javac_bin`, `source_file`, `classes_dir` (a fresh owned output directory) and `dependency_classpath` (existing reviewed dependencies). For a plain source not requiring annotation processing:

~~~bash
"$javac_bin" -version
"$javac_bin" -proc:none -d "$classes_dir" -cp "$dependency_classpath" "$source_file"
~~~

Use a dedicated empty dependency directory when there are no dependencies, rather than an unreviewed working directory. `-d` places classes under their package tree; run from that classpath root with the fully qualified class name. Do not mistake stale classes left from an earlier successful build for output from a failed one.

`-proc:none` disables annotation processors for this plain-source case. A project requiring generated code needs its reviewed processor configuration; do not silently use this command as its full build. Processors/plugins can execute during compilation even though main does not run.

When the intended runtime is older, an installed compiler supporting `--release N` can target that documented Java SE release. Compiler/runtime version matching and third-party dependency availability are separate. In particular, targeting an older release does not put removed JAXB classes into a modern runtime. Preserve the actual compiler diagnostics; missing `javax.xml.bind`, a public class/file-name mismatch and an unsupported release require different corrections.

See [compiler options and processing](https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html). Select the existing deployment's compatible build; compilation is not permission to install new dependencies.
