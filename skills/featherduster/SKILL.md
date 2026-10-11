---
name: featherduster
description: Analyze selected owned local samples for encoding and statistical properties with FeatherDuster. Use when a ciphertext heuristic is mistaken for a confirmed cipher or sample import changes record boundaries.
---

# Analyze the selected local samples

Read this entire SKILL.md before acting. Require the trusted installed FeatherDuster launcher, its compatible interpreter/dependencies and complete owned samples with a known producer/representation. Verify imported boundaries and decoding decisions before interpreting analysis. No conditional resources are required. Finish with the selected sample set, transformations, heuristic results and unresolved producer facts.

The historical upstream CLI uses Python2 syntax; do not substitute Python3 or install dependencies to repair startup. Review the trusted local launcher/runtime. `featherduster --help` describes positional file imports; startup imports its modules even for help. A failure leaves this task unavailable in that environment.

Start the established launcher:

~~~bash
featherduster
~~~

In the console, select one import matching the stored representation:

| Command | Boundary to preserve |
|---|---|
| `import singlefile` | Enter the selected file path; the complete file is one sample. |
| `import multifile` | Enter a text file containing one encoded sample per line; blanks are removed and surrounding whitespace is stripped. |
| `import manualentry` | Enter one encoded sample; newline ends input and surrounding whitespace is stripped. |

Use `samples` to inspect the imported set, then `analyze` for encoding/statistical analysis. Separate unrelated producers into different sessions: the analysis assumes samples share a production process. If prompted to replace samples with decoded values, retain the original and record the decision; confirm representation and count again. A missing import or empty set is incomplete analysis.

Recommendations are leads. A short sample's length or low randomness score does not establish RC4, key reuse or a cryptographic weakness; cipher modes and container overhead can change length expectations. Correlate with the producer's format/mode and enough independent samples. This task ends at analysis; selecting or running an attack module is a separate task.

References: [upstream import and analysis conventions](https://github.com/nccgroup/featherduster), [CLI import/analysis implementation](https://github.com/nccgroup/featherduster/blob/master/featherduster/featherduster.py).
