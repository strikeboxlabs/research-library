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

For a [shaded JAR](https://maven.apache.org/plugins/maven-shade-plugin/), separate application resources from bundled dependencies. Retain the full `META-INF/maven/.../pom.xml` or `pom.properties` member name and its artifact coordinates: a dependency's parent POM is not the application's POM. For a SOAP service, follow the factory, configuration and annotations that select its data binding. [CXF defaults to JAXB and also supports Aegis](https://cxf.apache.org/docs/databindings.html); both libraries being present does not identify the active binding. A WSDL describes operations and schemas, but does not by itself prove which binding implementation produced them. Finish with the resolved configuration chain or the specific missing configuration, without launching the application or building the recovered project.

Reconstructed source may omit comments, original names or details and can fail for some classes. Keep exact member names and relevant bytecode/resource evidence when an interpretation depends on missing or ambiguous output. A static branch or class initializer is not proof it executed. A downloaded image tag, archive similarity or local runtime result does not establish an exact replica of a remote deployment.

For an export, retain the original archive separately and verify the selected exported classes and any failed/omitted members. Do not compile or run recovered code as a way to complete this static review. See the [upstream launch and file-opening instructions](https://github.com/java-decompiler/jd-gui).
