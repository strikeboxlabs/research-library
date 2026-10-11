---
name: recaf
description: Open an acquired Java archive in Recaf for static class and method inspection. Use when a configuration source, call path or decompiler failure needs evidence from the archive without running its application entrypoint.
---

# Inspect the selected Java archive

Read this entire SKILL.md before acting. Require an acquired archive, trusted installed Recaf distribution, its compatible Java runtime and a graphical session. All steps are inline. Finish with the archive identity, selected class/method, observed code path and decompilation limits; a loaded workspace alone is incomplete.

Define `java_bin` as the selected runtime, `recaf_jar` as an existing independent Recaf distribution matching Linux/CPU architecture, and `input_jar` as the absolute acquired archive path. Keep the original bytes and fingerprint. For the documented independent Recaf 4 build, Java 22+ is required:

~~~bash
"$java_bin" -version
"$java_bin" -jar "$recaf_jar" --help
"$java_bin" -jar "$recaf_jar" --version
"$java_bin" -jar "$recaf_jar" --input "$input_jar"
~~~

The JAR passed to Java is Recaf; the input argument is the artifact to inspect. These commands do not ask Java to run the acquired application's main class. Launcher JARs and older Recaf releases have different contracts; confirm the installed artifact before reusing its switches. Do not invoke an updater merely to inspect one file. Missing JavaFX/display support or an unsupported runtime leaves the graphical task unavailable.

In the loaded workspace, locate the application package and selected class, then inspect the relevant method and callers rather than treating a string match as the whole behavior. Distinguish constructor/field initialization from per-request logic. An environment-variable read establishes a configuration dependency, not its current value or whether the deployed process loaded this archive. Dependency packages in a fat JAR do not prove every bundled feature is reached.

Record the fully qualified class and method with a focused code extract or screenshot. Decompiled source is a reconstruction; when names, exceptions or control flow look inconsistent, inspect the bytecode view and retain the parse/decompiler diagnostic. Missing classes or failed methods leave those branches unreviewed. A matching filename at another path does not prove byte identity with the deployed copy.

Keep this inspection read-only: close the workspace after recording findings. Editing/exporting, running startup scripts or attaching to a live JVM are separate tasks with different effects and prerequisites.

References: [release artifact/runtime contract](https://github.com/Col-E/Recaf/releases), [installed input/options contract](https://recaf.coley.software/dev/arch/running.html).
