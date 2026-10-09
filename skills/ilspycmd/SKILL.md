---
name: ilspycmd
description: Inspect managed .NET assemblies from Linux with ILSpyCmd. Use to locate types, trace properties and serialization paths, or recover readable code without launching the inspected application.
---

# Decompile the selected evidence

Use ILSpy's `ilspycmd` CLI, whose flags differ from the desktop frontend. Check `ilspycmd --version` and `--help`; the tool's own required .NET runtime can differ from the target assembly's framework. A missing tool runtime is not evidence that the captured assembly is invalid. This is the Linux CLI alternative to Bagel's dnSpy inspection.

Define `assembly` as an absolute path to a preserved working copy. List class names first; then set `type_name` to an observed fully qualified name and `source` to a fresh private output file:

~~~bash
ilspycmd --disable-updatecheck -l c "$assembly"
ilspycmd --disable-updatecheck -t "$type_name" "$assembly" > "$source"
~~~

Check the installed support for `--disable-updatecheck` when avoiding the optional update request. `-l c` lists classes; it does not decompile them. Check status, stderr and generated text. Missing references or decompilation errors can leave useful but incomplete output. On supporting versions, `--ignore-decompilation-errors` changes failure status; it does not repair the code.

When resolving referenced types matters, `-r "$reference_dir"` supplies the directory containing matching dependency assemblies. Do not substitute arbitrary versions merely to silence resolution errors. For a necessary whole-project view, use a new output directory:

~~~bash
ilspycmd --disable-updatecheck -p -o "$project_out" "$assembly"
~~~

Define `project_out` before use. `-p` requires `-o` and reconstructs project/source files; it does not recover the original source tree, build settings, comments or proof of a reproducible build. Do not build or run that project as part of passive inspection.

Trace the actual call and property-access path. A serializer can invoke setters while constructing objects and getters while serializing the response. A constant such as `Session = "Unauthorized"` is not an enforcement check by itself. An object-typed auto-property has generated accessors even if no explicit body is shown. Recognize async state-machine scaffolding and follow its body when needed; generated wrapper names are not separate application features. Nullable metadata does not add runtime null checks.

Record assembly hash, type/member and relevant dependency/settings together. Use `-il` for IL when a consequential reconstructed expression is ambiguous; decompiled C# is a reconstruction, not execution evidence. Keep embedded credentials out of shared excerpts.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Bagel pp. 9–20. Sources: [CLI help and examples](https://github.com/icsharpcode/ILSpy/blob/master/ICSharpCode.ILSpyCmd/README.md), [implementation](https://github.com/icsharpcode/ILSpy/blob/master/ICSharpCode.ILSpyCmd/IlspyCmdProgram.cs), [Json.NET type handling](https://www.newtonsoft.com/json/help/html/T_Newtonsoft_Json_TypeNameHandling.htm).
