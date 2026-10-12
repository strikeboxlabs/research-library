---
name: xfreerdp
description: Connect to an approved RDP desktop with the FreeRDP X11 client. Use when client version, account/domain selection, certificate identity or missing graphical support determines whether the requested desktop session is usable.
---

# Open the selected RDP desktop

Read this entire SKILL.md before acting. Require a working X11 display, the installed FreeRDP client, an approved endpoint and the intended account/domain. All steps are inline. Finish with the connected host/account, requested desktop result and session cleanup; a socket, authentication success or launched window alone is incomplete.

Select the installed binary as `rdp_bin`; distributions can name it `xfreerdp3` or `xfreerdp`. Confirm its own options before applying examples:

~~~bash
"$rdp_bin" /version
"$rdp_bin" /help
~~~

Define `endpoint` as the approved hostname, optionally with its RDP port, and `account` as the selected username. With FreeRDP 3's documented credential-input option, run from an interactive terminal:

~~~bash
"$rdp_bin" "/v:$endpoint" "/u:$account" /from-stdin
~~~

Supply the password at the client's credential prompt. Do not put it in command arguments or a shell pipeline recorded by the task. If the account needs a domain, add the installed client's `/d:` argument with the intended domain, or its supported qualified username form; do not guess between a local account and a domain account. Missing prompt support or an unattended stdin leaves this credential flow unavailable.

Check a certificate prompt against the approved server identity and independently supplied certificate evidence. Preserve a mismatch diagnostic and resolve the endpoint/trust problem. A changed certificate is not evidence that ignoring checks will reach the intended host.

For an owned endpoint explicitly configured for interactive Windows logon without NLA, choose that mode from the installed client's help. FreeRDP 3 documents `/sec:nla:off` to disable only NLA negotiation; `/sec:nla` instead forces NLA and disables other modes. With that established server requirement, open the approved endpoint and enter the supplied account at its Windows logon screen:

~~~bash
"$rdp_bin" "/v:$endpoint" /sec:nla:off
~~~

Retain certificate validation and the negotiated security result. This client choice does not change server policy or remove Windows account authentication. An NLA rejection alone does not justify selecting a weaker mode, and a blank-password notice applies only to its explicitly configured account. Historical `-sec-nla` spelling needs installed-version confirmation. Dynamic resolution is an independent display feature, not an authentication fix.

Distinguish missing display/client support, network timeout, certificate validation, authentication rejection and denied desktop access. An RDP login can succeed while the account lacks administrative rights or the requested application. Confirm the remote host/account inside the session before working. Review any loaded .rdp profile, action scripts and resource-redirection settings; these can run local hooks or expose local files/devices.

Disconnect the task's session when its work ends. Use the remote account's logoff action only when the task requires terminating that session; closing the client can leave it running. Preserve the actual session outcome and any unresolved prerequisite.

Reference: [FreeRDP 3 X11 client manual](https://manpages.debian.org/trixie/freerdp3-x11/xfreerdp3.1.en.html).
