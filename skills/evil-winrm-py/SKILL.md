---
name: evil-winrm-py
description: Open an authorized Windows WinRM session using an existing Kerberos cache and read selected identity or registry metadata with evil-winrm-py. Use to diagnose endpoint, SPN and cache mismatches without confusing a prompt with verified privileges.
---

# Verify a selected WinRM session

Read this entire SKILL.md before acting. Require the installed Python implementation, an approved Windows endpoint/account, a current owned Kerberos cache/configuration and permission for the selected remote reads. Follow connection, identity and requested metadata steps; finish with returned evidence or the exact unresolved prerequisite. This is a remote execution session, even when selected commands only read data.

Check `evil-winrm-py --version` and `--help`; Ruby evil-winrm has a different interface. Verify this installation's Kerberos dependencies: the reviewed build can continue with its NTLM default when those imports are unavailable, despite `-k`. Treat that as a missing prerequisite. Define `host`, `port` and `uri` as the approved endpoint, `service_host` as its registered lowercase service hostname, `krb_config` and `cache` as the selected absolute local paths. Check cache principal/expiry and realm/KDC/time configuration. A ticket does not prove WinRM authorization.

For an approved HTTP endpoint:

~~~bash
KRB5_CONFIG="$krb_config" KRB5CCNAME="$cache" evil-winrm-py \
  -i "$host" --port "$port" --uri "$uri" -k --no-pass --spn-hostname "$service_host"
~~~

For the configured HTTPS endpoint, add `--ssl` and use its actual port. The reviewed v1.5.0 passes `cert_validation=False`; HTTPS therefore does not validate the server certificate in that implementation. If certificate verification is a prerequisite, this build does not satisfy it: use a verified supported client/build instead. A service hostname override selects Kerberos identity, not routing or TLS certificate validity. A DNS alias/IP mismatch can cause an SPN failure even with a valid TGT. Retain endpoint/authentication errors before another account attempt.

Inside the connected shell, request identity, machine and working-directory evidence:

~~~powershell
whoami
$env:COMPUTERNAME
Get-Location
~~~

A profile-looking prompt is not token identity, administrator membership or SYSTEM privilege. Preserve the returned account and machine with the selected connection. For one approved registry property, define `$registryPath` and `$propertyName` as the exact requested non-secret setting:

~~~powershell
Get-ItemProperty -LiteralPath $registryPath -Name $propertyName -ErrorAction Stop
~~~

Missing property/access errors are unknown or absent-as-reported, not a default value. A configured value is not effective-policy proof without the relevant build/service behavior. Do not change it to complete a read task.

Exit with `exit` and record connection/read results. Session/debug logs can retain sensitive command output. `runps` executes a local script remotely and `loadps` evaluates its contents to load functions; neither is an inert inspection. This task does not require those commands. See the [pinned usage guide](https://github.com/adityatelange/evil-winrm-py/blob/v1.5.0/docs/usage.md) for implementation-specific options and compare actual installed help.
