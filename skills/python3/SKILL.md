---
name: python3
description: Inspect Python source without importing it, trace dynamic evaluation, distinguish child output/status, diagnose binary/text mistakes and decode captured SAML Redirect requests offline. Use when validation order, changed bytes or transport encoding obscure evidence.
---

# Inspect Python source without running the application

Select a trusted `python_bin` compatible with the source syntax and define `script` as the absolute path to a bounded local source file. Record the interpreter version. Importing an application to inspect it executes its module body; instead, read its source and parse an AST. This focused locator finds direct calls named `eval`, `exec` or `compile`:

~~~bash
"$python_bin" -I -S - "$script" <<'PY'
import ast
import sys
import tokenize

path = sys.argv[1]
with tokenize.open(path) as source_file:
    source = source_file.read()
tree = ast.parse(source, filename=path)
for node in ast.walk(tree):
    if (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"eval", "exec", "compile"}):
        print(f"{path}:{node.lineno}: {node.func.id}")
PY
~~~

`-I` excludes the current/script directory and user site from import search and ignores Python environment variables. `-S` also skips automatic site initialization. These reduce startup interference for this standard-library helper; they do not sandbox arbitrary code. `tokenize.open` respects the source encoding declaration. The helper parses the selected file without importing or evaluating it and creates no application bytecode cache.

An **illustrative** `validator.py:27: eval` points to a call site, not a proven vulnerability. Inspect that line and surrounding branches in the original file. Resolve the name's binding: a local function can shadow a builtin, while aliases, attribute calls and generated code can escape this small locator. No output is therefore not a clean security verdict. A syntax/encoding error leaves analysis incomplete; check the source and interpreter version instead of running the file to identify it. AST parsing is not a resource sandbox for huge or deeply nested input, nor proof that a program will compile or run successfully.

## Trace the value that actually reaches evaluation

Follow the input source, transformations, checks and evaluated argument separately. Checking an integer extracted from one part of a ticket does not validate another string later passed to `eval`. Removing formatting markers does not restrict Python's expression grammar. `compile` creates a code object; identify where it is later executed. `eval` evaluates an expression that can call functions, and `exec` executes statements.

Trace through called libraries too: an uploaded data file can reach evaluation inside a parser even when the web handler contains no direct `eval`. Restricting globals or setting `__builtins__` to `None` does not establish a sandbox. The [pymatgen parser advisory](https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f) documents precisely this failure. Identify the deployed dependency version, transformation function and reachable input before attributing it to the application; a filename extension or server banner is insufficient. Review source without importing the library or parsing the suspect file as a shortcut.

Check order as well as conditions. In an expression using `and`, the right operand is evaluated only when the left operand is truthy. A later acceptance check cannot undo an earlier effect. This **illustrative, harmless** example explains why a rejection message does not establish that nothing ran:

~~~python
def observed():
    print("effect reached")
    return False

result = True and observed()
print("accepted:", result > 100)
~~~

Its illustrative output is `effect reached` followed by `accepted: False`. Inspect the effect and the final predicate separately. If a script is invoked through sudo, combine this input flow with the exact allowed interpreter, script, RunAs identity and source ownership; a policy listing alone does not prove which branches are reachable.

For remediation, parse the intended data format and validate the complete consumed value. `ast.literal_eval` accepts literals/containers, not general arithmetic or function calls, and still has resource limits. Neither it nor this AST locator is a general sandbox. Retain the source location, input-to-call path, relevant guards and any unresolved dynamic binding as evidence; do not execute a privileged wrapper merely to demonstrate the finding.

See Python's [AST reference](https://docs.python.org/3.12/library/ast.html), [startup flags](https://docs.python.org/3.12/using/cmdline.html), [evaluation functions](https://docs.python.org/3.12/library/functions.html#eval), [Boolean semantics](https://docs.python.org/3.12/library/stdtypes.html#boolean-operations-and-or-not) and [source encoding reader](https://docs.python.org/3.12/library/tokenize.html#tokenize.open).

## Separate child output from the Python display

Replacing `sys.stdout` or using `contextlib.redirect_stdout` does not capture a subprocess's inherited OS output stream. A blank editor result therefore does not establish that a child never ran. `os.system` returns status, not captured output; on Unix that status uses wait encoding. Inspect the actual capture implementation before attributing silence to a filter or command failure.

For a controlled, small-output reproduction, collect stdout, stderr and status separately. This harmless child uses the current trusted interpreter:

~~~python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-I", "-S", "-c",
     "import sys; print('child output'); print('diagnostic', file=sys.stderr); sys.exit(3)"],
    capture_output=True, text=True, timeout=5,
)
print(result.returncode, repr(result.stdout), repr(result.stderr))
~~~

The **illustrative** result contains status `3`, `child output\n` and `diagnostic\n`. Output can accompany failure. A launch error or timeout raises an exception instead of returning this completed result; retain that distinction. `capture_output` buffers in memory and `text=True` decodes/normalizes text, so use files or byte mode for large output or exact-byte evidence. See [subprocess](https://docs.python.org/3/library/subprocess.html#subprocess.run) and [stdout redirection](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout).

## Inspect binary evidence without text conversion

When a script constructs a file or request body, check the bytes before changing the receiving service. Python 3 `str` holds Unicode; `"\x89"` is a character, while `b"\x89"` is one byte. Encoding the former as UTF-8 produces `c2 89`. Use bytes literals or binary file reads for binary content; choose an encoding only for a genuinely textual field.

Define `artifact` as a local regular working-copy file and inspect only its first 16 bytes with the trusted interpreter selected above:

~~~bash
"$python_bin" -I -S - "$artifact" <<'PY'
import sys

with open(sys.argv[1], 'rb') as source_file:
    prefix = source_file.read(16)
signature = bytes.fromhex('89504e470d0a1a0a')
print('prefix_bytes:', len(prefix))
print('hex:', prefix.hex(' '))
print('png_signature:', prefix.startswith(signature))
PY
~~~

An **illustrative** prefix `c2 89 50 4e 47 0d 0a 1a 0a` suggests the PNG signature passed through UTF-8 text encoding. Trace where the bytes became text and where they were encoded; do not blindly strip `c2` from the artifact. Fewer than eight bytes cannot contain the complete PNG signature. `png_signature: True` establishes only that prefix, even for an eight-byte file with no image chunks. Validate the complete artifact with its intended decoder before claiming a usable image. `prefix_bytes` is the bounded read length, not the file size.

For multipart clients, inspect the prepared part's bytes, not just its declared MIME type or the script's unconditional success message. A local file check alone does not prove the transmitted body was identical; library encoding and application acceptance need separate evidence.

See Python's [binary versus text I/O](https://docs.python.org/3.12/library/functions.html#open), [bytes and encoding](https://docs.python.org/3.12/library/stdtypes.html#bytes-objects) and the [PNG signature specification](https://www.w3.org/TR/png-3/#5PNG-file-signature).

For a captured SAML HTTP Redirect URL, use [bounded offline decoding](references/saml-redirect.md). It separates URL/base64/DEFLATE errors from XML meaning and signature validation.
