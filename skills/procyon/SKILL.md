---
name: procyon
description: Inspect Java JARs and class files offline with Procyon, recover readable methods and distinguish missing classes or decompiler failures from absent behavior. Use for plugin configuration and code-flow questions without launching the application.
---

# Recover Java behavior from a saved artifact

Read this entire SKILL.md before acting; reuse complete current context. Use an existing trusted Procyon installation and a preserved input copy. Check the archive and required classes, then inspect generated code and diagnostics. For plugin entrypoints, embedded connection settings or a selected-class investigation, read [plugin analysis](references/plugin-analysis.md) fully. Finish with class/method evidence and reconstruction limits; generated files alone do not establish complete coverage.

Define `decompiler_jar` as the existing trusted **standalone Procyon decompiler JAR**, `artifact` as the acquired application JAR, and `source_dir`, `log`, `errors` as fresh working paths. A similarly named library JAR need not contain the CLI or its dependencies. Check the installed build's help and Java compatibility:

~~~bash
java -jar "$decompiler_jar" --help
~~~

The first `-jar` belongs to the Java launcher and selects the trusted tool. Never substitute the acquired application there. Procyon accepts an input JAR as a positional argument; its older `-jar input.jar` option is deprecated in current upstream source. Do not mistake those two option layers.

Before expanding the input, inspect member names and compressed/uncompressed sizes; then test the bounded archive:

~~~bash
unzip -Z -l "$artifact"
unzip -t "$artifact"
~~~

CRC errors or truncated input require a fresh acquisition or a clearly limited recovery. After a clean container check and with a suitable output budget:

~~~bash
java -jar "$decompiler_jar" -o "$source_dir" "$artifact" > "$log" 2> "$errors"
~~~

Read stderr and inspect the relevant generated methods. The driver can report individual type failures and continue, so a zero exit status or one `.java` file does not establish complete decompilation. Nested types may be included inside their enclosing output; generated file counts need not equal `.class` member counts. Java output is reconstructed code: missing dependencies, compiler transformations and unsupported bytecode can obscure the original behavior. Do not infer an absent operation from a failed or omitted method.

Use [upstream CLI options](https://github.com/mstrobel/procyon/blob/master/Procyon.Decompiler/src/main/java/com/strobel/decompiler/CommandLineOptions.java) and the [decompiler guide](https://github.com/mstrobel/procyon/wiki/Java-Decompiler) for installed-build differences. If Procyon is unavailable, record that gap or select another already installed Java decompiler; installation and artifact execution are separate tasks.
