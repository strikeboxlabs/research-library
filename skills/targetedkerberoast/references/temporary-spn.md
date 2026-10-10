# Run a temporary-SPN test and verify state

Use this branch only for an explicitly selected account whose SPN write is in the authorized task. Confirm its exact DN, current full `servicePrincipalName` value set and effective write permission. An existing-SPN ticket request needs no temporary addition. Generic write rights do not mean every attribute write will satisfy directory policy.

Preserve a fresh LDAP read of the selected object's DN and SPN values on the same DC. For an environment supporting SASL GSSAPI over trusted LDAPS, define `dc_fqdn`, `target_dn` and `before_file`:

~~~bash
ldapsearch -LLL -Y GSSAPI -H "ldaps://$dc_fqdn" -b "$target_dn" -s base \
  '(objectClass=*)' distinguishedName servicePrincipalName > "$before_file"
~~~

Confirm the object was actually returned. In the reviewed implementation, the temporary path is for an account initially having no SPNs. It uses a fixed temporary SPN and replaces the attribute with that value, then replaces it with an empty value set after ticket collection. This is not a transactional add/delete of only an owned value. Concurrent changes, interrupted execution or errors can leave an unexpected state.

With the entrypoint's identity/cache/output variables already set, the selected write-enabled operation is:

~~~bash
python3 "$script" -d "$domain" -u "$user" -k --no-pass \
  --dc-ip "$dc_ip" --use-ldaps --request-user "$account" \
  --only-abuse -o "$output_file"
~~~

Verify the log's write, ticket and cleanup stages separately. Repeat the exact LDAP base-object read afterward and compare the complete SPN set with the pre-state, even when the tool prints success. SPN uniqueness conflicts, insufficient attribute rights and KDC errors are different failures. Do not retry a write-enabled run until ambiguous state is resolved.

If only the known temporary value remains and no other change occurred, use the deployment's authorized directory editor to remove that exact owned value, then reread. If concurrent values exist or the prior state is uncertain, reconcile with the object owner; never replace the whole attribute with an empty set blindly. Preserve the unresolved difference as a failed cleanup rather than reporting the ticket artifact as complete success.

Restoring the attribute does not retract already issued tickets or erase audit events. Keep the temporary test's time, DC, selected account, output and post-state associated without recording credentials. See [upstream mutation and cleanup implementation](https://github.com/ShutdownRepo/targetedKerberoast/blob/main/targetedKerberoast.py).
