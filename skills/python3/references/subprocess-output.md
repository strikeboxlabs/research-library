# Separate child output from the Python display


Replacing `sys.stdout` or using `contextlib.redirect_stdout` does not capture a subprocess's inherited OS output stream. A blank editor result therefore does not establish that a child never ran. `os.system` returns status, not captured output; on Unix that status uses wait encoding. Inspect the actual capture implementation before attributing silence to a filter or command failure.

For a list passed to `check_output` with its default `shell=False`, Python launches the selected executable directly. A naive string `.split(" ")` is not shell parsing: quotes remain data, repeated spaces can produce empty arguments, and shell operators are not automatically interpreted. Missing input can fail in the caller before launching anything. A child returning nonzero raises `CalledProcessError`, potentially with captured output; distinguish this from a missing executable or caller exception. A shell-free argument list still permits whatever executable and options the application selects, so it is not an authorization boundary. Review the input-to-argv contract without adding a remote command endpoint.

Inspect `shell` explicitly: on POSIX, a single-element list containing command text with `shell=True` still sends that text through a shell. The list shape does not provide the direct-argv semantics above. For remediation, use a fixed trusted executable and separately validated argument values with `shell=False`; command options and resource scope still need their own policy. Capturing stdout while ignoring stderr/status cannot establish a valid DNS answer, completed action or absence of side effects.

For a file-producing child, an existing output path is also separate evidence. Identify a fresh destination and associate its bytes with the selected invocation; a random name can collide with an older file. Checking only `isfile()` after an unchecked process result does not establish that this invocation created the artifact. Preserve diagnostics and distinguish fresh output from stale output before serving or retrying it.

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
