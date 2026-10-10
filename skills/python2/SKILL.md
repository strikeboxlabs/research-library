---
name: python2
description: Use an existing Python 2.7 environment for a verified legacy Django signed-cookie procedure. Select the matching signing salt, serializer and protocol instead of running old cPickle code under a current Python/Django stack.
---

# Legacy Python 2.7 session tooling

Read this entire SKILL.md before acting. This supports a known legacy application contract, not general Python 2 development. Use a reviewed existing interpreter/environment; a Python 2 shebang or unversioned pip install does not identify its dependencies. For signed-cookie construction and an explicitly authorized deserialization check, read [legacy Django sessions](references/django-signed-cookies.md) fully first. Finish with the generated artifact and observed validation/effect separately; generation is not server acceptance.

Define `python2_bin` as the actual installed Python 2.7 invocation. Inspect the trusted environment before using its signing API:

~~~bash
"$python2_bin" --version
"$python2_bin" -c 'import django; print(django.get_version())'
~~~

Do not import acquired application configuration just to identify settings: it is executable Python. Read its selected declarations and effective deployment context instead. Python 3 string/bytes handling, pickle defaults, signing algorithms and removed APIs can differ. A missing matching environment is a concrete prerequisite gap; report it instead of silently using the newest Django or installing tools as part of this procedure.

The reference describes the Django 1.6.11 API and Python 2.7 pickle protocol context. Resolve a different deployed version against its own code. See [legacy signing implementation](https://github.com/django/django/blob/1.6.11/django/core/signing.py) and [session serializers](https://github.com/django/django/blob/1.6.11/django/contrib/sessions/serializers.py).
