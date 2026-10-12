---
name: pwncat-cs
description: Transfer a selected ordinary file through an already established pwncat-cs session on a controlled Linux fixture. Use when local versus remote path direction, implementation names or progress receipts obscure file identity.
---

# Transfer one selected fixture artifact

Read this entire SKILL.md before acting. Require the Caleb Stewart pwncat-cs implementation, an already established authorized session to the controlled fixture and exact nonsecret source/destination paths. No conditional resources are required. Finish with the transfer result and independently compared file identity; a progress bar alone is insufficient.

Confirm the installed implementation and its local command help. Packages named `pwncat` can refer to different software; a historical apt installation line does not establish that it supplies the `pwncat-cs` command. Identify the active session and its remote identity before selecting files. This task uses an existing session and does not create listeners or run enumeration/escalation modules.

At the **local pwncat prompt**, use literal inspected paths. The following paths are **illustrative fixture paths**, to be replaced with the selected artifact:

~~~text
download /home/fixture/artifacts/report.txt ./received-report.txt
upload ./reviewed-input.txt /home/fixture/artifacts/new-input.txt
~~~

Download reads remotely and writes locally; upload reads locally and writes remotely. Both use the existing session transport, so no extra HTTP server or callback is required. Choose fresh destinations: download can overwrite an existing local file, and neither direction should replace an application configuration or executable as an incidental transfer.

Retain the selected session, exact paths, diagnostics and reported byte count. Compare source and destination size and SHA-256 through the fixture's established file inspection mechanism before using the artifact. A copied transcript, matching filename or 100% receipt is not checksum evidence. Encoding used internally by the transfer is transport handling, not proof of content safety or authenticity.

If a path, permission or remote reader/writer fails, preserve the error and inspect that selected file/context. Do not compensate by changing identity or permissions. Transfer completion does not execute the downloaded/uploaded file. Handle cleanup only for this task's explicitly owned temporary artifact.

References: [download path semantics](https://pwncat.readthedocs.io/en/latest/commands/download.html), [upload over the existing session](https://pwncat.readthedocs.io/en/latest/commands/upload.html).
