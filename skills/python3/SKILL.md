---
name: python3
description: Inspect Python source and metadata, diagnose owned scripts, reproduce bytes, decode captures, or perform bounded protocol, database, D-Bus, HTTP-oracle and Unix terminal tasks. Use when byte contracts, response classes or execution context determine the result.
---

# Python operational inspection

Read this entire SKILL.md before acting; reuse complete current context. Use the source locator below for static inspection. Read the applicable reference fully before its procedure; load only the branch needed for the task. Finish with the observed source/data/query result and its limits; parsing, decoding or connection success alone is not proof of safe execution or complete coverage.

- Untrusted input, validation order or a misleading rejection: [evaluation flow](references/evaluation-flow.md).
- A file handler's join or filename helper is mistaken for containment: [path handling review](references/path-handling.md).
- Missing child output or ambiguous return values: [subprocess output](references/subprocess-output.md).
- A saved JSON document or line-record format fails to parse: [JSON documents](references/json-documents.md).
- An owned local script's exception needs stack/source inspection: [post-mortem debugging](references/post-mortem.md).
- A dependency version is needed without importing its module: use the metadata query below.
- RESP argument/byte lengths or JSON-carried protocol data: [protocol framing](references/resp-framing.md), requiring `scripts/resp_frame.py`.
- Acquired AES key/counter/ciphertext and a known comparison contract: [AES-CTR reproduction](references/aes-ctr.md).
- Binary signatures, text/byte transformations or protocol body lengths: [binary evidence](references/binary-evidence.md).
- Captured SAML HTTP Redirect URL: [offline decoding](references/saml-redirect.md).
- Native WebSocket with greeting tokens or interleaved heartbeat messages: [WebSocket exchange](references/websocket-exchange.md).
- Authorized SQL testing carried by an observed WebSocket message: [application/query boundary](references/websocket-query.md), which also requires the exchange reference.
- A signed client-session object reaching an ORM relation filter and a stable authorized response oracle: [signed-session oracle](references/signed-session-oracle.md).
- Authorized LDAP-backed HTTP form testing with layered encoding or a response oracle: [form/oracle boundaries](references/ldap-form-oracle.md).
- MySQL CLI unavailable but a trusted Python environment already has PyMySQL: [bounded database inspection](references/pymysql-inspection.md).
- Inspect names on the owned Linux system bus with installed dbus-python: [D-Bus name inventory](references/dbus-names.md).
- Serve selected owned files or a cross-origin browser test module with an explicit response policy: [local file server](references/local-file-server.md).
- An authorized Unix child needs a pseudo-terminal: [PTY session](references/pty-session.md).
- A selected legacy account switch may share a terminal and permitted TIOCSTI behavior must be reproduced: [shared-terminal input](references/terminal-input.md).

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

## Query installed distribution metadata

Use a trusted Python 3.8+ interpreter from the application's environment and define `distribution` as its distribution name, which can differ from the import name. This reads metadata without importing that dependency:

~~~bash
"$python_bin" -I - "$distribution" <<'PY'
import sys
from importlib.metadata import PackageNotFoundError, version

try:
    print(version(sys.argv[1]))
except PackageNotFoundError:
    sys.exit("distribution metadata unavailable in this interpreter's search path")
PY
~~~

`-I` excludes user-site and current-directory packages; missing metadata is a search-path gap, not proof that a service lacks the library. Retain the interpreter, distribution and returned version. Metadata can be stale or modified and does not prove which code a running service loaded. Combine it with static call-path evidence before assessing an advisory; importing a framework just to read `__version__` executes module initialization. See [distribution metadata](https://docs.python.org/3/library/importlib.metadata.html).
