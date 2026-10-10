---
name: fickling
description: Statically inspect local Python pickle streams and extracted model metadata with Fickling. Use when severity thresholds, parse failures or incomplete container coverage could be mistaken for permission to load a model.
---

# Inspect pickle behavior without loading the object

Use the static CLI on an acquired file. `fickling.load()` and `pickle.load()` are different operations: they can deserialize and execute code. Do not use them to discover whether a file is safe. Check `fickling --version` and `fickling --help` because supported formats and analysis rules change.

## Select the actual input

The raw-pickle CLI below expects a pickle stream, not an arbitrary model archive. Inspect the container format and member listing first. Modern `torch.save` commonly produces ZIP containing `data.pkl`; older formats include tar and stacked pickle streams. `.pt` versus `.pth` does not establish which format was used. Extract the exact relevant member into a separate unprivileged workspace, preserving its archive identity and path. Account for all relevant members; one clean member does not cover the entire model or bundled Python code.

Define `pickle` as that existing nonempty raw input. Define `report` and `log` as fresh absolute paths; JSON output is appended, so reusing a report can mix separate scans:

~~~bash
umask 077
scan_status=0
fickling --check-safety --print-results --json-output "$report" "$pickle" > "$log" 2>&1 || scan_status=$?
printf 'Fickling exit status: %s
' "$scan_status"
~~~

Keep the status, diagnostics and report together. Stacked inputs can produce multiple adjacent JSON objects rather than a single object or array; a consumer must read every result. Empty/malformed output, missing expected results and unknown severities require investigation.

**Illustrative decisions:**

| Observation | Interpretation and next step |
|---|---|
| `LIKELY_UNSAFE`, process returns nonzero | Inspect the reported operations; do not accept it merely because it is below `OVERTLY_MALICIOUS`. |
| Parser error, traceback or missing report | Analysis is incomplete; check format, extraction and version support. Absence of findings is not a clean scan. |
| Complete reports say `LIKELY_SAFE`, exit zero | No unsafe operation was detected by these rules. This does not establish trust or authorise deserialization. |

The current CLI distinguishes unsafe findings from parser errors, but an uncaught tool failure can also return nonzero. Do not classify the outcome by exit status alone. A wrapper that rejects only one exact severity can accept other unsafe levels or scanner failures.

## Inspect why a finding occurred

For a supported input, the default CLI decompiles symbolically. Define fresh `decompiled` and `diagnostics` paths:

~~~bash
fickling "$pickle" > "$decompiled" 2> "$diagnostics"
~~~

Inspect imports, calls and unused results as text; do not run the generated Python. Unsupported opcodes or interpretation errors limit the conclusion. Normal tensor reconstruction can produce findings, but expected library names do not make every call benign. Successful inference or plausible model accuracy also does not prove that loading had no side effects.

Use the [Fickling CLI/source](https://github.com/trailofbits/fickling/blob/master/fickling/cli.py) for installed-version differences and [PyTorch serialization guidance](https://github.com/pytorch/pytorch/blob/main/docs/source/notes/serialization.md) for container and loader behavior. Since PyTorch 2.6, `torch.load` defaults to `weights_only=True` when no `pickle_module` is supplied; that is a restriction, not a general safety guarantee. Do not disable it just to make an unknown file load.
