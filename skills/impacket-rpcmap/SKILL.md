---
name: impacket-rpcmap
description: Inspect selected MSRPC interface exposure with Impacket rpcmap from Linux. Use to distinguish interface binding, management discovery and active operation-number calls.
---

# Impacket RPC interface mapping

Check `impacket-rpcmap -h`; upstream may provide `rpcmap.py`. Identify the intended DCE/RPC transport, endpoint and authentication context. An endpoint-mapper address is not interchangeable with an SMB named pipe or an arbitrary service port.

Define `binding` as the scoped RPC string binding, for example `ncacn_ip_tcp:host[135]`, and `interface` as a verified UUID/version string such as `UUID,1.0`. To restrict bind probes to that interface:

~~~bash
impacket-rpcmap "$binding" -uuid "$interface"
~~~

Replace both values from actual endpoint/interface evidence. The reviewed implementation still queries the management interface first; `-uuid` restricts its subsequent UUID bind-probe list. Without `-uuid`, unavailable or inaccessible management information can trigger a fallback across the built-in UUID database, generating more connections than a simple inventory query suggests. Inspect diagnostics and local implementation before using unrestricted discovery.

For authenticated mapping, `-auth-rpc domain/user` and `-auth-transport domain/user` address different layers; omission of the password can prompt. SMB/HTTP transport authentication is not proof that the RPC interface grants the same identity access. Do not lower `-auth-level` just to suppress a failure: it changes authentication/protection semantics.

`-brute-opnums` goes beyond binding: it calls operation numbers with empty request bodies. A method may have side effects even when arguments are missing. Use it only when those method invocations are part of the intended test. `-opnum-max 5` tests **0 through 5**, six numbers, and the default maximum is much larger. Version probing similarly expands the request set.

An accepted UUID bind proves interface availability at that endpoint/time, not permission for every method. `nca_s_op_rng_error` differs from malformed-stub or access errors; a non-fault response still needs protocol-aware interpretation before claiming meaningful method success. Match UUID/version/opnum to its interface specification. Save the binding, identity, options and observed errors; do not infer a universal anonymous capability from one walkthrough's old server.

Documentation reviewed 2026-10-09; Linux execution untested. Case: APT pp. 3–5. Source: [rpcmap implementation and CLI](https://github.com/fortra/impacket/blob/master/examples/rpcmap.py).
