---
name: ilspycmd
description: Inspect managed .NET assemblies from Linux with ILSpyCmd. Use to locate types, trace properties, serialization, crypto helpers and archive extraction paths, or recover readable code without launching the inspected application.
---

# Decompile the selected evidence

Use ILSpy's `ilspycmd` CLI, whose flags differ from the desktop frontend. Check `ilspycmd --version` and `--help`; the tool's own required .NET runtime can differ from the target assembly's framework. A missing tool runtime is not evidence that the captured assembly is invalid. This is a Linux CLI alternative to desktop dnSpy inspection.

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


# Trace archive writes before drawing a runtime conclusion

For a ZIP-consuming assembly, decompile the observed entrypoint/type using the commands above. Follow entry names through path construction to the exact extraction overload. `Path.Combine(base, entry.FullName)` does not enforce containment: a later rooted path can replace the base, and relative parent components need normalization and a boundary check. Interpret separators and roots for the application's OS; inspecting a Windows assembly on Linux does not change its Windows path semantics. Check the canonical destination, allowed root with a directory boundary, and link/reparse-point behavior separately.

`entry.ExtractToFile(destination)` creates a file but refuses an existing destination; overwriting requires another overload/setting. Missing parents, process permissions and exceptions still constrain writes. A discovered filename flow supports a potential out-of-directory write, not unrestricted overwrite or code execution. Preserve the method/overload and missing guard as evidence; actual process identity and destination access remain separate questions. See Microsoft's [extraction example and exceptions](https://learn.microsoft.com/en-us/dotnet/api/system.io.compression.zipfileextensions.extracttofile) when checking a specific framework.

Follow return values and ordering, not just method names. `String.Replace` returns a new string; discarding it leaves the original value unchanged. `Directory.GetFiles` returns an array of paths captured at that call: files created later are not automatically added to that array. A scanner that extracts entries then advances through the original array has not necessarily scanned those new entries in the same invocation. Resolve unclear branches in IL before translating surrounding prose into a guarantee.

# Follow a crypto helper across assemblies

When a database/config value feeds a decrypt method declared elsewhere, retain its row identity and follow the declaring assembly. A missing body in the executable does not establish missing code. Set `helper_assembly` to the matching captured DLL and `helper_type` to its observed fully qualified type:

~~~bash
ilspycmd --disable-updatecheck -r "$reference_dir" -t "$helper_type" "$helper_assembly" > "$helper_source"
~~~

Define `reference_dir` and a fresh `helper_source` before use. Trace both caller and helper: which row/field supplies ciphertext, which argument supplies the key, then decoding, byte encoding, IV, mode and padding. Base64 is a transport layer. A literal passed through `Encoding.UTF8.GetBytes` supplies raw bytes, not a password derivation function; count bytes rather than characters. Resolve numeric enums against the actual API: `CipherMode` 1 means CBC, while `CryptoStreamMode` 0 means Read. An omitted padding assignment requires checking the algorithm default; standard .NET symmetric algorithms default to PKCS7.

Follow the returned byte count as carefully as the cipher settings. A buffer allocated to ciphertext length can exceed the unpadded plaintext length. Decoding the entire zero-initialized buffer after one `CryptoStream.Read` can append NUL characters. The read can also be partial; [.NET 6 changed these stream semantics](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/6.0/partial-byte-reads-in-streams). For an independent format check, read through EOF and decode only bytes actually returned. Distinguish that corrected procedure from reproducing the application's exact behavior on its target framework. Readable text alone is not evidence of a valid application credential.


## Trace time-seeded key material precisely

For a helper using `new Random(seed)`, decompile its caller as well as the encryption routine using the type-selection procedure above. Follow the seed's time unit, integer conversion and every generator call. `DateTimeOffset.ToUnixTimeSeconds()` counts seconds; a millisecond value or local-time display is a different input. A sequence that fills a 16-byte IV then a 32-byte key must be reproduced in that order on the same generator instance. Reseeding for each array changes the sequence.

Record the target framework/runtime before porting this logic. Microsoft's [Random compatibility note](https://learn.microsoft.com/en-us/dotnet/api/system.random#notes-to-callers) does not guarantee identical sequences across major .NET versions. Verify a public known-seed vector on the relevant implementation before using a different runtime or language as a substitute; matching the seed number alone is insufficient.

Check explicit and default cipher settings, stream byte counts and the output open mode. `FileMode.Create` can truncate an existing destination; a failed decrypt can leave partial output. Keep any reviewed reconstruction separate from the original executable and original evidence. Header bytes suggest a format; validate the complete recovered structure with its reader before accepting the candidate. Successful padding or a file's existence does not establish correct recovery.
