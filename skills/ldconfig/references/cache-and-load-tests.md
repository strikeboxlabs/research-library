# Cache selection and controlled library loading

Use for an unexpected dependency path or an authorized test of a configured writable library directory. Required inputs are the actual executable, its architecture/direct dependency name, loader/configuration, available update authority and a restorable test scope. A setuid bit on ldconfig is an unusual authority condition, not a normal installation assumption.

## Establish which mechanism selects the library

For `binary` as the observed ELF path:

~~~bash
readelf -W -h -l -d "$binary"
readelf -W --dyn-syms "$binary"
"$ldconfig_bin" -p
"$ldconfig_bin" -v -N -X
~~~

A NEEDED string with a slash is a path. For bare names, glibc considers RPATH when RUNPATH is absent, non-secure LD_LIBRARY_PATH, RUNPATH, cache and defaults, with important per-object and hardware-capability differences. Configuration file order alone therefore does not predict every load. Secure execution suppresses environment search paths; it does not make a misconfigured cache trustworthy.

Inspect ownership/mode and parent traversal for the candidate directory, executable and update program. `nosuid`, ptracing and other execution restrictions can suppress a setuid effect. A successful ordinary-user trace or debugger session is separate from the normal privileged launch. A symbol named `seclogin` does not mean the library is first loaded at that call: dependencies/initializers may load before main and function binding can be lazy.

## Exercise the selected load, with a bounded observable effect

On the approved test host, select **one** otherwise unused library filename matching the target's observed NEEDED/SONAME and ABI, in an already reviewed configured directory. Preserve the original mapping/configuration and identify concurrent package changes before refreshing. Stop if the destination exists or that name could affect unrelated programs without an agreed test boundary. Do not add `/tmp` globally or overwrite a production library to make the example work.

An **illustrative** diagnostic replacement for a verified `int seclogin(void)` interface is:

~~~c
#include <stdio.h>
#include <unistd.h>

int seclogin(void) {
    printf("library-probe ruid=%lu euid=%lu\n",
           (unsigned long)getuid(), (unsigned long)geteuid());
    return 0;
}
~~~

Adapt the prototype and return contract to the observed implementation, rather than assuming them from a symbol name. Define `source` as that reviewed marker source, `built_library` as a fresh build output, `soname` as the observed bare dependency name, and `test_library` as the fresh exact destination in the selected directory:

~~~bash
gcc -Wall -Wextra -shared -fPIC -Wl,-soname,"$soname" "$source" -o "$built_library"
readelf -W -h -d --dyn-syms "$built_library"
test ! -e "$test_library" && test ! -L "$test_library" && cp -n -- "$built_library" "$test_library"
~~~

Check each result before advancing, including that the destination contains the intended artifact. Build success does not prove symbol/architecture compatibility. The shell existence check is not an atomic protection against concurrent changes; use an isolated test directory/host rather than an uncontrolled writable shared location. Review dependencies introduced by the marker too.

Using the established cache-update authority, run the verified ldconfig invocation with `-X` to rebuild the system cache without changing links:

~~~bash
"$ldconfig_bin" -X
"$ldconfig_bin" -p
~~~

The update is global even though the inserted artifact is narrow. If authority is supplied by an approved wrapper or sudo rule, use that exact granted invocation; a permission error is a missing authority, not a reason to change permissions. A private cache generated with `-C` does not automatically become the normal process's system cache.

Confirm the selected cached/resolved path for the trusted test executable. Then run the intended normal `"$binary"` launch and supply only its selected required input. This executes the program and diagnostic function. Capture the marker at the observed call: differing real/effective UIDs demonstrate that function's execution context at that time. Equal UIDs or no marker leave the privilege/call hypothesis unproved; consider launch policy, selected path, ABI, early errors and whether the branch was reached. Do not use a GDB launch as the privileged confirmation.

The marker proves code ran in the caller's context without changing UID or starting a shell. A successful dependency trace alone cannot prove this. Report cache update, resolved path, function execution and identity separately.

After the controlled test, remove only the exact artifact created for it, once its identity/ownership is rechecked, and rebuild the cache with the same approved invocation. If links/configuration were also changed by a separately approved procedure, restore those specific changes. Recheck the original mapping and functional behavior; do not blindly copy an old global cache over concurrent legitimate updates. Record unresolved restoration explicitly.

Consult [glibc loader semantics](https://manpages.debian.org/bookworm/manpages/ld.so.8.en.html), [execve privilege conditions](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/execve.2) and [GCC shared-library linking](https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html).
