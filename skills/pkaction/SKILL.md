---
name: pkaction
description: Inspect registered polkit action identifiers and defaults on the local Linux system. Use when an application's authorization action or its metadata is unclear.
---

# Inspect the registered action

Read this entire SKILL.md before acting. Require the intended local system bus and installed polkit tools. All instructions are inline. Finish with the selected action's metadata or the observed lookup error; registration is separate from authorization.

List the registered identifiers:

~~~bash
pkaction
~~~

Choose the exact identifier relevant to the application's documented operation. Define `action` as that identifier, then inspect its details:

~~~bash
pkaction --action-id "$action" --verbose
~~~

Retain status and diagnostics. Success is status zero; an error or unavailable authority leaves the lookup incomplete. An empty selection is not evidence that the application needs no authorization.

Action descriptions and default policies do not establish the current caller's effective rights. Local rules, subject/session attributes and operation details can affect that decision. Correlate the application's actual requested action with its authorization result; do not turn this inventory into an automatic attempt of each registered operation.

Reference: [packaged polkit manual](https://manpages.debian.org/trixie/polkitd/pkaction.1.en.html).
