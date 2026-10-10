# Change answers after observed DNS queries

Use this for an authorized DNS-rebinding reproduction with controlled initial/subsequent destinations. Establish the static listener and exact-name rule first. Define the existing `python_bin`, `fakedns_script`, `rules`, `bind_ip` and `dns_port`; preserve the prior test configuration and capture the caller's actual DNS sequence.

The fourth field is a query threshold and subsequent answer. This **illustrative** rule returns the first address twice, then the second:

~~~text
A ^probe\.lab\.test\.$ 192.0.2.10 2%192.0.2.20
~~~

Replace those reserved example addresses with the two authorized destinations. Restart the owned test process after changing its file; it reads rules at startup. The historical CLI uses:

~~~bash
"$python_bin" "$fakedns_script" -c "$rules" -i "$bind_ip" -p "$dns_port" --noforward --rebind
~~~

Check the installed revision rather than relying on that flag alone: the inspected upstream parser accepts `--rebind`, but its matcher applies the fourth-field rule without consulting the flag. Omitting it is therefore not a reliable way to disable changing answers. Remove the fourth field for a static rule.

The matcher tracks queries per rule and source IP, not per HTTP request or browser session. Two initial matching DNS queries reach the threshold; the third matching query from that source receives the subsequent answer. A recursive resolver can combine many callers behind one source IP. Other matching names under a broad regex share that rule's counter; unrelated clients have separate counts. Retries, prefetch, multiple workers and concurrent queries can change timing. Process restart clears this in-memory history.

Comma-separated addresses rotate one address at a time, rather than returning the entire list. Do not confuse that round-robin state with the per-source threshold. The inspected server is threaded; use sequential controlled queries to establish its behavior before interpreting concurrent application traffic.

Direct listener success is only the first test. Resolver positive/negative caches, local zones, browser caching and address checks can prevent a fresh query or reject the answer. Inspect the DNS capture and the actual connection destination; don't infer rebinding from a delayed HTTP hit alone. A configured low TTL is not a guarantee every layer refreshes when expected. Avoid resetting unrelated caches to make a demonstration appear successful.

If the application first validates an address and later connects using another lookup, record both stages and their destinations. HTTP Host, URL hostname and browser Origin are different inputs; changing DNS alone does not establish a routing or CORS bypass. Use a controlled marker at the intended destination to establish access and state the tested conditions. Restore any separately changed resolver policy and stop the owned listener at completion.

See [upstream rebinding description](https://github.com/Crypt0s/FakeDns#dns-rebinding) and [Rule.match, RuleEngine2 and listener source](https://github.com/Crypt0s/FakeDns/blob/master/fakedns.py).
