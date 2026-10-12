---
name: jd-gui
description: Launch an existing JD-GUI to inspect reconstructed Java classes in a selected archive. Use for static method, field and dependency review when an interactive Linux graphical session is available.
---

# Inspect the selected Java archive

Read this entire SKILL.md before acting. Require a trusted installed JD-GUI, its compatible Java runtime, an available graphical session and a preserved input copy. No conditional resources are required. Finish with the archive identity, exact member/class/method reviewed and reconstruction gaps; opening a class does not establish deployed behavior.

JD-GUI is a graphical decompiler, not a headless batch CLI. A distribution may provide a `jd-gui` launcher, but do not assume its path or install it during inspection. The upstream Java launcher works with the existing trusted tool archive. Define `java_bin` as that runtime and `jd_gui_jar` as JD-GUI itself:

~~~bash
"$java_bin" -version
"$java_bin" -jar "$jd_gui_jar"
~~~

In JD-GUI use **File > Open File** to select the acquired application archive or class. The archive supplied to Open File is data; do not substitute it for the tool JAR in the launch command. With no graphical session or a rejected format, record the gap and use an available static archive/bytecode reader for the selected members. Do not report a successful GUI review from a launcher exit alone.

For a WAR, distinguish application classes under `WEB-INF/classes`, dependency archives under `WEB-INF/lib`, deployment descriptors and resources. Trace the selected method's callers, inputs, checks and configured defaults in the preserved copy. Record whether a value comes from an argument, a configuration lookup, a default or another call; a named field alone does not establish its effective value. A library filename can suggest a version but does not establish which code a running service loaded.

Reconstructed source may omit comments, original names or details and can fail for some classes. Keep exact member names and relevant bytecode/resource evidence when an interpretation depends on missing or ambiguous output. A static branch or class initializer is not proof it executed. A downloaded image tag, archive similarity or local runtime result does not establish an exact replica of a remote deployment.

For an export, retain the original archive separately and verify the selected exported classes and any failed/omitted members. Do not compile or run recovered code as a way to complete this static review. See the [upstream launch and file-opening instructions](https://github.com/java-decompiler/jd-gui).
