# Inspect deleted-object evidence

Use the selected OpenLDAP connection: `dc_fqdn` is the verified DC DNS name, `bind_upn` the authorised bind identity and `base_dn` its observed domain naming context. The examples require working StartTLS trust and prompt via `-W`; use the established GSSAPI context instead when that is the required authentication method.

A normal AD search hides deleted objects. Using the same verified TLS/bind context, inspect RootDSE `supportedControl` and the naming context before changing the query. For the domain's usual Deleted Objects container:

~~~bash
deleted_base="CN=Deleted Objects,$base_dn"
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$deleted_base" -s one -E '!1.2.840.113556.1.4.417' -E pr=500/noprompt '(isDeleted=TRUE)' objectGUID isDeleted isRecycled sAMAccountName lastKnownParent msDS-LastKnownRDN
~~~

The critical Show Deleted control has no value. `!` prevents silently ignoring an unsupported control. This changes visibility, not permissions: an empty result or denied container is not proof that no deletion occurred. Confirm the naming context/container and delegated list/read rights; a custom group named "AD Recycle Bin" does not by itself establish those rights or that the feature is enabled.

Select the returned deleted DN or correlate the retained `objectGUID`; a display name is not unique and may no longer be retained. To inspect one object, repeat the control with `-b "$deleted_dn" -s base '(isDeleted=TRUE)'` and explicitly requested identity/custom attributes. Use an LDIF-aware reader for encoded DNs and binary GUIDs; do not paste a base64 GUID into a text equality filter.

Retained fields depend on deletion state, schema and visibility. Recycle Bin retention is finite. Show Deleted includes tombstones/deleted objects but excludes recycled objects; when that distinction matters and the server supports it, Show Recycled (`1.2.840.113556.1.4.2064`) includes all three. Neither control recovers garbage-collected data. Consult Microsoft's [control comparison](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/4b8f2a0e-9ea6-4be3-b639-4b019948c568) and [object lifecycle](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/538ec135-1465-4266-bb0a-777924f02846) for missing-field cases. A recovered historical value is evidence of that object, not proof of another account's current credentials.
