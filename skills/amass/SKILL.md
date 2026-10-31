---
name: "amass"
description: "Map externally-visible assets for an authorized domain with OWASP Amass enum, choosing passive collection or explicitly authorized active techniques. Use when subfinder's source set is insufficient or source attribution and storage in an output database matter."
---

# Amass asset enumeration

Installed invocation: `/usr/bin/amass`, version `5.1.1` (Kali package amass; subcommands, `amass enum` is the enumeration entrypoint).

Read this entire SKILL.md before acting. Require one in-scope domain and explicit permission for the collection mode. Finish with the enumeration output and the mode actually used; naming a domain's assets is separate from testing them.

Define `domain` as the authorized domain and `out` as a new output path. Passive collection only queries third-party sources; amass 5.x `enum` has no `-o` flag — capture stdout:

~~~bash
/usr/bin/amass enum -passive -d "$domain" > "$out" 2>"$progress"
~~~

Amass is a long-running background stage, not a pipeline step to wait on: full passive runs commonly take tens of minutes to hours. Launch it detached and let the rest of the chain proceed on other enumerators (subfinder), merging amass results in when it finishes. Two behaviors make interruption costly: findings are emitted at completion, so a killed run leaves an empty output file (incomplete coverage, not absence), and stderr carries a continuous progress-bar flood — always redirect it to a progress log as shown rather than mixing it into results.

`-active` adds techniques that touch the target's own infrastructure (DNS resolution from claimed territory, bruteforce and alterations) — run it only under authorization that covers those interactions. Amass writes structured results and by default a local database that support later queries; that weight is the trade-off for deeper source collection and source attribution per finding.

A passive run is bounded by the sources Amass reaches at that moment; an empty section is unqueried coverage, not absence. Resolve and probe results separately (httpx skill) and keep scope checking on every discovered name, including wildcard-derived and historical ones.

References: [user guide](https://github.com/owasp-amass/amass/blob/master/doc/user_guide.md).
