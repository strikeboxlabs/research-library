---
name: sendemail
description: Submit an explicitly requested message with a selected attachment through the SendEmail SMTP client. Use when an explicit relay, MIME attachment, message-file input or SMTP acceptance result matters.
---

# Submit a reviewed message to its intended relay

Read this entire SKILL.md before acting. Require explicit authorization to send the chosen message, its sender/recipient, reviewed body/attachment and the configured relay's transport policy. No conditional resources are required. Finish with the submission status and acceptance evidence or the failed/uncertain stage; acceptance does not prove inbox delivery or opening.

Confirm the installed SendEmail implementation with `sendemail --help`, `sendemail --help message` and `sendemail --help networking`; executable capitalization can differ. This client is distinct from the local Sendmail command interface. Missing relay/client capability is a prerequisite gap, not a reason to install tools or change mail configuration automatically.

Define `smtp_server` as the intended `host:port`, `sender` and `recipient` as single ordinary mailbox addresses, `subject` as a reviewed single-line ASCII subject, `body` as an existing plain ASCII text file, `attachment` as its selected absolute file path and `submission_log` as a fresh private path. Reject header CR/LF, extra recipients and option-like inputs. Choose `tls_mode` from the relay's confirmed policy: `yes` requires STARTTLS support; `no` is appropriate only when the task explicitly permits that plaintext route, such as an owned local collector. Opportunistic `auto` can fall back to plaintext. TLS negotiation alone is not proof of the intended authenticated relay; verify this build's trust/name behavior when that assurance is required. This narrow example uses a relay already permitting the selected submission without SMTP credentials:

~~~bash
umask 077
sendemail -s "$smtp_server" -f "$sender" -t "$recipient" -u "$subject" \
  -o message-file="$body" -o message-content-type=text -o message-charset=us-ascii \
  -o tls="$tls_mode" -a "$attachment" > "$submission_log" 2>&1
status=$?
~~~

This sends mail; it is not a draft or dry run. `-a` constructs an attachment; it does not execute that file. Use normal message construction here, not `message-format=raw`, which treats input as a complete message and ignores the attachment option. Encoded MIME overhead can exceed an advertised SMTP size limit even when the original file is smaller. The sender field does not establish mailbox ownership or satisfy authentication. If the relay requires authentication, use its separately established credential/transport procedure; do not place a password into a copied command line.

Read status and diagnostics at the actual stage: connection/TLS, sender, recipient, DATA and final acceptance. An accepted message can later bounce, be filtered or remain queued. A timeout/disconnect after DATA can leave acceptance uncertain; check the selected relay's message evidence before resubmitting to avoid duplicates. Keep any delivery/read evidence separate from the client's success line. Sending a document does not prove an application opened it or ran content inside it.

See the packaged [SendEmail manual](https://manpages.debian.org/testing/sendemail/sendemail.1.en.html) and [implementation/extended help](https://sources.debian.org/src/sendemail/1.56-5.2/sendEmail/) for this version's input and transport behavior.
