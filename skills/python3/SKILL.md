---
name: python3
description: Inspect Python source and metadata, diagnose owned scripts, reproduce bytes, decode captures, or perform bounded protocol, database, D-Bus, HTTP-oracle and Unix terminal tasks. Use when byte contracts, response classes or execution context determine the result.
---

# Python operational inspection

Read this entire SKILL.md before acting; reuse complete current context. Use the source locator below for static inspection. Read the applicable reference fully before its procedure; load only the branch needed for the task. Finish with the observed source/data/query result and its limits; parsing, decoding or connection success alone is not proof of safe execution or complete coverage.

- Untrusted input, validation order or a misleading rejection: [evaluation flow](references/evaluation-flow.md).
- A file handler's join or filename helper is mistaken for containment: [path handling review](references/path-handling.md).
- A backup wrapper uses tarfile extraction or claims a filter makes every archive safe: [archive restore review](references/archive-restore.md).
- An lxml conversion service accepts XML and stylesheets: [XML and XSLT controls](references/xml-xslt-controls.md).
- Missing child output or ambiguous return values: [subprocess output](references/subprocess-output.md).
- A saved JSON document or line-record format fails to parse: [JSON documents](references/json-documents.md).
- A delimited record is reproduced from another language with different field boundaries: [literal separators and split limits](references/delimited-records.md).
- An owned local script's exception needs stack/source inspection: [post-mortem debugging](references/post-mortem.md).
- A dependency version, ambiguous module origin, site hook or writable bytecode cache needs static review: use the metadata and import-source guidance below.
- RESP argument/byte lengths or JSON-carried protocol data: [protocol framing](references/resp-framing.md), requiring `scripts/resp_frame.py`.
- Acquired AES key/counter/ciphertext and a known comparison contract: [AES-CTR reproduction](references/aes-ctr.md).
- Binary signatures, text/byte transformations or protocol body lengths: [binary evidence](references/binary-evidence.md).
- One acquired AD objectSid field needs strict binary decoding: [SID field interpretation](references/sid-field.md).
- Captured SAML HTTP Redirect URL: [offline decoding](references/saml-redirect.md).
- Native WebSocket with greeting tokens or interleaved heartbeat messages: [WebSocket exchange](references/websocket-exchange.md).
- A native WebSocket sends one legitimate JSON request without a greeting: [single request/reply](references/websocket-single-reply.md), using the separate `websockets` library.
- Authorized SQL testing carried by an observed WebSocket message: [application/query boundary](references/websocket-query.md), which also requires the exchange reference.
- A signed client-session object reaching an ORM relation filter and a stable authorized response oracle: [signed-session oracle](references/signed-session-oracle.md).
- Authorized LDAP-backed HTTP form testing with layered encoding or a response oracle: [form/oracle boundaries](references/ldap-form-oracle.md).
- MySQL CLI unavailable but a trusted Python environment already has PyMySQL: [bounded database inspection](references/pymysql-inspection.md).
- Inspect names on the owned Linux system bus with installed dbus-python: [D-Bus name inventory](references/dbus-names.md).
- Serve selected owned files or a cross-origin browser test module with an explicit response policy: [local file server](references/local-file-server.md).
- Save one approved HTTP(S) artifact with a size bound and fresh destination: [HTTP download](references/http-download.md).
- Read one owned NTP server's time sample through installed ntplib without setting the system clock: [NTP query](references/ntp-query.md).
- Interpret a selected OPC UA Variable's access metadata using installed asyncua: [OPC UA attribute evidence](references/opcua-attributes.md).
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

Use a trusted Python 3.8+ interpreter from the application's environment and define `distribution` as its distribution name, which can differ from the import name. Establish trust in its site configuration first: this helper uses `-I` but allows system site initialization. It reads metadata without importing that dependency:

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

For an ambiguous import, inspect the acquired source, launch mode and readable project files without importing the application. Python normally searches the input script's directory first; `-c`/`-m` ordinarily use the current directory. A local module can shadow a standard-library module. For example, `secrets` is standard-library Python3.6+, but `from secrets import SECRET_KEY` can refer to an application module of the same name. The import statement or a nearby filename alone does not prove the deployed origin. Correlate the actual launch/search-path configuration and the matching source; an isolated metadata helper intentionally uses a different search path. Finish with that supported origin or the missing path/loader evidence. See [search-path initialization](https://docs.python.org/3.12/library/sys_path_init.html) and [standard secrets API](https://docs.python.org/3.12/library/secrets.html).

Include cached bytecode and its parent directory in that trust review. A protected source file does not establish that its `__pycache__` is protected. Python's timestamp/size or hash checks concern cache freshness, not publisher authenticity; checked and unchecked hash modes differ. Inspect acquired ownership, permissions, interpreter and loader evidence without importing the application to test a suspect cache. A writable cache path is a deployment-integrity finding, not proof that particular bytes were loaded. Preserve the evidence and have the deployment owner restore trusted artifacts and appropriate ownership/permissions. A usage error can occur after imports have already run, while code inside a function requires a call; distinguish these execution points. See [cached bytecode invalidation](https://docs.python.org/3.12/reference/import.html#cached-bytecode-invalidation).

For site hooks, inspect acquired `.pth` files, directory ownership and the caller's `site.addsitedir()` locations as text. That call processes the selected directory's hooks when reached; it is not merely a path append or necessarily interpreter startup. Hooks can run before a wrapper validates its requested action. `-I` does not suppress all site initialization; `-S` suppresses the automatic pass, but cannot prevent application code explicitly processing a site directory. Record the actual call order and permissions without launching the suspect environment. Remediation should remove untrusted writers from privileged code-loading paths. See [Python site processing](https://docs.python.org/3.10/library/site.html).
