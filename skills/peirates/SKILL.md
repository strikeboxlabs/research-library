---
name: "peirates"
description: "Attack Kubernetes from a foothold inside the cluster with Peirates: enumerate service accounts, RBAC reach and secrets, then execute the actions they permit. Use after obtaining a pod, token or kubeconfig within an authorized engagement."
---

# Peirates Kubernetes attack

Installed invocation: `/usr/bin/peirates`, version `1.1.28` (Kali package peirates; interactive console).

Read this entire SKILL.md before acting. Require an in-cluster foothold (service-account token, kubeconfig or shell in a pod) from an authorized engagement. Finish with the access actually demonstrated — tokens found, permissions verified, actions taken — not just menu output.

~~~bash
/usr/bin/peirates
~~~

Peirates is menu-driven and builds its option list from what it finds: it enumerates the current service account, reachable API resources, other pods' tokens, node credentials and registry access, then offers the attacks those enable (exec into pods, create privileged workloads, read secrets). Every menu action is a real cluster mutation or read under the engagement's authorization — treat each as logged activity.

Non-obvious ordering: run the enumeration options before attack options, because collected tokens and endpoint data populate the attack menus; a greyed-out attack usually means its prerequisite enumeration has not run. A denied API call documents RBAC boundaries worth reporting even when the attack fails.

References: [project documentation](https://github.com/inguardians/peirates).
