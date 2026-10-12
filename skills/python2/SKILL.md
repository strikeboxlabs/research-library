---
name: python2
description: Use an existing Python 2.7 environment for selected legacy serving, request/session construction or a Unix PTY child, and interpret native-reference ownership or legacy input evaluation. Match runtime, protocol and dependencies before applying current Python assumptions.
---

# Legacy Python 2.7 operational tooling

Read this entire SKILL.md before acting. Select the known legacy application, native-reference or input-evaluation interpretation task. Use a reviewed existing interpreter/environment; a Python 2 shebang or unversioned pip install does not identify its dependencies. For signed-cookie construction read [legacy Django sessions](references/django-signed-cookies.md) fully first; for an encoded raw-pickle handler and selected execution check read [raw pickle requests](references/raw-pickle.md) fully first. These are separate request contracts. The Unix PTY branch below needs neither Django nor pickle. Finish with the generated artifact and observed validation/effect separately, or the supported static ownership/input finding; generation is not server acceptance.

For selected owned files served by an existing Python2.7 environment, read [legacy file server](references/local-file-server.md) fully before that procedure; this does not need Django or pickle.

For a CPython2.7 extension whose native object lifetime or reference-count explanation is unclear, read [native-reference ownership](references/native-ownership.md) fully before interpreting that code. It supports a benign count observation and static API/control-flow review, without importing the acquired extension.

Define `python2_bin` as the actual installed Python 2.7 invocation. Inspect its version; query Django only when using the signing branch:

~~~bash
"$python2_bin" --version
# Signed-cookie branch only:
"$python2_bin" -c 'import django; print(django.get_version())'
~~~

Do not import acquired application configuration just to identify settings: it is executable Python. Read its selected declarations and effective deployment context instead. Python 3 string/bytes handling, pickle defaults, signing algorithms and removed APIs can differ. A missing matching environment is a concrete prerequisite gap; report it instead of silently using the newest Django or installing tools as part of this procedure.

For a legacy prompt source review, Python2.7 `input` evaluates the entered expression, equivalent to eval(raw_input(prompt)); it is not Python3's text-only input. Follow the exact interpreter and any local rebinding before attributing that behavior. Print-statement syntax is a language-generation clue, not proof of which executable a native wrapper launches. Review the wrapper and the input-to-effect path as text; a setuid file mode does not establish that its child retains the same effective identity. For an owned text-input remediation use raw_input with the intended parser/validation, or migrate the application with matching dependency checks. Preserve the source locations and unresolved runtime/child identity without evaluating a supplied expression to demonstrate the finding. See the [versioned input contract](https://github.com/python/cpython/blob/v2.7.18/Doc/library/functions.rst).

The signed-cookie reference describes the Django 1.6.11 API and Python 2.7 pickle protocol context. Resolve a different deployed version against its own code. See [legacy signing implementation](https://github.com/django/django/blob/1.6.11/django/core/signing.py) and [session serializers](https://github.com/django/django/blob/1.6.11/django/contrib/sessions/serializers.py).


## Give an authorized Unix child a terminal

In an established interactive channel reporting no TTY, define `child_bin` as the intended installed executable on that machine. Python 2.7's Unix PTY support can attach it:

~~~bash
"$python2_bin" -c 'import pty, sys; pty.spawn([sys.argv[1]])' "$child_bin"
~~~

Check the selected child's `tty`/`id` or equivalent terminal/identity result. This starts a child with the existing authority; it does not change UID, authenticate a network peer or configure the local relay terminal. Local echo, signal handling, job control and window dimensions remain separate. Do not use Python 3's newer wait-status conversion API as if it existed in this legacy invocation. Track/exit the owned child and restore terminal settings changed by the actual session; a quiet socket does not establish that it ended. See the [matching Unix PTY contract](https://github.com/python/cpython/blob/v2.7.18/Doc/library/pty.rst).
