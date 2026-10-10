---
name: python2
description: Use an existing Python 2.7 environment for legacy raw-pickle requests, Django signed-cookie construction or a selected Unix PTY child. Match encoding, serializer, protocol and dependencies instead of silently using a current Python stack.
---

# Legacy Python 2.7 operational tooling

Read this entire SKILL.md before acting. This supports a known legacy application contract, not general Python 2 development. Use a reviewed existing interpreter/environment; a Python 2 shebang or unversioned pip install does not identify its dependencies. For signed-cookie construction read [legacy Django sessions](references/django-signed-cookies.md) fully first; for an encoded raw-pickle handler and selected execution check read [raw pickle requests](references/raw-pickle.md) fully first. These are separate request contracts. The Unix PTY branch below needs neither Django nor pickle. Finish with the generated artifact and observed validation/effect separately; generation is not server acceptance.

Define `python2_bin` as the actual installed Python 2.7 invocation. Inspect its version; query Django only when using the signing branch:

~~~bash
"$python2_bin" --version
# Signed-cookie branch only:
"$python2_bin" -c 'import django; print(django.get_version())'
~~~

Do not import acquired application configuration just to identify settings: it is executable Python. Read its selected declarations and effective deployment context instead. Python 3 string/bytes handling, pickle defaults, signing algorithms and removed APIs can differ. A missing matching environment is a concrete prerequisite gap; report it instead of silently using the newest Django or installing tools as part of this procedure.

The signed-cookie reference describes the Django 1.6.11 API and Python 2.7 pickle protocol context. Resolve a different deployed version against its own code. See [legacy signing implementation](https://github.com/django/django/blob/1.6.11/django/core/signing.py) and [session serializers](https://github.com/django/django/blob/1.6.11/django/contrib/sessions/serializers.py).


## Give an authorized Unix child a terminal

In an established interactive channel reporting no TTY, define `child_bin` as the intended installed executable on that machine. Python 2.7's Unix PTY support can attach it:

~~~bash
"$python2_bin" -c 'import pty, sys; pty.spawn([sys.argv[1]])' "$child_bin"
~~~

Check the selected child's `tty`/`id` or equivalent terminal/identity result. This starts a child with the existing authority; it does not change UID, authenticate a network peer or configure the local relay terminal. Local echo, signal handling, job control and window dimensions remain separate. Do not use Python 3's newer wait-status conversion API as if it existed in this legacy invocation. Track/exit the owned child and restore terminal settings changed by the actual session; a quiet socket does not establish that it ended. See the [matching Unix PTY contract](https://github.com/python/cpython/blob/v2.7.18/Doc/library/pty.rst).
