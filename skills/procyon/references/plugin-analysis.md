# Follow a plugin's configuration into the method that uses it

Use this for a saved Bukkit/Spigot-style plugin or a small Java library whose connection settings affect another service. Preserve the original archive. Define `artifact` as that JAR, `decompiler_jar` as the trusted standalone tool, and all output paths as fresh files under the working directory. Review the member listing, duplicate names and size budget before reading or extracting members.

For a plugin with one ordinary root-level descriptor, define `descriptor` as a fresh output file:

~~~bash
unzip -p "$artifact" plugin.yml > "$descriptor"
~~~

Check UnZip's status and inspect the text as data. The descriptor's `main` class identifies a useful starting point; it does not prove that this copy was loaded or enabled on the live server. If the descriptor is absent, use the archive's actual application metadata instead of guessing the class name.

For one uniquely listed, regular `.class` member, define `member` as its exact archive name, `class_file` as a fresh output file, and `source_dir`/`errors` as fresh paths. UnZip still interprets wildcard characters inside a quoted member selector; confirm it selects exactly the intended member. Preserve package directories if you later need neighboring classes resolved.

~~~bash
unzip -p "$artifact" "$member" > "$class_file" &&
java -jar "$decompiler_jar" -o "$source_dir" "$class_file" 2> "$errors"
~~~

The isolated class is useful for a narrow question but can lack dependency/nested-type context. If reconstruction is incomplete, inspect the containing JAR and relevant dependencies, then compare raw bytecode for that same class. Define `bytecode` and `bytecode_errors` as fresh files:

~~~bash
java -jar "$decompiler_jar" -r "$class_file" > "$bytecode" 2> "$bytecode_errors"
~~~

Use the method signature, constants and call instructions to resolve a disputed operation. Raw output also requires successful class loading and interpretation; it does not automatically repair unsupported bytecode.

For an **illustrative** plugin method that constructs an RCON client for `127.0.0.1:27015`, issues a player-count command and writes the result to a web-directory file, follow the actual constructor and calls:

| Finding | Supported interpretation and next check |
|---|---|
| Method is `onEnable()` on a `JavaPlugin` subclass | It is a plugin-enable callback. Check descriptor and deployment evidence before attributing execution; static code does not establish that the plugin was enabled. |
| Constructor receives loopback, a port and password bytes | Those are this client connection's inputs in the server process's network namespace. They do not establish remote reachability, a listener bound to loopback only, or an OS-account password. Check the actual constructor signature when imports are unclear. |
| RCON result flows to a `PrintWriter` | Identify the target path and write/flush/close and exception paths. Code indicating a write is not proof of a completed disk update. |
| Path resembles a served web file | Website consumption is a hypothesis until its route/template or an observed response supports it. Likewise a literal password's continued validity or reuse is a separate question. |

Conclude with the class/method, the observed data flow and any missing runtime or reconstruction evidence. Keep sensitive literal values in the authorized evidence location, not general skill prose. See [JavaPlugin lifecycle](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/plugin/java/JavaPlugin.html) and [plugin descriptor fields](https://docs.papermc.io/paper/dev/plugin-yml/).
