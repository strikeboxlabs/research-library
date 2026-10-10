# Read lockout policy for a selected user

Use the selected OpenLDAP connection: `dc_fqdn` is the verified DC DNS name, `bind_upn` the authorised bind identity and `base_dn` its observed domain naming context. The examples require working StartTLS trust and prompt via `-W`; use the established GSSAPI context instead when that is the required authentication method.

Use the established authenticated connection and domain `base_dn`. Define `user_dn` as the exact DN of the selected user. Query the domain defaults and the user's resultant password-settings object separately:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$base_dn" -s base '(objectClass=*)' lockoutThreshold lockoutDuration lockOutObservationWindow
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$user_dn" -s base '(objectClass=*)' sAMAccountName msDS-ResultantPSO
~~~

If `msDS-ResultantPSO` returns a DN, set `pso_dn` to that exact value and inspect its settings:

~~~bash
ldapsearch -LLL -x -ZZ -H "ldap://$dc_fqdn" -D "$bind_upn" -W -b "$pso_dn" -s base '(objectClass=*)' msDS-LockoutThreshold msDS-LockoutDuration msDS-LockoutObservationWindow
~~~

**Illustrative:** domain `lockoutThreshold: 0` alongside a selected user's resultant `msDS-LockoutThreshold: 5` means the domain-default observation did not settle that user's policy. Zero disables count-based lockout for the policy in question; it does not establish unlimited retries across applications or permission to try credentials. An omitted/denied attribute is not zero. If no resultant PSO is returned, establish successful object/attribute visibility before falling back to domain defaults; keep unresolved visibility as a limitation.

Preserve the DN, queried DC, bind identity and collection time with policy values. This reads configured policy, not current lockout state or the success of a particular authentication attempt. Microsoft's [resultant-policy documentation](https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-aduserresultantpasswordpolicy) explains the user/group precedence behind `msDS-ResultantPSO`.
