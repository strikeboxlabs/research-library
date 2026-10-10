# Handoff and recovery

## Service follow-up

For installed Nmap and an authorized service-identification task, omit `-g` and explicitly use the default script mode. Set `output_prefix` to a fresh local result prefix:

~~~bash
rustscan --no-config -a "$target" -p "$ports" -b 100 -t 3000 --tries 2 \
  --scripts default -- -sV -oA "$output_prefix"
~~~

Arguments before `--` belong to RustScan; arguments after it belong to the configured script, normally Nmap. Read the displayed invocation: the default handoff supplies its discovered ports and target. Do not add a conflicting Nmap `-p` or target accidentally. `-sV` probes application protocols; add NSE scripts only when their actual actions fit the task. A custom RustScan script configuration can execute something entirely different.

Separate discovery from follow-up failures. If ports were found but Nmap is missing, exits with an error or rejects an option, retain the port findings. With `discovered_ports` set from the observed numeric list, a direct follow-up is:

~~~bash
nmap -sT -Pn -sV -p "$discovered_ports" -oA "$output_prefix" "$target"
~~~

This connects again and may observe changed state. `-Pn` skips host-discovery gating, not filtering or reachability problems. Nmap's XML/normal output gives service evidence; the earlier RustScan port list alone does not.

## Unexpectedly empty or inconsistent results

| Observation | Useful adjustment |
|---|---|
| File-descriptor errors | Compare `ulimit -Sn` and `ulimit -Hn` with batch size. Reduce `-b`; raising concurrency is not a repair for resource exhaustion. |
| High latency, loss or a fragile forward | Reduce `-b`, increase `-t`, repeat only the uncertain scope with more `--tries`. Compare against one expected port from the same route. |
| Hostname points elsewhere | Resolve and record its addresses; use the intended IP and retain the hostname for later TLS/application tests. |
| Connection succeeds but service probe fails | Consider TLS, protocol negotiation, application access controls and changing listeners before calling it a false-positive port. |

`--ulimit 10000` requests a process file-descriptor limit; it is not a packet rate or scan depth. The requested limit may fail under the account's hard limit. Check the actual diagnostic and effective batch behavior rather than copying a writeup's large value. TCP connect results do not establish UDP coverage; use an explicitly supported protocol mode/tool for that question.

See [speed and accuracy](https://github.com/bee-san/RustScan/wiki/Increasing-Speed-&-Accuracy) and [scan/handoff implementation](https://github.com/bee-san/RustScan/blob/master/src/main.rs).
