---
name: "angr"
description: "Solve binary-reachability and input-constraint problems with the angr symbolic execution engine: find inputs reaching a target address, or recover required constraints. Use when manual disassembly analysis needs automated path solving."
---

# angr symbolic execution

Installed invocation: `/opt/tools/angr/.venv/bin/python` (dedicated venv at /opt/tools/angr; angr 10.0.5 with the unicorn engine enabled).

Read this entire SKILL.md before acting. Require the acquired binary and a concrete goal (target address, constraint question) before writing the script. Finish with the solved inputs or the bound of the search attempted.

~~~python
import angr
proj = angr.Project("/path/to/binary", auto_load_libs=False)
state = proj.factory.entry_state()
sm = proj.factory.simulation_manager(state)
sm.explore(find=0xTARGET, avoid=0xBAD)
if sm.found:
    print(sm.found[0].posix.dumps(0))
~~~

Run scripts with `/opt/tools/angr/.venv/bin/python`, not the system interpreter — angr is a library and this venv isolates it. The core pattern is explore(find, avoid): success depends on choosing avoid addresses that prune the state explosion, and `auto_load_libs=False` keeps symbolic execution out of libc. For large binaries, constrain the entry state (fixed argv length, known prefix) before exploring; unconstrained symbolic buffers blow up the state count faster than any other mistake.

angr answers reachability and constraint questions; it does not replace disassembly (ghidra, radare2 skills identify the target addresses angr should seek). A timed-out explore is a bounded search, not proof of unreachability.

References: [project documentation](https://docs.angr.io).
