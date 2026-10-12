# Correlate a loaded module's symbols

For an existing approved remote debug target, require its matching kernel ELF, the exact loaded module's local symbol file and observed current section addresses. This procedure adds debugger symbols; it neither inserts the module into the kernel nor establishes that its code ran.

At the selected guest/target, acquire the module's actual readable section metadata. Define `module_name` as the exact observed loaded name:

~~~bash
cat "/sys/module/$module_name/sections/.text"
cat "/sys/module/$module_name/sections/.data"
cat "/sys/module/$module_name/sections/.bss"
~~~

Inspect each status. Missing or restricted metadata is a prerequisite gap; zeros or addresses from another load are not substitutes. Section presence/layout can differ by build. Retain the target boot and module load context alongside the section values.

In the stopped GDB session, substitute the matching local symbol path and those actual numeric addresses:

~~~text
add-symbol-file /absolute/path/approved-module.ko TEXT_ADDRESS -s .data DATA_ADDRESS -s .bss BSS_ADDRESS
info files
info functions selected_function
disassemble /r selected_function
~~~

The path/address words above are placeholders. Supply every additional section needed for the selected symbols. An omitted section uses the file's default address; one base for .text does not necessarily relocate every module section correctly. Compare the selected symbol's current address and instruction bytes with the stopped target before using it as diagnostic evidence.

Module unload/reload or another boot invalidates the address record. Remove/reload stale symbols deliberately with remove-symbol-file; do not apply a historical writeup's constants. A symbol-table acknowledgment proves the debugger read symbols, not a build match, a module load or root cause. Keep unresolved relocation or unavailable debug information explicit.

See [GDB symbol-file commands](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Files.html).
