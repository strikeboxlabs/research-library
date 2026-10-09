---
name: jdb
description: Attach the Java command-line debugger to an existing JDWP endpoint, reach a relevant breakpoint and inspect suspended threads. Use when deferred breakpoints, missing locals or expression side effects cause confusion.
---

# jdb attached JVM inspection

Use the JDK's `jdb`, not a native debugger for Java stacks. Record `jdb -version` and inspect `jdb -listconnectors`. Define `jdwp_host` and `jdwp_port` as the existing authorized JDWP endpoint, often a local forwarded port:

~~~bash
jdb -attach "$jdwp_host:$jdwp_port"
~~~

Passing a main class instead launches a different debugging workflow. Do not enable a new public JDWP listener as an attachment repair: this interface controls the JVM, and a reachable port is not an authentication boundary. Confirm which process/environment the forward reaches.

At the **jdb prompt**, use `classes` and `methods package.Class` to identify the actual application method. Set `stop in package.Class.method` or `stop at package.Class:line`; use the full signature for an overloaded method. These are placeholders to replace with observed symbols. A deferred breakpoint means its class has not loaded, not that execution has stopped. An initialization method may never run again in a long-lived application; choose a repeatable request handler and trigger only the intended action.

Once stopped:

~~~text
threads
thread <observed-thread-id>
where
locals
~~~

Select the relevant frame with `up`/`down`; `locals` depends on debug information and a suspended frame. `list` needs matching source files/sourcepath, while absent source does not necessarily prevent a stack trace. `next`, `step` and `cont` resume execution differently; consider the application's other suspended threads and request timeouts.

`print`/`eval` evaluate expressions: method calls can execute application code, modify state or block. Prefer fields/simple values for inspection and treat method invocation as a separate action, never as passive data retrieval.

Use `clear` with the breakpoint's original location, then `cont` when resumption is intended. `quit` disposes an attached debugger connection; a JVM launched by the debugger has different process ownership. Confirm the application's state after detachment. Retain the method/frame, observed values, symbol limitations and any execution you triggered.

Documentation reviewed 2026-10-09; Linux execution untested. Case: AI pp. 10–11. Sources: [jdb manual](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jdb.html), [commands](https://github.com/openjdk/jdk/blob/master/src/jdk.jdi/share/classes/com/sun/tools/example/debug/tty/TTYResources.java), [JDI disposal](https://docs.oracle.com/en/java/javase/25/docs/api/jdk.jdi/com/sun/jdi/VirtualMachine.html#dispose()).
