---
name: kubeletctl
description: Read the pod inventory of one approved owned Kubelet node with kubeletctl. Use when node-local pod data is being mistaken for an API-server namespace or full cluster inventory.
---

# Read one node's pod inventory

Read this entire SKILL.md before acting. Require a trusted executable, explicit owned node/port and an approved isolated diagnostic transport. Finish with actual response status, node scope and observed pod metadata; a rendered table or zero exit alone is insufficient.

Check `kubeletctl version` and `pods --help`. The reviewed v1.7 transport skips TLS server verification even when CA options are supplied; it also does not attach kubeconfig bearer tokens in this request helper. Do not infer verified server identity or authenticated API access from its CA/config flags. If verified HTTPS is required, use an approved client that actually validates the node certificate, or a version whose transport behavior has been independently verified.

For this specifically approved node diagnostic, define `node` and `port` explicitly. Avoid implicit workstation kubeconfig loading:

~~~bash
kubeletctl --ignoreconfig --server "$node" --port "$port" --raw pods
~~~

`pods` issues GET `/pods` to that Kubelet. Raw output preserves the response for status/body inspection. A403/401 or malformed response is incomplete inventory, not an empty node. In v1.7 the formatted path decodes a PodList without first proving HTTP success and its namespace flag does not filter this result. Read the actual namespace/name/container fields; this endpoint covers one node, not every pod in the cluster. Missing entries and time differences remain gaps.

Keep the capture private because pod metadata can contain sensitive configuration. Report only the required names/counts and scope. Inventory does not grant container execution, API-server permissions or node filesystem access. Resolve denied access through the owner's configured identity, preserving the diagnostic.

See [pod handler](https://github.com/cyberark/kubeletctl/blob/v1.7/cmd/proxy/pods.go), [config selection](https://github.com/cyberark/kubeletctl/blob/v1.7/cmd/root.go) and [transport behavior](https://github.com/cyberark/kubeletctl/blob/v1.7/pkg/api/requests.go).
