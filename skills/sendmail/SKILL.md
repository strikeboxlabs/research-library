---
name: sendmail
description: Submit an explicitly requested message through the Sendmail 8 command interface and inspect queue evidence. Use to distinguish message headers, envelope recipients, dot handling and queued versus delivered mail.
---

# Select the local submission implementation

Read this entire SKILL.md before acting. Require an explicitly requested message and intended envelope recipient, then identify the installed implementation below and construct/review the message before submitting. No conditional resources are required. Finish with submission/queue evidence and any delivery uncertainty; a successful command is not inbox delivery.

Resolve the installed `sendmail` executable and its package/manual. This name can belong to Sendmail, Postfix, Exim or a lightweight compatibility client; administrative and queue flags are not universally interchangeable. The procedure below targets the Sendmail 8 interface. It uses the configured local mail route and can submit mail without an explicit SMTP host argument.

For an explicitly requested message, define `sendmail_bin` as that verified executable, `recipient` as one intended ordinary mailbox address, `subject` as a single-line ASCII subject, `body` as the reviewed plain ASCII body file and `message` as a fresh private output path. Reject CR/LF in header values and reject pipe/file/option-like recipient input. Local aliases can expand to multiple destinations; establish the intended mailbox or alias before submission.

~~~bash
umask 077
printf 'To: %s\nSubject: %s\n\n' "$recipient" "$subject" > "$message" &&
cat -- "$body" >> "$message"
~~~

Require successful construction and review that file before sending. The blank line separates headers from body. This minimal example relies on the configured MTA to supply missing origin/date identifiers; use a MIME-aware generator for non-ASCII text or attachments.

~~~bash
"$sendmail_bin" -i -- "$recipient" < "$message"
status=$?
~~~

`-i` preserves leading dots and a body line consisting only of `.`. The command argument is the envelope recipient; the `To:` header alone does not select it in this mode. `-t` instead derives recipients from To/Cc/Bcc headers and removes Bcc before transmission, so do not add it to an unreviewed message. A From header is not the envelope sender; `-f` changes that sender under the implementation's policy.

## Establish submission, then delivery

Retain status, stderr, submission time and any queue identifier. A zero status does not prove inbox delivery or that a recipient opened a link. On Sendmail, inspect the queue without triggering delivery:

~~~bash
"$sendmail_bin" -bp
~~~

Correlate the specific identifier with available MTA logs or delivery-status messages. Absence from the visible queue is not proof of delivery: it may already have failed, moved or be hidden by access limits. Temporary failure can leave a queued message; check before resubmitting to avoid duplicates. `-q` processes queued mail and is not a read-only status check. Resolve routing or rejection at the reported stage rather than changing system configuration as a diagnostic default.

See the [Sendmail manual maintained in the FreeBSD source tree](https://github.com/freebsd/freebsd-src/blob/stable/13/contrib/sendmail/src/sendmail.8) for submission flags, aliases, exit meanings and queue behavior; follow the installed provider's manual when it differs.
