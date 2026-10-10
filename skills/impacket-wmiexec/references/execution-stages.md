# Diagnose the stage before retrying

WMI/DCOM creates the process; SMB retrieves redirected output. A command can therefore execute even when output collection fails. Preserve the command, timestamp, host, authenticating principal and full diagnostic so a retry does not duplicate an operation with side effects.

| Observation | Next decision |
|---|---|
| RPC endpoint or DCOM connection fails | Check the selected host, endpoint mapper and negotiated RPC reachability. An open SMB port alone is insufficient. |
| WMI returns access denied | Verify the account's WMI/DCOM authorization and remote administration policy. SMB login success does not answer this. |
| Process creation succeeds but share access fails | Treat execution as possible; investigate the output channel before running the command again. |
| Output file is temporarily unavailable | The command may still be running; distinguish a sharing violation from a permanently wrong share/path. |
| Text is garbled | Check the remote code page and the client's `-codec`; preserve raw evidence before reinterpreting it. |

`-share` selects the SMB share used for output retrieval; it does not grant access or make an arbitrary share point to the redirected file's location. Keep the selected share's underlying directory consistent with the tool's output redirection. The usual administrative share is part of why a command may execute successfully yet return no readable result.

`-nooutput` skips SMB output collection and cannot support the interactive mode. Use it only for a one-shot command with a separate observable result; silence is not proof of success. `-silentcommand` changes shell wrapping and implies no output in current builds. It is not a generic repair for a failing shell command or missing file evidence.

Normal collection attempts to delete its temporary output file. A dropped connection or interrupted process can leave it behind. Verify only the path associated with this invocation before cleanup; do not wildcard-delete other output files. WMI execution does not create the service used by Impacket psexec, so service deletion is not this client's cleanup method. Closing the client does not undo the executed command or guarantee all child processes stopped.

Where the task needs the remote exit status, explicitly emit or record it from the selected remote shell with correct quoting and verify that evidence. Do not equate the local Python process's exit status with the remote command's exit code.
