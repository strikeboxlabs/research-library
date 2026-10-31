---
name: "cdk"
description: "Evaluate and exploit container and Kubernetes weaknesses from inside a foothold with the zero-dependency CDK binary: recon subcommand plus a library of container-escape and K8s attack routines. Use inside containers the engagement authorizes."
---

# CDK container exploitation toolkit

Installed invocation: `/usr/local/bin/cdk`, version `1.5.6` (release binary cdk_linux_amd64 from cdk-team/CDK).

Read this entire SKILL.md before acting. Require delivery of the binary into an in-scope container and authorization covering both recon and any exploit run. Finish with what evaluate observed and which exploits ran with what result.

~~~bash
/usr/local/bin/cdk evaluate --full
/usr/local/bin/cdk run --list
~~~

`cdk evaluate` is the recon pass (capabilities, mounts, network, service-account tokens, kernel attack surface); `--full` extends collection. `cdk run` executes a specific technique from the built-in list — escapes, K8s API abuse, proxying — each a state-changing action on the container or cluster. The intended order is evaluate, then run the techniques evaluate justified.

The binary is deliberately self-contained for dropper use in locked-down containers; copying it into a target is itself an action on that target and belongs in the engagement log. A technique that fails may still leave partial effects; verify container and node state after any run.

References: [project documentation](https://github.com/cdk-team/CDK).
