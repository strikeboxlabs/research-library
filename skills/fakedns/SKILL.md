---
name: fakedns
description: Serve scoped synthetic DNS answers with Crypt0s FakeDns and reproduce query-count rebinding. Use when resolver caches, regex rules or per-client counters obscure which address a caller actually receives.
---

# Supply a controlled DNS answer

Read this entire SKILL.md before acting. Select the Crypt0s implementation, rules and intended listener; finish with captured queries/answers and their scope. For changing answers after a query threshold, read [rebinding and cache interpretation](references/rebinding.md) fully first. A configured rule or startup message does not prove that the application used that answer.

Define `python_bin` and `fakedns_script` as the existing trusted interpreter/script, `rules` as a reviewed configuration file, and `bind_ip`/`dns_port` as an available address and UDP port on the intended test interface. Inspect that implementation's help:

~~~bash
"$python_bin" "$fakedns_script" -h
"$python_bin" "$fakedns_script" -c "$rules" -i "$bind_ip" -p "$dns_port" --noforward
~~~

This runs a foreground UDP server. Defaults can expose every interface on port 53; explicit binding and `--noforward` avoid unrelated upstream lookups. A port collision or missing bind permission is a failed listener, not a DNS result. Using a high port requires the querying client/forwarder to select it explicitly. Do not replace the system resolver merely to start this test.

Each rule has a type, Python regex and answer; for example this **illustrative** exact-name rule:

~~~text
A ^probe\.lab\.test\.$ 192.0.2.10
~~~

The inspected parser supplies a trailing dot and matches case-insensitively from the start; anchor both ends and escape literal dots. Rules are tried in file order. Broad earlier matches can hide later rules. Use the actual record type: an A rule does not supply an AAAA answer. Prefer an explicit address over `self`, whose hostname lookup can select an unintended interface.

Send the intended query directly to this listener with an already available DNS client, then test through the application's resolver separately. Retain name, type, client source, time and answer. A matching log entry does not identify the browser/application behind a recursive resolver. With `--noforward`, an unmatched name gets a negative response; it is not proof the public name does not exist. Stop the owned listener when the test ends.

See [configuration](https://github.com/Crypt0s/FakeDns#fakedns) and [parser/listener implementation](https://github.com/Crypt0s/FakeDns/blob/master/fakedns.py) for installed-revision differences.
