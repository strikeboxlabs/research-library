# Create or diagnose the selected owned pod

Require trusted kubeconfig/context, approved namespace and the actual requested operation. For creation, require a reviewed local manifest identifying one intended Pod, its exact name, intended image, command, volumes and security settings. `create -f` changes the cluster and can launch the workload; file/YAML validity is separate from permission/admission and runtime behavior. Match any explicit manifest namespace to the selected one. Define `config`, `context`, `namespace`, `manifest` and `pod` from those inputs.

~~~bash
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  --request-timeout=20s create -f "$manifest"
status=$?
~~~

Record the actual result before continuing. AlreadyExists requires inspecting the existing object's identity, not deleting/replacing it automatically. Forbidden distinguishes create from list/get authority. A client dry-run does not test server admission or prove a usable workload; a server dry-run contacts the API but does not persist the resource.

After successful creation, inspect this exact Pod. When Ready is the required runtime condition:

~~~bash
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  wait --for=condition=Ready "pod/$pod" --timeout=60s
wait_status=$?
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  --request-timeout=20s get pod "$pod" -o json
~~~

Creation/Running/Ready answer different questions. On timeout retain phase, conditions and container waiting/terminated reasons; image availability, scheduling and application startup need their specific evidence. Readiness is a point-in-time condition, not proof of every application operation. Retain object UID and requested lifecycle/cleanup state separately.

For an approved diagnostic on an existing owned pod, define `container` as its actual intended container. An **illustrative** ordinary OS-release read is:

~~~bash
kubectl --kubeconfig "$config" --context "$context" -n "$namespace" \
  exec "$pod" -c "$container" -- cat /etc/os-release
status=$?
~~~

This executes cat inside that container; it does not read the host's file or prove host identity. `--` separates remote arguments, without automatically invoking a shell. Select -i/-t only for an intended stdin/terminal session; TTY changes stream behavior. Get/list permission does not establish pods/exec permission. Command-not-found, nonrunning-container, API permission and transport errors leave different prerequisites unresolved.

References: [create](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/), [wait](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/), [exec](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_exec/).
