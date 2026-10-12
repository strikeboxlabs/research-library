---
name: r2
description: Inspect static strings and their file and virtual addresses in a selected owned binary with radare2. Use when plain string text lacks section/address context or the two address spaces are being confused.
---

# Static radare2 string metadata

Read this entire SKILL.md before acting. Require a bounded binary identified as an executable object, a trusted r2 launch environment and a fresh report path; do not open a project file as the input. Finish with parser status, selected string metadata and address-space limits. This task reads the object without executing or modifying it.

Define `binary` as the absolute acquired object path and `strings_report` as a nonexistent file in a private working directory. Record the input size/hash. Check `r2 -v` and `r2 -h`; use a trusted launch environment without an inherited `R2_ARGS` override, since it can replace command-line arguments.

~~~bash
(umask 077; set -C; r2 -NN -q -c 'izj' "$binary" > "$strings_report")
~~~

`-NN` suppresses user settings and automatic plugins; `-q` exits after the fixed command. `izj` reports strings in data sections as JSON; plain `iz` gives the corresponding table. Do not interpolate acquired strings into r2 commands. Retain stderr and status, then inspect the actual report rather than interpreting an empty file as successful analysis. Check `iz?` for the installed generation if a command/field is rejected.

Associate each selected string with its section, encoding, length and `paddr`/`vaddr`. `paddr` identifies its physical/file location in this object; `vaddr` describes the loader's virtual-address model. Equal values in one section do not make them interchangeable elsewhere. A displayed virtual address is not the current runtime load address of a PIE process. String size can include encoding/terminator bytes and differ from character length. A string match is neither a symbol identity nor proof that executed code consumes it.

If the selected bytes are missing, `iz`'s section scope can explain the gap; identify the object's sections/encoding and the exact requested bytes before expanding inspection. Parser failure or missing mapping remains unresolved. Complete with the supported string/address evidence, not an exploitability or execution claim.

See [launch options](https://github.com/radareorg/radare2/blob/master/man/radare2.1) and [string-command help](https://github.com/radareorg/radare2/blob/master/libr/core/cmd_info.inc.c).
