---
name: kubectl
description: Query selected Kubernetes pods/namespaces and self-permissions with explicit kubeconfig context, or perform approved single-pod creation and container diagnostics. Use when Forbidden, namespace scope or pod readiness is mistaken for cluster-wide authority.
---

# Select the cluster identity and resource scope

Read this entire SKILL.md before acting. Require trusted kubectl, a trusted authorized kubeconfig and intended context/namespace. Read [pod operations](references/pod-operations.md) fully for selected pod-status inspection, approved manifest creation or an in-container diagnostic. Finish with the requested resource result, actual context/scope and status; API acceptance, runtime readiness and command execution are separate evidence.

Inspect acquired kubeconfig as text before using it: credential exec plugins and referenced files can cause local execution/exposure. Use the intended trusted identity, retaining CA verification. Define `config`, `context` and `namespace` as the approved values. Check installed client help/version, then query that namespace:

~~~bash
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  --request-timeout=20s get pods -o wide
status=$?
~~~

An empty successful list is limited to this namespace/identity/time. Forbidden records a specific identity, verb, resource and scope; it differs from an unreachable API or unauthenticated request. Local file access does not establish cluster permissions, and OS UID differs from API identity. Retain the exact diagnostic.

If the task explicitly requires the namespace catalogue, `kubectl --kubeconfig "$config" --context "$context" --request-timeout=20s get namespaces` queries that cluster-scoped resource. Seeing a namespace does not grant pod read/create/exec within it. Stay with the intended namespace rather than retrying across unrelated namespaces to obtain permission. A package/profile label does not establish the running node's runtime version.

For an owned identity's effective permission question, use the same trusted context and explicit namespace:

~~~bash
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  --request-timeout=20s auth can-i --list
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  --request-timeout=20s auth can-i list pods
~~~

Retain returned rules, yes/no, warnings and errors separately. A failed rules review or an incompleteness warning is not a complete rights catalogue. Check the specific requested verb/resource (and subresource when applicable) rather than treating list/get/create as interchangeable. A yes describes authorization for that request; admission, quota and workload runtime can still reject a later mutation. It does not create a service account, elevate the identity or establish permission in another namespace. Review a hostPath/hostNetwork manifest's intended node effects separately from API authorization. See [self-permission checks](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_can-i/).

References: [kubeconfig selection](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/), [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/).
