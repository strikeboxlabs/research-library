---
name: hostname
description: Read the Linux hostname and configured interface addresses without confusing container namespace, DNS resolution or address order with network reachability.
---

# Identify the current network context

Read this entire SKILL.md before acting. Use the Debian/net-tools implementation's read-only forms below after checking `hostname --help`; other implementations differ. Finish with the observed name/addresses and their namespace, then verify the intended route separately before choosing a target range.

~~~bash
hostname
hostname -I
~~~

`hostname` without an argument reads the current hostname. `-I` lists configured interface addresses, omitting loopback and IPv6 link-local addresses; output order is unspecified. It does not return prefix lengths, the default route, public/NAT address or all reachable peers. A container address such as **illustrative** `172.18.0.7` does not justify guessing a `/24` or scanning it; establish the interface prefix and authorized range first.

`hostname -i` instead resolves the hostname through the resolver and can return a loopback value or fail. It is a different observation from `-I`. A short hexadecimal hostname is a container lead, not proof: correlate namespace, mount/cgroup and daemon evidence. Names and addresses belong to the current context; they need not identify the underlying host.

Giving a new name as a positional argument changes the hostname when permitted. Do not use that form for identification. See [hostname options and address distinctions](https://manpages.debian.org/bookworm/hostname/hostname.1.en.html).
