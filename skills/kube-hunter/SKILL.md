---
name: "kube-hunter"
description: "Hunt for Kubernetes cluster weaknesses with kube-hunter from inside or outside the cluster, probing for exposed dashboards, kubelet ports and known misconfigurations. Findings are leads about cluster posture, not confirmed compromise."
---

# kube-hunter cluster hunting

Installed invocation: `/usr/local/bin/kube-hunter` (pipx package kube-hunter).

Read this entire SKILL.md before acting. Require an authorized cluster target and a chosen vantage: outside the cluster network or inside it. Finish with the vulnerability list and the vantage used; an outside scan cannot see inside-only exposure paths.

~~~bash
/usr/local/bin/kube-hunter --quick
~~~

`--quick` limits to a subset of checks; from a compromised pod use `--pod` so hunters run with the in-cluster network and service-account view, which finds exposure an outside scan cannot. The `--list` output names the individual hunters so a finding can be traced to the check that produced it.

kube-hunter sends probes to cluster endpoints (kubelet, API, dashboards) and reports known-weak configurations: an open read-only kubelet port, an unauthenticated dashboard, exposed etcd. Each is a reported weakness for the operator — a lead to verify, not an exploited path, and none of it establishes what an attacker could reach beyond the probe itself.

References: [project documentation](https://github.com/aquasecurity/kube-hunter).
