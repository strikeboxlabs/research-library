---
name: pyinstaller
description: Package a reviewed owned Python application and interpret build artifacts. Use when spec generation, platform dependence or collected resources are confused with a completed runnable build.
---

# Build the selected owned Python application

Read this entire SKILL.md before acting. Require reviewed application/dependency inputs, an installed PyInstaller environment and fresh owned build/output directories. Build as the ordinary owning user on the intended platform. For an existing spec or added application resources, read [spec files and resources](references/spec-files.md) fully before building. Finish with the selected artifact, build diagnostics and any actual launch result; spec creation alone is incomplete.

Define `entry_script` as the reviewed absolute Python entry point, `product_name` as the approved simple output name and `build_directory`, `output_directory`, `spec_directory` as distinct fresh owned directories outside the input tree. Inspect the installed version/help before adapting options:

~~~bash
pyinstaller --version
pyinstaller --help
pyinstaller --name "$product_name" --workpath "$build_directory" --distpath "$output_directory" --specpath "$spec_directory" "$entry_script"
status=$?
~~~

The default is a directory bundle; `--onefile` selects a single executable. Neither mode makes Python inputs or build hooks passive data. Use trusted source, hooks, spec and dependency search paths. Avoid combining this task with privileged wrappers or acquiring unrelated files as resources.

Retain the status and relevant build log. A generated `.spec` can remain after a failed build. Confirm the actual output and expected bundle mode before declaring packaging complete. A COLLECT completion applies to directory collection; a one-file spec can omit that stage. Do not reconcile mismatching excerpts by assuming the shown spec produced the shown log.

PyInstaller builds for its running OS/environment; a Linux bundle is not a Windows executable simply because an output suffix changes. A completed artifact still needs an ordinary-user launch check in the intended environment before claiming it works. Record missing runtime libraries or unavailable GUI/display requirements as gaps.

Reference: [official invocation and platform behavior](https://pyinstaller.org/en/stable/usage.html).
