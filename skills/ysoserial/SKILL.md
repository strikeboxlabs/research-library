---
name: ysoserial
description: Select and generate Java serialization fixtures with ysoserial for an authorized lab test. Use when gadget dependencies, producer JDK failures, binary corruption or callback evidence need interpretation.
---

# Match the generator to the observed consumer

Establish that the application actually consumes Java object serialization and identify the reachable dependency/JDK versions. A library on disk alone does not establish a usable gadget chain or an unsafe deserialization entry point. XML unmarshalling and native Java serialization require different generators even when both involve Java.

Define `jar` as the pinned local ysoserial all-dependencies JAR. Record its checksum and the **producer** JDK separately from the consumer runtime:

~~~bash
java -version
sha256sum -- "$jar"
java -jar "$jar"
~~~

The no-argument call prints the available payloads/dependencies and exits nonzero for usage. That is distinct from a failed generation. Select a gadget whose documented conditions match the observed consumer. Historical JDK restrictions matter; for example, a producer reflection/module error occurs locally and says nothing about whether a request reached the target. Prefer a dedicated compatible runtime over changing the workstation's default Java or the target's security settings.

Define `gadget` from the installed list, `argument` according to that gadget's documented contract and the selected lab probe, and `payload`/`log` as new output files:

~~~bash
java -jar "$jar" "$gadget" "$argument" > "$payload" 2> "$log"
~~~

Check the exit status and diagnostic file before using the output. Native Java serialization is binary; keep stdout separate from stderr and never call text `.strip()`, decode it as UTF-8 or store it in a shell variable. A nonempty/truncated file after failure is not a valid fixture.

Gadgets do not all accept shell command lines. Chains calling `Runtime.exec(String)` do not automatically interpret pipes, redirection or `&&` as a shell would. Match the actual gadget argument semantics rather than building progressively more complex quoting around a wrong assumption.

Artifact generation, application transport/wrapping, deserialization and an observed effect are separate stages. A valid serialized stream may still require an application-specific envelope/signature. DNS/RMI contact proves a lookup/connection, not arbitrary execution; correlate the intended harmless probe with the actual observation. Do not deserialize the generated artifact locally merely to check its syntax.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Arkham pp. 7–12; Atlas pp. 11–14. Sources: [upstream usage](https://github.com/frohoff/ysoserial), [generator](https://github.com/frohoff/ysoserial/blob/master/src/main/java/ysoserial/GeneratePayload.java), [CommonsCollections5 conditions](https://github.com/frohoff/ysoserial/blob/master/src/main/java/ysoserial/payloads/CommonsCollections5.java).
