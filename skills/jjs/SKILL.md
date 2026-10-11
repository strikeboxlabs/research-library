---
name: jjs
description: Run a selected trusted legacy Nashorn JavaScript task and diagnose its engine, script arguments and Java class access. Use when a Java-backed script needs jjs rather than browser JavaScript or Node.js.
---

# Run the selected legacy script

Read this entire SKILL.md before acting. Require the trusted script/task and a verified ordinary-user jjs installation from the selected image. Nashorn/jjs was removed from JDK 15; a java executable alone does not establish availability. No conditional resources are required. Finish with the actual engine, requested script result and unresolved errors rather than treating an interpreter prompt as success.

Define `jjs_bin` as the verified executable invocation and inspect its `-h` and `-version` output. Account for the selected Java environment/classpath. An unfamiliar set-user-ID interpreter is a configuration finding to report, not the normal runner for this task.

For a reviewed local script, define `script` as its absolute path and `input` as the selected argument it expects:

~~~bash
"$jjs_bin" -doe "$script" -- "$input"
status=$?
~~~

`--` separates arguments available to the script's `arguments` object from interpreter options/script filenames. `-doe` expands errors to a stack trace. Multiple script files can execute in one invocation; select only the reviewed file. With no script file, jjs opens an interactive shell and waits for input.

For a selected interactive runtime check, start `"$jjs_bin"` and enter:

~~~javascript
var System = Java.type('java.lang.System');
println(System.getProperty('java.version'));
println(System.getProperty('java.home'));
quit();
~~~

These are observations about that JVM. They do not establish numeric OS identity or application success. `Java.type` resolves a fully qualified Java class; a missing class or incompatible classpath needs diagnosis rather than substituting a similarly named JavaScript object. Embedded engines can impose class-access policy that a standalone jjs does not share.

Nashorn's default language generation and Java APIs differ from Node.js/browser execution. A script can perform Java file/process operations under its actual process context; treat it as executable code. If a reviewed script starts a child and waits for it, inspect the child's returned status and requested artifact separately. A zero interpreter status or a printed process object is not proof that every child operation succeeded.

Report a missing legacy engine or runtime dependency as a capability gap. Do not silently download a replacement engine, change a privileged launcher or promote this task to another account.

References: [jjs command options](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jjs.html), [Nashorn Java interoperability](https://docs.oracle.com/javase/8/docs/technotes/guides/scripting/nashorn/api.html), [JDK 15 migration/removal](https://docs.oracle.com/en/java/javase/15/migrate/).
