---
name: java
description: Run an existing Java command-line program with an explicit runtime, classpath and arguments. Diagnose launcher, missing-class and runtime-version failures before interpreting the application's output.
---

# Select the runtime and entry class

Read this entire SKILL.md before acting. Establish the reviewed program's entry class or executable JAR, required dependencies and intended file effects. Finish with the exit status and actual application result; class loading alone does not prove the task succeeded.

Define `java_bin` as the selected runtime, `classpath` as its existing classes/dependencies, `main_class` as the fully qualified entry class and `input_file` as the intended application argument:

~~~bash
"$java_bin" -version
"$java_bin" -cp "$classpath" "$main_class" "$input_file"
~~~

Pass the class name without `.class`. On Linux the classpath uses colons; a directory entry is the package-tree root. Explicit `-cp` prevents an unrelated working directory/CLASSPATH from selecting the program. Arguments after the entry class belong to the application; options before it belong to Java. Review inherited launcher/agent options such as `JDK_JAVA_OPTIONS` and `JAVA_TOOL_OPTIONS` when selecting a trusted execution context.

For an executable JAR, use `"$java_bin" -jar "$jar" "$input_file"` instead. Its manifest entry and dependency handling differ; `-jar` does not combine an ordinary `-cp` override as if it were class mode. Source-file launch on newer JDKs is another mode, not a substitute for the historical compiled-class invocation.

`ClassNotFoundException`/a missing main class points to names, packaging or classpath. `NoClassDefFoundError` can identify an absent dependency after the main class was found. `UnsupportedClassVersionError` means the runtime cannot load that bytecode version. Inspect the actual error/cause; neither recompiling blindly nor a zero exit proves the requested output was produced. A modern runtime does not contain every legacy API: JAXB's removal in JDK 11 can break programs using `javax.xml.bind` even when the compiler accepted a compatibility target.

See [launcher modes/options](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html) and [removed runtime APIs](https://docs.oracle.com/en/java/javase/21/migrate/removed-tools-and-components.html).
