# Resolve missing symbols for the exact build

Require the acquired executable/library and a candidate debug artifact from the same build. A release banner or similarly named libc file is insufficient. Retain module/build identity and GDB's actual loading diagnostics before attributing names to addresses.

GDB can select separate symbols through a `.gnu_debuglink` filename with validated CRC, or a matching build ID. Search locations include adjacent/.debug files and the configured global debug directories; build-ID layout uses `.build-id/first-two-hex/rest.debug`. Copying an arbitrary .debug file to a familiar basename does not establish either match.

For an offline task, disable automatic downloads before loading artifacts when installed GDB supports it:

~~~text
set debuginfod enabled off
show debug-file-directory
~~~

Set `debug-file-directory` deliberately to the actual owned debug directory if required, then inspect loaded file/shared-library information and symbol diagnostics. A missing supported option is a version gap; do not silently enable network retrieval to fix it. Existing startup/automatic script-loading restrictions still apply.

Distinguish ELF runtime-library selection (RPATH/RUNPATH and loaded mappings) from GDB's debug-file search. Match the actual loaded module, not merely a nearby library. If symbols match but `list` fails, obtain corresponding source/path mapping; missing source is a separate problem. Finish with verified matching symbols or the unresolved identifier/path mismatch.

See [GDB separate debug files](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Separate-Debug-Files.html).
