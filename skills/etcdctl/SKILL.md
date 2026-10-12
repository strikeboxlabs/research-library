---
name: etcdctl
description: Write and verify one selected nonsecret configuration key in an owned etcd v3 fixture. Use when a successful key write needs to be distinguished from a consumer applying the resulting configuration.
---

# Change one configuration key

Read this entire SKILL.md before acting. Require the selected owned endpoint, configured authentication/TLS, one exact nonsecret key/value and permission for its downstream effects. Follow the write/readback procedure; finish with both statuses, the observed value/revision and any requested consumer result. Missing consumer evidence remains unresolved.

Select `endpoints`, `key` and `value` explicitly. Inspect the existing exact key first and identify consumers watching its namespace. A harmless-looking string can trigger a file rewrite or service restart. This workflow uses a controlled fixture key; it does not broaden into namespace discovery or secret retrieval. Keep configured credentials private and retain TLS verification.

~~~bash
ETCDCTL_API=3 etcdctl --endpoints="$endpoints" --write-out=json get -- "$key"
~~~

After confirming the intended baseline and overwrite effects:

~~~bash
ETCDCTL_API=3 etcdctl --endpoints="$endpoints" put -- "$key" "$value"
put_status=$?
ETCDCTL_API=3 etcdctl --endpoints="$endpoints" --write-out=json get -- "$key"
get_status=$?
~~~

`put` replaces an existing value. `OK` and zero status establish the store operation; they do not establish rendered-file correctness or application health. An omitted value is read from stdin. Quoting and `--` keep the selected operands intact.

JSON returns RPC bytes encoded as base64: decode the returned exact key/value before comparing; retain the revision when concurrent writers matter. A successful empty get is absence, not an empty stored value. Readback is a later observation, not an atomic guarantee that nobody overwrote this write. Diagnose a nonzero status from stderr before retrying.

See the [upstream v3 client reference](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md) for the installed version's API selection and output format. Confirm that version during the controlled Linux pass.
