---
name: dstat
description: List available plugins in a selected classic Python Dstat installation. Use when a plugin name or search-directory listing is mistaken for successful loading or resource collection.
---

# Establish the available plugin names

Read this entire SKILL.md before acting. Require a trusted identified classic Dstat executable and its supported interpreter. This branch lists plugins; it does not install, initialize or run a selected external plugin. Finish with implementation/version, names and listing errors, keeping runtime readiness unresolved.

Define `dstat_bin` as the installed trusted executable and `report` as a fresh private output file:

~~~bash
"$dstat_bin" --version
"$dstat_bin" --list >"$report"
~~~

Check both statuses and retain diagnostics. Read all groups: internal names and external directories are distinct. The reviewed classic implementation discovers external Python filenames without importing those plugins in the list branch. A listed name therefore does not prove dependency compatibility, initialization or usable measurements. Confirm that contract for the installed implementation before relying on it; PCP's dstat and later forks can differ.

Directory visibility depends on the caller and its environment. A missing group/name can reflect its search path or permissions rather than absence everywhere. Duplicate names can occur across directories; establish the actual selected origin before any separately authorized collection. Review executable/plugin-directory trust and avoid elevation merely to list names. Interpreter deprecation or import errors require the matching package/runtime contract; suppressing a warning is not a compatibility fix.

See the [classic implementation](https://github.com/dstat-real/dstat/blob/master/dstat) and [project lineage](https://github.com/dstat-real/dstat).
