---
name: sshd
description: Check a reviewed OpenSSH server configuration and run a temporary owned foreground daemon. Use when effective Match policy, listener scope, host keys or single-connection debug mode explains a server test.
---

# Check and observe an owned SSH daemon

Read this entire SKILL.md before acting; reuse complete current context. Require the verified installed daemon, a reviewed task configuration/host key, approved listener/account scope and the necessary existing administration rights. Check configuration before starting, retain listener/login evidence, then stop the owned daemon; a parse result alone is not a live server result.

Define `sshd_bin` as its verified absolute executable, `config` as the existing absolute reviewed configuration and `effective` as a fresh private output. For its supported test modes:

~~~bash
"$sshd_bin" -t -f "$config"
~~~

Only after zero status:

~~~bash
umask 077
"$sshd_bin" -T -f "$config" > "$effective"
~~~

`-t` checks configuration/key sanity; `-T` prints effective configuration and includes these checks. For a selected connection's Match rules, add the installed supported `-C` values for user, source address/host and local address/port. Unmatched defaults do not establish that account's effective policy. Test under the same intended permissions and configuration/arguments as the eventual daemon.

For a temporary local test, require the reviewed configuration to select only the approved loopback listener on an unused high port, its intended host key and the already provisioned test account. Review Include/Match, authentication and forwarding policy rather than inheriting the system daemon's defaults. Keep its process/session distinct from an existing service:

~~~bash
"$sshd_bin" -D -e -f "$config"
~~~

`-D` stays in the foreground and ordinary connection handling can fork; `-e` sends logs to stderr. `-d` is different: it stays foreground, does not fork and handles only one connection. A debug daemon disappearing after one client is not necessarily a crash. `-p` overrides Port settings but a port embedded in ListenAddress can override it; inspect actual listener scope instead of assuming a high port makes a daemon local.

Use a known authorized client and retain host-key verification, actual accepted identity and the requested operation's result. A listening socket proves neither login permission nor forwarding authorization. Unreadable host keys, missing runtime directories or a bind conflict need their specific prerequisite resolved; do not weaken file modes or replace another service. Stop the owned foreground process and check listener/child-session state before completing. Consult [OpenSSH daemon modes](https://man.openbsd.org/sshd) and [server configuration](https://man.openbsd.org/sshd_config) for installed-version policy differences.
