---
name: postconf
description: Inspect or change selected parameters in an owned Postfix configuration. Use when server identity, trusted relay clients or local-recipient routing explains an SMTP failure.
---

# Select the Postfix configuration and mail stage

Read this entire SKILL.md before acting. Require trusted installed Postfix tools and the intended instance's configuration. Read [local delivery](references/local-delivery.md) fully when interpreting recipient rejection or a mailbox result. For a change, establish the exact parameter/value, write authority and recovery path first. Finish with configuration, activation and application evidence separately.

Define `config_dir` as the selected instance's absolute configuration directory. Query named parameters rather than dumping unrelated secret-bearing maps:

~~~bash
postconf -c "$config_dir" mail_version myhostname mydestination mynetworks \
  local_recipient_maps local_transport mail_spool_directory
~~~

Check status and warnings. `-c` selects that directory's main.cf; it does not prove which instance a running process uses. `-d` returns defaults rather than configured values. Resolve parameter references before claiming their effective expansion. master.cf overrides require separate inspection. Retain distribution package/patch context when a historical release matters.

For an authorized edit, define `parameter` and `value` as the reviewed single setting. Preserve main.cf and its ownership/mode in a fresh protected backup using the existing approved configuration-management context. Then:

~~~bash
postconf -c "$config_dir" -e "$parameter = $value"
postconf -c "$config_dir" "$parameter"
~~~

Stop on errors or unexpected values; reconcile concurrent edits before restoring anything. The disk edit does not reload the daemon. Use the selected instance's approved validation/activation path, then verify the mail operation. Postfix's `check` may create missing directories and is not purely read-only lint. Do not widen relay trust or disable recipient checks to make one message pass.

See the packaged [postconf command](https://manpages.debian.org/bookworm/postfix/postconf.1.en.html) and [parameters](https://manpages.debian.org/bookworm/postfix/postconf.5.en.html).
