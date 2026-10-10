# Add and remove one RBCD principal

Use the authenticated `ptc` array from the entrypoint. Define `resource_account` as the computer account receiving the delegation setting and `delegating_account` as the service/computer principal allowed to act toward that resource. Preserve trailing `$` characters through quoting. These roles are easy to reverse.

RBCD stores a security descriptor in `msDS-AllowedToActOnBehalfOfOtherIdentity` on the resource object. Before a write, preserve its exact prior descriptor through the available directory export process as well as the human-readable SID list. Confirm the task permits the selected change and that the authenticating principal can write this attribute.

~~~bash
"${ptc[@]}" -action read_rbcd -delegate-to "$resource_account"
"${ptc[@]}" -action write_rbcd -delegate-to "$resource_account" \
  -delegate-from "$delegating_account"
"${ptc[@]}" -action read_rbcd -delegate-to "$resource_account"
~~~

Compare the actual SID and preserve unrelated entries. Do not interpret an unresolved SID as an absent principal. If the entry already existed before the task, the task does not own its removal. A successful LDAP change establishes directory state; it does not prove a later S4U ticket request or service access succeeded. Those stages also depend on service names, account credentials, ticket policy and the selected impersonated identity.

For a temporary entry added by this task, the selected cleanup action is:

~~~bash
"${ptc[@]}" -action remove_rbcd -delegate-to "$resource_account" \
  -delegate-from "$delegating_account"
"${ptc[@]}" -action read_rbcd -delegate-to "$resource_account"
~~~

`flush_rbcd` clears the entire attribute and is not equivalent to removing this task's entry. Even selected removal can leave an empty descriptor where the attribute was originally absent; compare the complete original state when exact restoration is required. Preserve concurrent authorized changes instead of blindly restoring an old descriptor. A timeout after a write leaves the result uncertain until a fresh read establishes it.

An access-denied write after successful certificate login is an authorization result, not proof that certificate authentication failed. Record both stages without claiming a full delegation test from the write alone. The [upstream action definitions](https://github.com/AlmondOffSec/PassTheCert/tree/main/Python) distinguish selected removal from flushing.
