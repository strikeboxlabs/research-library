# Inspect an owned script's failure

Use this only for a trusted owned local reproduction with understood effects, interpreter and dependencies. Debugging runs code; static inspection of an acquired script is a different task. Inspect applicable `.pdbrc` files first because pdb loads debugger commands from them.

Define `script` as the selected absolute source path and `python_bin` as its intended interpreter:

~~~bash
"$python_bin" -m pdb "$script"
~~~

At the initial `(Pdb)` prompt, `continue` runs the program. If it fails, module-mode pdb enters post-mortem debugging. Inspect:

~~~text
where
list
~~~

Record the exception, failing file/line and surrounding call stack. `up`/`down` select another frame. `quit` ends this debugging session; continuing/restarting can repeat program effects. Post-mortem inspection does not resume the failed statement.

Debugger expressions and unknown commands can execute Python in the selected frame; pdb is not a read-only viewer or a separate privilege boundary. A missing dependency or different environment can produce a different failure from the original program. An application can also deliberately invoke `pdb.post_mortem` on its traceback; that does not make exposing the debugger in a privileged service appropriate. See [Python pdb documentation](https://docs.python.org/3/library/pdb.html).
