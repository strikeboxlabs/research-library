---
name: mcs
description: Compile trusted local C# sources into a selected Mono managed assembly. Use to resolve explicit sources, assembly references, unsafe-language requirements and output-path mistakes without confusing compilation with runtime compatibility.
---

# Compile a selected managed assembly

Read this entire SKILL.md before acting. Require installed Mono mcs, reviewed local `.cs` sources, any referenced assemblies and a fresh owned output path. Select the intended assembly kind and complete with compiler status/diagnostics and the resulting artifact, or the exact missing dependency. Running the result is a separate task requiring the matching runtime and platform APIs.

For a small trusted console utility, supply all source files explicitly; use real paths for `source_file` and `output_file`:

~~~bash
mcs --version
test ! -e "$output_file" && test ! -L "$output_file"
mcs -target:exe "-out:$output_file" "$source_file"
~~~

Only compile after the destination check succeeds. The compiler writes the selected file and can replace an existing output. A managed `.exe` contains CIL; the suffix does not make it a native Linux binary or prove Windows API availability. Include all files that form the assembly, rather than expecting project discovery or incremental linking.

If trusted source uses unsafe C# pointer constructs, add `-unsafe`. The Microsoft-style `/unsafe` alias is accepted, but it enables a language feature rather than granting OS privileges or starting a service. Missing type/namespace errors need the correct source/reference, such as `-r:System.Core.dll` or `"-r:$assembly_file"`; installing unrelated libraries or suppressing warnings does not resolve that prerequisite. Review the selected compiler's language/profile support when modern syntax is rejected.

Use `-target:library` with a `.dll` output for a library. A missing `Main` error for an executable may indicate a library source or an omitted entrypoint file; multiple entrypoints may need the intended `-main:ClassName`. Do not change assembly kind solely to hide an error when the user needs an executable.

Retain compiler exit status and relevant diagnostics. After success, verify the newly created nonempty output at the explicit path. A stale file beside failed compilation is not a successful build. Report the source/reference set, kind and compiler version; test runtime behavior only in the appropriate controlled environment. Windows-specific P/Invoke declarations can compile on Linux while still requiring Windows at execution time.

See the [Mono compiler manual](https://github.com/mono/mono/blob/main/man/mcs.1) for profile, reference and option details, and [Mono C# compiler documentation](https://www.mono-project.com/docs/about-mono/languages/csharp/) for language support.
