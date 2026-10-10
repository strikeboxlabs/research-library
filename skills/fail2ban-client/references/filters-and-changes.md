# Matching, actions and selected changes

## Why an event did not cause the expected action

Set `log_sample` to an acquired small log sample and `filter_file` to the matching filter configuration. This helper tests text matching without banning a client:

~~~bash
fail2ban-regex "$log_sample" "$filter_file"
~~~

Read matched, ignored and missed counts together with timestamp parsing. A regex match in an offline sample does not prove the running jail reads that file, uses the same filter or sees enough recent failures. A journal backend needs the corresponding journal input/match semantics. Keep malformed timestamps and an incorrect time zone separate from a nonmatching failure expression.

Set `action` to one exact name returned by `get "$jail" actions`:

~~~bash
fail2ban-client get "$jail" action "$action" actionban
fail2ban-client get "$jail" action "$action" actionunban
~~~

These retrieve command templates; they do not execute them. Trace parameters, tags and helper paths to the installed action configuration. A jail can run multiple actions, and a successful firewall update does not guarantee a WHOIS/email notification succeeded. Conversely, a failing notification need not mean the ban failed. Review custom scripts and interpolation as executable configuration; do not paste untrusted log/WHOIS content into a privileged shell to reproduce them.

## Unban one selected client

After establishing the intended jail, client address and authorization, define `client_ip`:

~~~bash
fail2ban-client set "$jail" unbanip "$client_ip"
fail2ban-client status "$jail"
~~~

Verify the address left the jail's list and that the actual action removed its restriction. A different jail or independent firewall rule can still block the client. Continued matching failures can immediately ban it again; fix the cause rather than repeatedly unbanning. Use `set "$jail" banip "$client_ip"` only when a deliberate manual ban is the task, not as a diagnostic read.

## Load a corrected configuration

~~~bash
fail2ban-client -t
fail2ban-client reload "$jail"
fail2ban-client status "$jail"
~~~

Use the same explicit `-c`/`-s` deployment context when required. Stop if configuration validation fails. A jail reload is narrower than restarting the daemon. Check the installed release before adding `--restart` or `--unban`, which change the operation's effects. Runtime `set` changes and edited configuration have different persistence; record and verify the intended state instead of assuming a runtime change survives restart.

See [regex tester](https://github.com/fail2ban/fail2ban/blob/master/man/fail2ban-regex.1), [jail configuration](https://github.com/fail2ban/fail2ban/blob/master/man/jail.conf.5) and [client commands](https://github.com/fail2ban/fail2ban/blob/master/man/fail2ban-client.1).
