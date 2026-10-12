---
name: prusaslicer
description: Establish the installed PrusaSlicer command-line interface and diagnose missing GUI/display versus CLI capability without loading a project. Use before choosing a trusted model-processing task on Linux.
---

# Establish the selected CLI

Read this entire SKILL.md before acting. Require the trusted installed Linux executable and ordinary user context. This task discovers the interface without loading or slicing a project; no conditional resources are required. Finish with observed build/help, status and supported next task or missing runtime prerequisite.

Set `prusaslicer_bin` to the selected absolute executable path:

~~~bash
"$prusaslicer_bin" --help
help_status=$?
~~~

Preserve diagnostics and the actual build string/actions. A filename, transferred executable or executable mode does not establish trusted provenance or library compatibility. Use this build's help before choosing options; PrusaSlicer differs from upstream Slic3r, including `--help-fff` and `--help-sla` for technology-specific settings.

An ordinary launch can request the GUI. A missing DISPLAY message therefore does not establish that command-line model operations are unavailable. Do not manufacture a display value or elevate privileges to repair the interface. Distinguish missing shared libraries, unsupported options and display initialization from a project parsing error.

Model processing is a separate task requiring reviewed input/profile and output effects. AMF/3MF projects can import profiles; post-processing settings can execute external scripts during G-code export. Loading an untrusted project or running a privileged export is unsuitable as an interface probe. A help result does not validate a model, produce G-code or establish that later slicing completed.

References: [Prusa CLI differences](https://github.com/prusa3d/PrusaSlicer/wiki/Command-Line-Interface/7cc20b4b1b317f0a16bde1858769da0620392036), [upstream CLI help](https://manual.slic3r.org/advanced/command-line), [post-processing effects](https://help.prusa3d.com/article/post-processing-scripts_283913).
