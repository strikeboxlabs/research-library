# Remote member-host acquisition and the SAM result

Use when the approved task requires **live** credential-store acquisition from one selected member host, rather than parsing existing hives. Establish the host's member/DC role, selected authentication, admin/share/service access, private output and permitted acquisition effects. The standard workflow can enable/start RemoteRegistry, save temporary hive files, retrieve them over SMB and later restore service state/remove owned artifacts. It is not a read-only query or a one-account SAM selector.

The reviewed standard remote CLI can also attempt an NTDS stage; `-skip-security` skips SECURITY/LSA parsing but does not select SAM-only or suppress every remote acquisition step. No generic `-just-sam-user` flag is assumed. If the requested scope excludes those additional accesses, acquire the approved hive snapshots through an allowed method and use LOCAL parsing in the entrypoint instead. This is a scope/implementation distinction, not a reason to omit the supported live workflow.

For an explicitly approved selected-host acquisition with those stages permitted, define `domain`, `operator`, `member_fqdn`, `output_prefix` and existing authentication. Known password login prompts normally:

~~~bash
umask 077
impacket-secretsdump "$domain/$operator@$member_fqdn" -skip-security -outputfile "$output_prefix"
~~~

For an existing CIFS-compatible ticket, use the cache's actual hostname/SPN identity:

~~~bash
export KRB5CCNAME="$cache"
impacket-secretsdump -k -no-pass "$domain/$operator@$member_fqdn" \
  -skip-security -outputfile "$output_prefix"
~~~

Use supported `-target-ip`/`-dc-ip` addressing controls only while preserving the hostname identity. A service ticket can permit SMB/registry access without granting DRSUAPI replication. On a member server, a later NTDS error does not invalidate a separately completed SAM extraction, and successful SAM output does not establish directory dump success. Check stages independently.

Inspect `${output_prefix}.sam` and acquisition/cleanup diagnostics. Preserve host/store and `username:RID:LM:NT:::` mapping; a local Administrator NT hash is not the domain Administrator credential just because the name/RID is familiar. A machine-account or NetNTLM artifact is not the selected local user's NT hash. If a subsequent known-account login is specifically requested, select that actual identity and service, not every recovered record.

Complete with the recovered SAM records for the approved host, unresolved stages and verified RemoteRegistry/temporary-file cleanup. Do not claim a partial remote run acquired every store. No VSS/replication fallback should broaden scope automatically. See [CLI/stage ordering](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py) and [RemoteOperations acquisition/cleanup](https://github.com/fortra/impacket/blob/master/impacket/examples/secretsdump.py).
