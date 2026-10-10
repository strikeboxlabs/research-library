# Separate child output from the Python display


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
