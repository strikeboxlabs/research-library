---
name: ropgadget
description: Inspect instruction-sequence candidates with ROPgadget in local binary-analysis fixtures. Use when architecture, search depth, address filtering or hidden register effects make gadget listings misleading.
---

# Treat gadget output as candidates

Confirm the `ROPgadget` executable and its `--help`; package names and command capitalization differ. Use the exact binary build under analysis. Establish its format, architecture, bitness and byte order before selecting decoder options. A Linux-hosted analysis tool can inspect a foreign binary without making that binary runnable on Linux.

Define `binary` as the existing artifact, and `report` as a fresh local output file:

~~~bash
ROPgadget --binary "$binary" --depth 10 > "$report"
~~~

`--depth` is a search depth in **bytes**, not a count of instructions. Check diagnostics and the actual architecture before interpreting an empty result. Keep the full relevant sequence; a grep match on one mnemonic can conceal the instructions around it.

For a deliberately restricted x86 search, define `address_range` from the observed executable mapping in the tool's `start-end` hexadecimal syntax:

~~~bash
ROPgadget --binary "$binary" --range "$address_range" --only 'pop|ret'
~~~

This filter can hide useful sequences containing other instructions. `--badbytes` filters gadget **addresses**; it does not certify every byte of a future input. `--offset` adjusts reported addresses and does not measure or disable ASLR. Resolve runtime load bias from the actual process before comparing a listed address with debugger memory.

For each candidate, inspect all operand widths, memory accesses, stack changes, flags and register clobbers. In Attended, a sequence containing `not al` also performed `adc cl,...`; another shifted `eax`, not just `al`. A scalar floating-point conversion is not a bitwise copy, and an adjacent `mov` may destroy a register that matters later. Those differences change whether the sequence meets the intended constraint.

Cross-check the exact bytes and complete sequence with a disassembler. On variable-length architectures, decoding from a different byte boundary can produce a different instruction stream. A listing alone proves neither that a process reaches the sequence nor that mitigations and runtime state permit the proposed behavior. Verify selected candidates in the matching controlled debugger fixture before making execution claims.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Attended pp. 22–25, adapted from OpenBSD. Sources: [ROPgadget usage](https://github.com/JonathanSalwan/ROPgadget), [argument definitions](https://github.com/JonathanSalwan/ROPgadget/blob/master/ropgadget/args.py).
