---
name: marshalsec
description: Select a marshalsec marshaller and generate a scoped Java unmarshalling fixture. Use when XML/JSON versus serialized bytes, local test execution, JNDI stages or runtime differences cause misleading results.
---

# Choose the actual unmarshalling format

Identify the consumer's marshalling library and reachable dependency versions from code/configuration. Castor XML, Jackson JSON and Java object serialization are distinct formats; one payload generator cannot be substituted solely because all use Java. Pin the marshalsec source/JAR and producer JDK; upstream documents Java 8 for its build/runtime. Skipping Maven tests builds an artifact without validating its behavior.

Define `jar` as the selected local all-dependencies JAR and `marshaller` as the exact class corresponding to the observed consumer, for example `Castor` only when Castor is established:

~~~bash
java -version
java -cp "$jar" "marshalsec.$marshaller"
~~~

Without a gadget, the marshaller lists its available choices; a usage exit need not mean incompatibility. Inspect that gadget's argument contract and additional classpath requirements. Do not select it from a name match alone.

For a selected JNDI-indirection gadget in the lab, define `gadget` as its listed identifier, `jndi_url` as the explicitly scoped controlled lookup endpoint, and `payload`/`log` as new output files:

~~~bash
java -cp "$jar" "marshalsec.$marshaller" "$gadget" "$jndi_url" > "$payload" 2> "$log"
~~~

Use this form only when the selected gadget accepts one JNDI URL; other gadgets have different argument counts/types. Check status and diagnostics. Preserve the generated format, encoding and namespaces; submitting XML as raw Java serialized bytes, or merging diagnostic text into it, changes the test.

**`-t` unmarshals the generated payload locally.** It is not a passive syntax check and may cause the very behavior under investigation on the authoring host. `-a` generates/tests all supported payloads for that marshaller and expands the operation beyond a selected fixture.

A JNDI lookup, an RMI/LDAP reference response, a subsequent class/resource fetch and execution are distinct stages. The consumer's JDK and trust settings govern later stages; a connection in listener logs alone establishes no more than contact. A marshalsec reference redirector, a ysoserial JRMP listener and a normal RMI registry serve different protocols/objects. Sending a serialized file through a raw TCP listener does not implement the required RMI exchange.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Atlas pp. 9–14. Sources: [upstream usage and prerequisites](https://github.com/mbechler/marshalsec), [marshaller/test implementation](https://github.com/mbechler/marshalsec/blob/master/src/main/java/marshalsec/MarshallerBase.java).
