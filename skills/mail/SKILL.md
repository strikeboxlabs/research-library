---
name: mail
description: Select the correct mail or mailx implementation and submit a requested message from Linux. Use when attachment flags, SMTP settings, subject handling or delivery claims differ between GNU Mailutils and S-nail.
---

# Identify the mail implementation first

`mail` and `mailx` are executable names shared by incompatible programs. Inspect the resolved binary, package and local manual before copying flags from a writeup. Attended uses S-nail; Awkward uses GNU Mailutils.

| Operation | GNU Mailutils mail | S-nail |
|---|---|---|
| Subject | `-s` | `-s` |
| Attach a file | `-A` / `--attach` | `-a` |
| Add a header | `-a` / `--append` | Use the installed version's header facilities; GNU syntax is not portable. |
| SMTP destination | Inspect configured mailer/transport | `-S mta=smtp://host:port`, with appropriate authentication/TLS settings. |

Do not use a send command merely to inspect configuration. It can submit through a local MTA even without an explicit server argument. Confirm the intended route and sender before a requested delivery.

For **GNU Mailutils**, define `recipient` as one verified ordinary email address, `subject` as the intended single-line subject, and `body`/`attachment` as existing absolute files. When sending that message is part of the task:

~~~bash
mail --subject="$subject" --attach="$attachment" -- "$recipient" < "$body"
~~~

Omit `--attach` when no attachment is wanted. Keep the subject in one argument; reject CR/LF header injection and do not assemble a command with `eval`. An unquoted subject can become additional options: Mailutils `--exec` runs mail commands and those can invoke a shell. Shell quoting does not validate recipient syntax; mail programs can also support special file/pipe recipients. The example assumes an ordinary mailbox, not an arbitrary destination string.

Do not transplant GNU's `--` usage into S-nail blindly: S-nail can use it to introduce MTA arguments. Likewise, supplying `-a` to the wrong implementation may create a header instead of an attachment. Check the generated MIME message at the controlled test receiver before relying on a batch submission.

A zero exit status or SMTP acceptance establishes submission at that stage, not inbox delivery, attachment opening or execution. Retain the destination, time and relevant queue/message identifier; diagnose rejection, deferred delivery and recipient-side filtering separately.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Attended pp. 5–8; Awkward p. 24. Sources: [GNU Mailutils invocation](https://mailutils.org/manual/html_node/Invoking-Mail.html), [S-nail manual](https://www.sdaoden.eu/code-nail.html).
