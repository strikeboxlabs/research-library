# Read the Windows native listener snapshot

Require an already authorized Windows session on the selected owned machine and the native `netstat.exe`. Run there; Linux net-tools switches are not interchangeable.

~~~powershell
netstat.exe -an
$status = $LASTEXITCODE
~~~

Inspect the complete output/status. `-a` includes active TCP connections and TCP/UDP listeners; `-n` retains numeric endpoints. Select TCP `LISTENING` rows using the Local Address column. An **illustrative** local `127.0.0.1:9090` with foreign `0.0.0.0:0` is an IPv4 loopback listener, not a listener on every local interface. UDP rows do not have TCP state.

For available process attribution, use `-ano` and correlate its PID with the same host/time. Windows `-p` selects protocol, whereas Linux net-tools uses it for program/PID display. `-b` requests involved executable components and can fail without sufficient permissions. Missing attribution is not evidence that no process owns the socket.

An HTTP listener attributed to System/PID 4 can reflect HTTP.sys kernel-side handling. That PID does not identify the application worker or prove its effective account is SYSTEM. Correlate the current HTTP request queue and registered URL with the worker process and service identity. `netsh http show servicestate view=requestq verbose=yes` can supply request-queue metadata in an authorized Windows session; its output can include other services and belongs in private evidence. A URL reservation from `show urlacl` records registration permission, not a running handler or its privileges. See [HTTP service state and URL reservations](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-http).

A familiar port number is an application lead, not identification. Preserve selected addresses, state, host and observed time before separately checking the permitted application endpoint. The workstation's loopback and the remote machine's loopback are different locations. A partial or filtered transcript cannot establish all listening ports.

Reference: [Microsoft netstat options and columns](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat).
