---
name: h2csmuggler
description: Check one authorized h2c upgrade endpoint and compare a selected HTTP/2 request with its ordinary edge response. Use when upgrade banners, multiple responses or application redirects are being mistaken for an access-control bypass.
---

# Separate upgrade acceptance from application access

Use a reviewed local Bishop Fox h2csmuggler script and compatible Python/hyper-h2 environment. Define `script` as its absolute path and inspect `python3 "$script" -h`. The upstream HTTPS path uses `ssl.wrap_socket`, removed in Python 3.12, and lacks modern hostname verification/SNI handling. Resolve client compatibility before interpreting a connection failure as a server result; do not repair it by silently weakening TLS verification.

Define `edge_url` as one approved upgrade URL, `seconds` as a positive total test budget, and `upgrade_log` as a fresh private file. With GNU timeout available:

~~~bash
umask 077
timeout --signal=INT --kill-after=2s "$seconds" \
  python3 "$script" -x "$edge_url" -m 5 --test >"$upgrade_log" 2>&1
~~~

`-m` is a socket timeout, not a total runtime cap. Upstream `--test` declares success after seeing HTTP 101, before confirming useful HTTP/2 application data. A timeout, malformed response or 101-only success is therefore incomplete evidence of tunneling. A proxy may itself support h2c without bypassing any rule.

If the task includes comparing application access, define `probe_url` as one agreed non-mutating endpoint on the same intended authority, plus fresh private `normal_headers`, `normal_body` and `tunnel_log` paths:

~~~bash
curl --http1.1 --silent --show-error --connect-timeout 5 --max-time 15 \
  --dump-header "$normal_headers" --output "$normal_body" "$probe_url"
timeout --signal=INT --kill-after=2s "$seconds" \
  python3 "$script" -x "$edge_url" -m 5 "$probe_url" >"$tunnel_log" 2>&1
~~~

Compare status, body and Location for the **requested probe**, not the first response printed. The initial response belongs to the upgrade request; later output follows `Requesting - ...`. **Illustrative:** an initial 200 followed by a 302 to a role-error page establishes an application rejection, not successful access to the requested data. An edge 403 changing to an application rejection can identify a changed enforcement layer while application authorization still holds.

Keep method, hostname, credentials and cache context equivalent before attributing a difference to the tunnel. Upstream `-H 'Name: value'` headers apply to the later HTTP/2 request, not the initial upgrade request; it has no general curl-compatible cookie-jar behavior. An authenticated upgrade requirement may therefore need a different client. The positional URL sets HTTP/2 authority/path through the edge connection; it does not make a separate direct connection to that hostname.

The upstream implementation also omits the proxy URL query from the initial request and drops explicit ports from Host/authority construction. Record these fidelity limits. Its printed body decodes UTF-8 with replacement, so the log is not a binary download artifact. Preserve request-stage evidence and errors; successful transport alone does not prove a policy violation or the identity of the responding hop.

See the [upstream usage and interpretation notes](https://github.com/BishopFox/h2csmuggler), [implementation](https://github.com/BishopFox/h2csmuggler/blob/master/h2csmuggler.py) and [Python TLS migration notes](https://docs.python.org/3.12/whatsnew/3.12.html#ssl).
