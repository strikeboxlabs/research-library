---
name: remmina
description: Open an approved remote desktop from Linux with Remmina's CLI launcher. Use when choosing an RDP URI or reviewed connection profile, missing graphical/plugin support or a launch status obscures the actual session result.
---

# Launch the selected desktop session

Read this entire SKILL.md before acting. Require an available graphical session, installed protocol plugin, a known approved endpoint and the user's intended account/profile. Review profile commands and connection settings before opening it. Finish with the actual connected endpoint/account and requested desktop result; a launched window or zero CLI status alone is incomplete.

Inspect the installed invocation:

~~~bash
remmina --version
remmina --help
~~~

For an existing reviewed profile, define `profile` as its absolute .remmina path:

~~~bash
remmina -c "$profile"
~~~

For a simple RDP connection, define `rdp_uri` as a reviewed URI such as the **illustrative** `rdp://operator@desktop.example.invalid`, with no password embedded:

~~~bash
remmina -c "$rdp_uri"
~~~

`-c` connects using a profile or supported URI; `-e` edits a profile. This launcher opens a graphical client, not a headless remote command. Keep the argument quoted, and use an existing profile's explicit domain/account settings when URI interpretation would be ambiguous. Supply credentials through the approved interactive/secret-store flow.

A profile may contain pre/post commands, SSH tunneling, shared folders or other connection effects. Review those settings and the endpoint before loading a downloaded profile. The [upstream user guide](https://github.com/FreeRDP/Remmina/wiki/Remmina-User%27s-guide) describes profile command hooks.

Separate a missing display/plugin, connection failure, certificate identity problem, account authentication and denied desktop access. Preserve the actual diagnostic; do not suppress server-identity checks to clear a connection error. Once connected, confirm the selected host/account within the session before performing the requested work. A different tool's authentication badge does not establish desktop usability or administrative rights.

Disconnect the task's session when finished; closing the client need not log off the remote account. Avoid quitting a shared Remmina instance just to close one connection. See the packaged upstream [Remmina manual](https://man.archlinux.org/man/remmina.1.en) for URI/profile and installed-option differences.
