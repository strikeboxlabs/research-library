---
name: initctl
description: Emit one approved Upstart application event and verify the affected existing job. Use when event completion, task lifetime or the wrong system/user manager makes a service result ambiguous.
---

# Deliver the selected Upstart application event

Read this entire SKILL.md before acting. Require a running Upstart daemon, its verified installed client, the selected manager and authority for the specific existing application event's effects. Review all matching existing job definitions and their trusted inputs before emission. All instructions are inline. Finish with command status and the actual application/task result; unavailable manager access or unknown event effects leaves the action blocked.

Define `initctl_bin` as the verified executable, `event` as the approved application event and `job` as the known affected job. Establish system versus user/session context, including inherited UPSTART_SESSION and selected client connection options. A legacy initctl binary on a different init system does not supply a running Upstart manager.

~~~bash
"$initctl_bin" --version
"$initctl_bin" version
"$initctl_bin" show-config
"$initctl_bin" status "$job"
~~~

Check each result. `show-config` lists event conditions, not the complete executable job contents; inspect the actual matching configuration and dependencies. An event can start or stop several jobs. Directory/file ownership alone does not determine the daemon's execution identity, and a writable job is executable input. Do not rewrite a privileged job to test an event.

Only after its existing effects are understood and approved:

~~~bash
"$initctl_bin" emit "$event"
status=$?
"$initctl_bin" status "$job"
~~~

Without `--no-wait`, emission waits for affected services to run/stop and tasks to finish; a long-running task can keep the client waiting. `--no-wait` establishes queuing instead. Select the worker's bounded observation policy without interpreting interruption as rollback or automatically emitting again. Event environment arguments can alter job behavior; omit them unless part of the established contract.

A finished one-shot task can return to stop/waiting. That state is not alone proof it failed or never ran. Verify its intended ordinary artifact/log/application result separately; successful delivery to no matching job is not that result. Preserve original errors and manager context before deciding whether a retry is justified.

References: [client commands, event waiting and manager connections](https://manpages.debian.org/jessie/upstart/initctl.8.en.html), [job conditions and task behavior](https://manpages.debian.org/jessie/upstart/init.5.en.html).
