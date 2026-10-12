# Inspect the current Kubernetes identity's rules

Use a known cluster API, its trusted CA and a provisioned identity. A service-account directory or environment variable is a clue about context, not independent proof of cluster identity. Require the intended namespace; OS UID and Kubernetes identity are different.

Define `api` as the verified HTTPS API base without a trailing slash, `ca_file` as its trusted CA file, and `auth_headers` as a private file containing the provisioned Authorization header. Define `request_json`, `headers` and `body` as private task files. Put a reviewed SelfSubjectRulesReview in `request_json`, replacing the illustrative namespace below with the intended one:

~~~json
{"apiVersion":"authorization.k8s.io/v1","kind":"SelfSubjectRulesReview","spec":{"namespace":"example-namespace"}}
~~~

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --cacert "$ca_file" --request POST \
  --header "@$auth_headers" --header 'Content-Type: application/json' \
  --data-binary "@$request_json" --dump-header "$headers" --output "$body" \
  --write-out 'status=%{http_code}\n' \
  "$api/apis/authorization.k8s.io/v1/selfsubjectrulesreviews"
status=$?
~~~

This POST evaluates the caller's rules; it does not grant permissions or create a workload. A CA variable which is never passed to curl does not verify TLS. Keep transport status, HTTP status and the complete response before parsing. Authentication failure, Forbidden, API incompatibility and an empty successful rule set are distinct results.

Read `status.incomplete` and `status.evaluationError` alongside `resourceRules` and `nonResourceRules`. Do not replace a missing status/rule field with an empty list and report no access. Preserve API group, resource/subresource, verbs and any resource-name restriction together. An incomplete review can contain valid returned rules while omitting others. For one required operation, use the cluster's specific self-access review or an administrator's effective-policy review; do not treat this rules summary as an authorization engine for other users.

When separately reviewing an acquired pod manifest, connect each container's `volumeMounts[].name` to `spec.volumes[].name`. The volume source's host path does not reveal the container's mount path by itself. Include the selected container, mount path, subpath and read-only setting before claiming where data is visible. A privileged flag alone does not establish a successful host-file read. Complete with the reviewed identity/scope, returned rules and unresolved mapping, rather than executing a workload to prove an inference.

See [Kubernetes authorization reviews](https://kubernetes.io/docs/reference/access-authn-authz/authorization/), [review response fields](https://github.com/kubernetes/api/blob/master/authorization/v1/types.go) and [volume/mount semantics](https://kubernetes.io/docs/concepts/storage/volumes/).
