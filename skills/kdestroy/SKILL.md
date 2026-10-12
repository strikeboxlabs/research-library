---
name: kdestroy
description: Destroy one selected MIT Kerberos credential cache after an owned task. Use when default-cache selection, collections or a later client session make cleanup ambiguous.
---

# Remove the selected task cache

Read this entire SKILL.md before acting. Require the installed MIT implementation and exact owned cache selected for cleanup. No conditional resources are required. Finish with destruction status and a subsequent inspection of that same cache; changing a shell variable is separate from removing credentials.

Check local help and identify the cache type. For one task-owned FILE cache, define `cache_path` as its absolute path. Inspect its principal/service metadata before selecting it for deletion:

~~~bash
klist -c "FILE:$cache_path"
kdestroy -c "FILE:$cache_path"
destroy_status=$?
klist -c "FILE:$cache_path"
inspection_status=$?
~~~

Retain both statuses and diagnostics. A successful destruction followed by a missing-cache result supports cleanup of this selected cache. A remaining readable cache, permission error or wrong implementation needs investigation; do not treat every failed inspection as proof of deletion.

Bare `kdestroy` selects the default cache, potentially through KRB5CCNAME. `-A` destroys a collection and `-p` selects a principal within one; neither is needed for the FILE task above. Inspect collection membership before choosing broader cleanup.

Switching KRB5CCNAME for another task does not require destroying an unrelated default cache. Destruction does not unset that variable, revoke long-term keys, remove copies or end already authenticated application sessions. Record the consumer/session state separately.

Reference: [MIT cache selection and destruction](https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/kdestroy.html).
