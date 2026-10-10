---
name: targetedkerberoast
description: Request selected Kerberos service-ticket material with targetedKerberoast, including its temporary-SPN mode. Use to distinguish existing-SPN collection from directory writes and verify restoration after an authorized targeted test.
---

# Select existing-SPN or temporary-SPN behavior

Read this entire file before acting. Read [temporary SPN changes](references/temporary-spn.md) before permitting directory writes. Finish with the selected account, complete ticket record, actual directory state and any unresolved cleanup; a generated record is not a recovered password.

The tool can modify `servicePrincipalName` by default for users without one. Use `--no-abuse` when the task only requests material for existing SPNs. Define `script` as the verified installed targetedKerberoast script and inspect `python3 "$script" -h`; options differ across snapshots.

For one authorized account, define `domain`, `user`, `dc_ip`, `account` and private `output_file`. Select an already valid matching Kerberos cache through `KRB5CCNAME`:

~~~bash
umask 077
python3 "$script" -d "$domain" -u "$user" -k --no-pass \
  --dc-ip "$dc_ip" --use-ldaps --request-user "$account" \
  --no-abuse -o "$output_file"
~~~

`account` is the target username, distinct from the authenticating `user`. The installed `--dc-host` option can supply the actual DC name where needed; preserve name/realm/address coherence rather than treating the IP as a universal Kerberos identity. LDAPS requires the deployment's functioning certificate/authentication setup.

Inspect the log and complete output record. `$krb5tgs$` material is an offline-verification artifact, not a raw NT hash or proof of password recovery. Keep encryption type and selected principal with it. No output can mean no eligible SPN, account filtering, failed bind or failed ticket request; use the actual diagnostic to decide.

Do not omit `--request-user` accidentally: broader defaults can select many accounts. `--only-abuse` skips accounts already having SPNs and enables the distinct write-dependent task; it is incompatible with `--no-abuse`. See [upstream usage](https://github.com/ShutdownRepo/targetedKerberoast) for selection/authentication options.
