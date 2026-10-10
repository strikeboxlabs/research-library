# Interpret and finish the selected relay test

Retain separate evidence for the inbound protocol/identity, chosen target, authentication result and post-authentication operation. A challenge-response record is bound to its negotiation; it is not a reusable NT hash or a recovered password. A hash capture can succeed while relaying that exchange fails.

| Stage | What an incomplete result means |
|---|---|
| Listener starts, no client reaches it | Check routing, binding and the authorized trigger. This says nothing about the target's relay protections. |
| Client connects but does not authenticate | Inspect the client's protocol/authentication behavior; a TCP connection is not an NTLM exchange. |
| Target rejects authentication | Check the actual protocol response, account context and applicable signing, binding or extended-protection requirements. Do not diagnose every rejection as an invalid password. |
| Target authenticates but action fails | The principal may lack rights for that action. Preserve authentication success separately from access denial. |
| Local interactive console appears | This exposes an authenticated protocol client; it is not automatically a Windows shell or administrator session. |

The selected destination protocol determines the action implementation. In the SMB implementation, `-i` takes the interactive client branch. Default noninteractive behavior can attempt remote-registry/hash operations, and executable/command options have additional effects. Changing an `smb://` target into `ldap://`, HTTP enrollment or another protocol is not merely changing transport: review that protocol's write/collection defaults first.

SMB signing requirements, LDAP protections and HTTP extended protection operate at different stages. An unsigned-service observation is a prerequisite lead, not proof that every originating protocol/identity can be relayed. Historical source patches for RPC, IPv6 or fixed challenges are not assumptions to carry into a current installed build. Identify the actual build before interpreting a failure.

For the entrypoint's interactive SMB branch, connect locally to the port printed by the tool, for example with an installed TCP client and the actual port. Commands such as `get` retrieve data and `put`/`rm` change files; select them according to the authorized task. Do not assume every console command is read-only.

Stop the listener after the bounded test and verify its sockets closed. Ending the relay process does not undo actions already performed through its authenticated sessions. Record and clean up only artifacts created by the selected action, preserving unrelated service and directory state. An interrupted test with an ambiguous write needs a fresh state check before retrying.

See the [SMB action implementation](https://github.com/fortra/impacket/blob/master/impacket/examples/ntlmrelayx/attacks/smbattack.py) and [protocol options](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py).
