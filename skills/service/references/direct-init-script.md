# Use the selected direct SysV interface

Read this entire reference before acting. Require an existing trusted init script, its supported action and the task's actual permission to invoke it. Inspect the script and its sourced defaults/helpers as code before using status or restart; neither is a passive file read. A filename beneath `/etc/init.d` does not prove package provenance, configuration validity or the effective backend.

Set `init_script` to the verified absolute path. For permitted state inspection:

~~~bash
"$init_script" status
status=$?
~~~

Direct scripts need not accept the wrapper's `--version` or `--help`. Establish their interface from the trusted package documentation and acquired script. Under systemd, determine whether this script redirects an action to a managed unit before attributing the result. A sudo grant to this exact script/action does not automatically authorize `service` or `systemctl` as substitutes.

After the service's configuration validator passes and the requested interruption is authorized, perform the supported restart in that permitted context:

~~~bash
"$init_script" restart
restart_status=$?
"$init_script" status
status=$?
~~~

Preserve both results and check the selected service's normal health operation. A failed stop can prevent a start; a failed start can leave the service down. Some implementations return zero when the daemon binary is missing, so an action status alone is insufficient. Follow existing diagnostics before retrying or deleting runtime files.

LSB defines action/status conventions, but the installed script supplies actual behavior. Do not trigger failed logins or modify executable action definitions merely to test a restart. Finish with backend, interruption/result and health or its gap.

References: [LSB init actions](https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/iniscrptact.html), [example Fail2ban Debian script](https://github.com/fail2ban/fail2ban/blob/0.11/files/debian-initd).
