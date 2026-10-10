---
name: python3
description: Inspect Python source without importing it, trace evaluation and output/byte errors, decode SAML captures, use an existing PyMySQL driver or reproduce bounded HTTP-form/LDAP and token-based WebSocket/query exchanges.
---

# Python operational inspection

Read this entire SKILL.md before acting; reuse complete current context. Use the source locator below for static inspection. Read the applicable reference fully before its procedure; load only the branch needed for the task. Finish with the observed source/data/query result and its limits; parsing, decoding or connection success alone is not proof of safe execution or complete coverage.

- Untrusted input, validation order or a misleading rejection: [evaluation flow](references/evaluation-flow.md).
- Missing child output or ambiguous return values: [subprocess output](references/subprocess-output.md).
- Changed signatures or multipart bytes: [binary evidence](references/binary-evidence.md).
- Captured SAML HTTP Redirect URL: [offline decoding](references/saml-redirect.md).
- Native WebSocket with greeting tokens or interleaved heartbeat messages: [WebSocket exchange](references/websocket-exchange.md).
- Authorized SQL testing carried by an observed WebSocket message: [application/query boundary](references/websocket-query.md), which also requires the exchange reference.
- Authorized LDAP-backed HTTP form testing with layered encoding or a response oracle: [form/oracle boundaries](references/ldap-form-oracle.md).
- MySQL CLI unavailable but a trusted Python environment already has PyMySQL: [bounded database inspection](references/pymysql-inspection.md).

## Locate evaluation calls without importing source

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

References: [AST limits](https://docs.python.org/3.12/library/ast.html), [interpreter startup](https://docs.python.org/3.12/using/cmdline.html), [source encoding](https://docs.python.org/3.12/library/tokenize.html#tokenize.open).
