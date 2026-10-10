# Interpret the execution stage

| Last successful stage | What remains unproven / useful next check |
|---|---|
| SMB authentication | Share write access and service-control rights. |
| File uploaded | Service creation/start and whether endpoint protection permits that binary. |
| Service created | Process start, RPC/pipe connectivity and command execution. |
| Command output received | Exit status and successful service/file cleanup. |
| Cleanup message printed | Verify the specifically named artifacts when the task requires confirmed restoration. |

Preserve the first relevant error and exact artifacts before retrying. Access denied at a share is not the same as access denied creating a service. Local-account token filtering, service ACLs and remote administrative policy can prevent execution despite valid credentials. Do not disable security controls or switch protocols merely to conceal that failure; select a supported administrative path allowed by the task.

If endpoint protection blocks the uploaded binary, report that execution stage as blocked. Do not assume the service or uploaded file was removed. A broken pipe can occur after remote execution started, so blindly repeating the command may duplicate its effects. Determine the selected command's outcome before retrying a consequential operation.

At completion or failure, inspect the exact service name and share/path recorded for this operation through the approved administration channel. Remove only owned artifacts that remain, after confirming the command/process no longer needs them. Do not delete a service or similarly named executable merely because its name resembles a default. Where cleanup cannot be verified, report the remaining artifact and required owner action explicitly.

A clean local console exit is not a full remote transaction guarantee. Keep authentication, execution and cleanup evidence distinct in the result. See [Impacket service installation/removal](https://github.com/fortra/impacket/blob/master/impacket/examples/serviceinstall.py).
