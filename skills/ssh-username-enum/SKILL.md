---
name: ssh-username-enum
description: Use Justin Gardner's CVE-2018-15473 OpenSSH username enumeration helper for a selected account set. Use to interpret the malformed-authentication oracle, legacy Paramiko compatibility and inconclusive transport results.
---

# OpenSSH malformed-request account oracle

Read this entire SKILL.md before acting. Require the reviewed installed helper/build, compatible interpreter/Paramiko and a selected SSH endpoint/account set. Validate the response distinction before enumerating; finish with classified accounts, controls and failed/incomplete attempts. A valid-user signal does not authenticate the account or establish its password.

This package describes Rhynorater/Justin Gardner's `sshUsernameEnumExploit.py` interface, also distributed historically as `45233.py`; it is not a generic interface for every CVE helper. The vulnerable server parses malformed authentication requests differently for nonexistent users. This is a parsing/response oracle; OpenSSH 7.8's timing mitigations are a separate change. A version banner alone cannot establish exposure, especially with distribution backports.

Define `enum_python` as the compatible installed interpreter, `enum_script` as the reviewed installed helper path, `ssh_host`/`ssh_port` as the scoped endpoint, and `control_user` as a known existing account. Inspect that build's help before using these options:

~~~bash
"$enum_python" "$enum_script" --help
"$enum_python" "$enum_script" --port "$ssh_port" --username "$control_user" "$ssh_host"
~~~

Current upstream also tests three randomly generated usernames before the selected task; they are likely negatives, not guaranteed nonexistent accounts. Require distinguishable controls before interpreting its output. A patched target can cause the helper to exit **zero** with a not-vulnerable message and no enumeration. An exception, negotiation failure, timeout or rate-limited connection is inconclusive, not an invalid account.

For `accounts` as a small reviewed file containing one exact username per line and `results` as a fresh private file:

~~~bash
umask 077
"$enum_python" "$enum_script" --port "$ssh_port" --threads 1 --userList "$accounts" --outputFile "$results" --outputFormat json "$ssh_host"
~~~

The option is called threads, but this upstream uses a multiprocessing pool. It can retry transport failures and opens more connections than the list length. It strips line-edge whitespace. Keep stderr/status and check the complete result: output keys are `Valid` and `Invalid`; rejected/failed tasks may leave no result file. Compare the returned unique account set with the intended list; duplicates can be deduplicated in JSON. Do not classify by `grep valid`, which also matches negative text in list output.

The helper patches private Paramiko authentication-handler internals at import time. Its requirements leave Paramiko unpinned, and modern versions may expose `_handler_table` as a property or change handler behavior. Even help can fail before argument parsing. Keep that as a local compatibility gap: use the controlled image's verified compatible environment or a reviewed updated implementation with its own verified interface. Do not install/downgrade libraries or silently patch the tool during an account check. The exact historical helper/interpreter is not inferred from a renamed script file.

Resolve details with the [upstream helper](https://github.com/Rhynorater/CVE-2018-15473-Exploit), [argument/oracle implementation](https://github.com/Rhynorater/CVE-2018-15473-Exploit/blob/master/sshUsernameEnumExploit.py) and [OpenSSH 7.8 parsing fix](https://www.openssh.org/txt/release-7.8). Password verification or login is a separate selected task.
