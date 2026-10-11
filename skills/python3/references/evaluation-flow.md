# Trace the value that actually reaches evaluation


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

String formatting is a separate mechanism from eval. In a source review, identify which string becomes the format template and which values are arguments. Concatenating external data into the template exposes it to replacement-field parsing; passing a string as a value to a fixed `"{label}".format(label=value)` template keeps its braces as data. Keep templates fixed and avoid passing rich internal objects to external templates. A formatting error does not prove data remained confidential, and formatting alone is not a demonstrated arbitrary-code execution path. See [format-string syntax](https://docs.python.org/3/library/string.html#format-string-syntax).

See Python's [AST reference](https://docs.python.org/3.12/library/ast.html), [startup flags](https://docs.python.org/3.12/using/cmdline.html), [evaluation functions](https://docs.python.org/3.12/library/functions.html#eval), [Boolean semantics](https://docs.python.org/3.12/library/stdtypes.html#boolean-operations-and-or-not) and [source encoding reader](https://docs.python.org/3.12/library/tokenize.html#tokenize.open).
