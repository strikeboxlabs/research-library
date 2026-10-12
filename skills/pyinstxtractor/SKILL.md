---
name: pyinstxtractor
description: Extract a selected owned PyInstaller executable into a fresh work area. Use when embedded Python versions, CArchive/PYZ counts or repaired bytecode headers determine what was actually recovered.
---

# Extract the embedded application without launching it

Read this entire SKILL.md before acting. Require the selected acquired executable, a trusted installed extractor script and a matching Python interpreter. Use an isolated disposable analysis environment with an owned fresh work directory; this parser writes files and is not a containment boundary. All instructions are inline. Finish with the archive diagnostics and identified recovered artifacts, distinguishing partial extraction from complete recovery.

Define `extractor` as the verified absolute `pyinstxtractor.py` path, `artifact` as the selected absolute input, `python_bin` as the trusted interpreter and `work_directory` as the empty owned analysis directory. Preserve the input fingerprint and interpreter/extractor revision. Do not execute the acquired application to identify its packaging.

~~~bash
cd -- "$work_directory" || exit
"$python_bin" "$extractor" "$artifact" >extract.stdout 2>extract.stderr
status=$?
~~~

Inspect both streams and the status. Output goes below the current directory as `basename(input)_extracted`, rather than beside the input; an existing directory can be reused, so choose a fresh work area. Filename handling and parser assertions do not make malformed archives safe outside that environment. Keep reported renaming or skipped-member diagnostics attached to the recovered file inventory.

The detected Python major/minor should match the extracting interpreter for PYZ unmarshalling. On a mismatch, retain the first result as partial and use an available matching trusted environment in a new work directory. A CArchive extraction can succeed while PYZ extraction was skipped or individual members failed. Counts describe archive entries, not a guarantee every expected file was recovered. The tool's `2.1+` message identifies a packaging format family, not the exact PyInstaller release.

Possible entry points include bootstraps and runtime hooks as well as application bytecode. Identify the relevant `.pyc` through recovered filenames and static context. Automatically reconstructed bytecode headers enable compatible analysis; they do not recover original source comments, formatting or exact timestamps. A printed success message and zero exit status are insufficient alone: inspect errors, skip notices and the actual selected files before handing them to a compatible decompiler.

References: [extractor project and invocation](https://github.com/extremecoders-re/pyinstxtractor), [Python-version FAQ](https://github.com/extremecoders-re/pyinstxtractor/wiki/Frequently-Asked-Questions), [parser and output behavior](https://github.com/extremecoders-re/pyinstxtractor/blob/master/pyinstxtractor.py).
