---
name: inveigh
description: Capture a bounded selected HTTP NTLM authentication exchange with cross-platform Inveigh. Use when an application sends outbound integrated authentication and identity, listener exposure or challenge-response interpretation needs evidence.
---


# Select the capture surface before starting Inveigh

Read this entire SKILL.md before acting. Require the authorized sending application, owned listener/route and bounded capture window. Finish with actual protocol/principal and retained challenge-response evidence, then stop the listener; a capture is neither a recovered password nor a successful relay.

Use Kevin Robertson's C# cross-platform Inveigh, not its legacy PowerShell script. Define `inveigh_bin` as the installed Linux executable and inspect `"$inveigh_bin" -?`. An installed DLL may instead require a verified `dotnet Inveigh.dll` invocation. Do not guess the image path/build. The Linux build lacks the Windows packet sniffer and relies on supported listeners; running it with elevation does not enable that sniffer.

For one explicit HTTP capture through an already arranged route, define `listen_ip`, `http_port`, `out` (an existing private directory), and `minutes`. On a build supporting these options:

~~~bash
"$inveigh_bin" -ListenerIP "$listen_ip" -IPv6 N \
  -HTTP Y -HTTPPorts "$http_port" -HTTPAuth NTLM \
  -HTTPS N -SMB N -LDAP N -Proxy N \
  -DNS N -LLMNR N -MDNS N -NBNS N -DHCPv6 N -ICMPv6 N \
  -RunTime "$minutes" -RunCount 1 -FileDirectory "$out" -FileOutput Y
~~~

This selects capture without name-service spoofing; bare defaults enable additional protocols. Inspect the startup summary and real listener sockets rather than assuming the disabled list fits every build. A low port may need the environment's approved binding privileges. Do not alter firewall or system security to conceal a bind failure. `-Inspect Y` is observation-only mode and can suppress the active behavior needed for a capture; it is not an equivalent successful test.

Trigger only the selected authorized request separately. Preserve timestamp, HTTP endpoint, account/domain and complete NTLMv2 challenge/response record from the actual output file. A proxy/tunnel can make the peer look like loopback, so IP alone cannot identify the sender. An **illustrative** `NTLMv2 captured for [EXAMPLE\svc_monitor]` proves that principal negotiated with this listener; it does not establish the destination's relay protections or current NT hash.

If the app reports an error while Inveigh captures a response, keep those two results separate. No capture can mean routing, listener, trigger or the client's authentication policy; it is not proof the credential is invalid. Offline candidate checking and live relaying are different tasks: a saved NetNTLMv2 line is not replayed as an NT hash. End the process and verify the listener closes; protect output and avoid repeating or expanding the sending identities merely to obtain a hit.

See [upstream cross-platform usage/options](https://github.com/Kevin-Robertson/Inveigh) and [current argument handling](https://github.com/Kevin-Robertson/Inveigh/blob/master/Inveigh/Program.cs).
