---
name: tee
description: Write the same input to a selected file and stdout with tee, including an authorized privileged append. Use when shell redirection permissions, accidental truncation or echoed output obscures whether the file changed.
---

# Write the selected stream

Read this entire SKILL.md before acting. Establish the selected destination, append versus replacement, writer identity and intended bytes. Finish with tee's status and the actual file content; seeing echoed input on stdout does not prove a successful write.

GNU tee copies stdin to each selected file and stdout. Without -a it truncates an existing file; -a appends. It is not an editor, duplicate detector or atomic update. Define `file` as the inspected destination and `line` as the exact single record, without an embedded newline. For an ordinary owned file:

~~~bash
printf '%s\n' "$line" | tee -a -- "$file"
~~~

Check the pipeline status immediately: in the usual shell it is the final tee status; Bash pipefail also exposes a failed producer. Then verify the intended record in the selected file. An error can leave partial output or change one destination while another fails. Retrying an append can duplicate a record, so inspect first.

When the task explicitly requires a privileged write and the selected sudo policy permits it:

~~~bash
printf '%s\n' "$line" | sudo tee -a -- "$file"
~~~

Here tee opens the file under sudo. In `sudo printf ... >>file`, the calling shell opens the redirection before sudo, so that spelling does not grant the file open additional rights. Conversely, a sudo permission to run tee can have consequential file-write scope; it is not limited to the producing command. Preserve the existing file and its content/ownership when restoration is required. For a hosts-file record, confirm the intended name/address and existing mapping before appending; a successful write is separate from actual resolver behavior.

Use `>/dev/null` after tee only when discarding stdout is intended; it does not suppress stderr or validate the file. GNU --output-error controls broken-output handling and varies by implementation. See [the packaged GNU manual](https://manpages.debian.org/bookworm/coreutils/tee.1.en.html) for append and output-error behavior.
