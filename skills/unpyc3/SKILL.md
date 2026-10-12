---
name: unpyc3
description: Recover partial Python source from selected bytecode using the greyblue9 unpyc37-3.10 fork. Use when unsupported opcodes, interpreter mismatches or placeholder functions make a decompilation misleading.
---

# Interpret a partial bytecode decompilation

Read this entire SKILL.md before acting. Require an owned selected `.pyc`, its established Python major/minor and a trusted installed greyblue9 unpyc37-3.10 environment. All instructions are inline. Finish with retained output and diagnostics plus the supported recovered portions; an incomplete function remains unresolved.

This package refers to the greyblue9 fork, not every tool named unpyc3. Its documented coverage is strongest for Python 3.7, with progressively weaker 3.8/3.9 support and minimal 3.10 support. Do not infer support for later bytecode. A missing compatible interpreter or module is a specific prerequisite gap rather than permission to execute the acquired application.

Define `python_bin` as the trusted compatible interpreter and `bytecode` as the selected absolute `.pyc`. Use a fresh owned directory and trusted module search path, then capture both streams:

~~~bash
"$python_bin" -m unpyc.unpyc3 "$bytecode" >recovered.py 2>decompile.stderr
status=$?
~~~

The module invocation is the current project's documented CLI. A historical `src/unpyc3.py` command is revision dependent: a compatibility import wrapper need not invoke the same main function. Identify the actual fork/revision rather than copying its old pathname blindly.

Inspect `recovered.py` as text and preserve stderr/status. A wrong-magic warning is a compatibility failure to resolve before interpreting recovered code. The parser reads marshalled code objects; it does not need to run the target module. Parsing acquired binary data still belongs in the disposable analysis environment.

The implementation can catch a decompilation exception, print it, then display the partial suite without returning a failing process status. For example, an unsupported `GEN_START` opcode can leave readable imports/constants followed by `pass` where a function could not be reconstructed. That `pass` does not establish that the original function was empty. Syntax-valid output is also not proof of behavioral equivalence.

Use trustworthy recovered literals/imports as bounded leads and corroborate decisions with independent application/source evidence. If the selected function fails, retain its name and exact diagnostic and choose a compatible analysis tool when available. Do not fill in missing control flow or call partial output the original source.

References: [fork, coverage and CLI](https://github.com/greyblue9/unpyc37-3.10), [reader and partial-output implementation](https://github.com/greyblue9/unpyc37-3.10/blob/master/src/unpyc/unpyc3.py).
