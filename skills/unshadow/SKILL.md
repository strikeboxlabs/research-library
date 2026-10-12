---
name: unshadow
description: Join existing owned passwd and shadow snapshots into a private offline audit record while preserving passwd identity fields. Use when checking account-record alignment or preparing a selected administrative audit input.
---

# Join an existing account snapshot pair

Read this entire SKILL.md before acting. Establish the already acquired authorized passwd/shadow pair from the same host and capture interval, plus a fresh private output path. No additional resources are required. Finish with the actual join status and record-alignment findings; report a missing input or implementation instead of substituting a live protected-file acquisition.

Define `passwd_snapshot` and `shadow_snapshot` as existing absolute input paths and `joined` as a nonexistent absolute output path in a private directory. The installed John/Openwall `unshadow` helper takes passwd first and shadow second, even though its implementation reads the shadow input first. Keep account hashes and output out of logs:

~~~bash
umask 077
(
  set -o noclobber
  unshadow "$passwd_snapshot" "$shadow_snapshot" > "$joined"
)
join_status=$?
printf 'unshadow status=%s\n' "$join_status"
~~~

An unsuccessful command can leave a partial output file; preserve it as incomplete evidence and choose a fresh path for a retry. Do not treat file existence as success. Review the record structure locally without printing the password/hash field into the report.

The join matches usernames exactly and replaces a nonempty passwd password field with the matching shadow password field. It keeps the passwd UID, GID, GECOS, home and shell fields; it does not retain shadow password-aging fields. An unmatched passwd record or an empty passwd password field can be emitted unchanged. Therefore exit status zero does not prove that every account obtained a matching shadow value. An `x` placeholder left in output is not a recovered password, and locked values such as `!` or `*` are not automatically usable credentials.

Confirm that the selected inputs are from the same account namespace and capture interval. Investigate duplicates and missing users in the source records before drawing alignment conclusions; the current implementation stores duplicate shadow names such that the later matching record can win. Keep originals unchanged rather than silently resolving conflicts in the audit output. Joining representations neither decrypts passwords nor validates any login.

Report only completion status, selected input identity and the requested alignment conclusion, with unresolved records counted or named as authorized. Subsequent password recovery, protected-file collection or credential use is a separate task.

See [Openwall's implementation](https://github.com/openwall/john/blob/bleeding-jumbo/src/unshadow.c) for parsing and matching details when installed behavior differs.
