---
name: avalonia-ilspy
description: Inspect selected managed .NET assemblies in the existing Avalonia ILSpy Linux GUI. Use to navigate types and helper calls while retaining assembly identity and unresolved reference warnings.
---

# Inspect an assembly in the Linux GUI

Read this entire SKILL.md before acting. Require a trusted installed launcher matching the Linux architecture, a graphical session and the selected preserved assembly with matching dependencies when needed. No conditional resources are required. Finish with the assembly digest, selected type/member, reconstructed evidence and unresolved warnings.

Define `ilspy_bin` as the installation's actual launcher and `assembly` as the absolute working-copy path. Launch as the ordinary user:

~~~bash
"$ilspy_bin"
~~~

Use File > Open to load `assembly`, expand its namespaces/types and select the member relevant to the question. Follow linked helper types or use Search/Analyze to inspect references, keeping the declaring assembly with every selected member. Opening an assembly does not run its entrypoint. Do not build or launch reconstructed projects during this inspection.

Record the displayed assembly identity, target framework/runtime metadata and resolution warnings separately. A PE32 managed container can describe an AnyCPU assembly; it alone does not establish a required 32-bit process. A missing dependency warning can leave an incomplete getter/setter reconstruction even when navigation works. Supply matching acquired references or retain that limitation; arbitrary substitute DLLs do not establish the original behavior.

For credential or byte-transform helpers, retain only redacted call/encoding semantics. Assignment between byte-array variables aliases the object; reconstruction is not proof of a copied array, a valid credential or a successful service connection. Close the owned window after saving the selected private finding.

Avalonia ILSpy is a distinct desktop frontend, with its own release/runtime contract; ILSpyCmd CLI flags are not GUI launcher flags. Its [upstream repository](https://github.com/icsharpcode/AvaloniaILSpy) is archived and unmaintained. Use this for an existing selected installation and consult its matching release instructions when an architecture/runtime problem prevents launch.
