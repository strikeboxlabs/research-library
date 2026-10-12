---
name: impacket-changepasswd
description: Change an owned account's known password through Impacket's SAMR client. Use when password-must-change status, password policy, protocol selection or misleading exit status complicates a permitted password change.
---

# Change one owned account password

Read this entire SKILL.md before acting; reuse complete current context. Require the installed supported Impacket client, one explicitly authorized account/DC, its known current password and the approved new password/lifecycle. Perform one selected change, inspect the server outcome and verify the account through its intended approved consumer or report the unresolved result.

Inspect `impacket-changepasswd -h`; installations may expose `changepasswd.py`. Define `changer` as the verified invocation, `domain` as the account domain, `account` as the owned account and `server` as the intended DC. For a supported SMB/SAMR password-change path:

~~~bash
"$changer" -protocol smb-samr "$domain/$account@$server"
status=$?
~~~

The reviewed client prompts for the current password, new password and its confirmation when those arguments are omitted. Keep both secrets out of argv and avoid debug logs that can reveal credential inputs. This is an account state change, not a login test.

Password change and administrative reset are different operations. `-reset` selects a privileged reset and is not a repair for a failed change. `STATUS_PASSWORD_MUST_CHANGE` and `STATUS_PASSWORD_EXPIRED` can prevent ordinary SMB login while the change protocol remains available. They do not grant a passwordless reset: SAMR can bind anonymously for an expired-password change while the operation still uses the old password. A deliberately known empty old password is an old value, not proof that arbitrary accounts need no credential.

Inspect the explicit server success or policy/error result. In the reviewed version, handler failure can be logged without a corresponding nonzero top-level exit; zero status alone is insufficient. After an uncertain connection loss, check the intended consumer once with the selected new credential before retrying a mutation. Retain the actual outcome and account/DC context without recording the password.

Policy/history restrictions, transport errors and lack of account rights need different fixes. Do not switch to hash-setting, weaker policy or administrative reset automatically. Updating a password does not itself prove every DC/consumer has accepted it, revoke existing tickets or update an application's stored credential. Account for the intended consumer and approved credential storage explicitly. See [Impacket's password client](https://github.com/fortra/impacket/blob/master/examples/changepasswd.py) and [Microsoft password-change mechanisms](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/password-change-mechanisms).
