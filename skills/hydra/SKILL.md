---
name: hydra
description: Run scoped online authentication tests with THC Hydra. Use to choose protocol modules, control candidate ordering and concurrency, and distinguish valid credentials from protocol or response-classification errors.
---

# Test the intended authentication path

Read this entire file before acting. Read [HTTP forms and attempt control](references/forms-and-attempts.md) for form authentication, multiple accounts or retry planning. Establish the authorized accounts, candidate set and attempt budget before sending logins; finish with verified protocol outcomes and actual coverage.

Hydra performs online attempts, unlike offline hash tools. Inspect `hydra -h` and `hydra -U SERVICE` for the installed module. A supported service name does not guarantee the build includes its dependencies. Choose the real protocol/port: SSH, FTP and an application's web form are different authentication paths.

For one selected account, set `target`, `port`, `login`, `candidate_file` and a fresh private `results` path. The candidate file contains only the agreed passwords, one per line:

~~~bash
umask 077
hydra -l "$login" -P "$candidate_file" -t 1 -W 3 -w 10 -f \
  -s "$port" -o "$results" "$target" ssh
~~~

`-t 1` selects one concurrent connection; `-W` spaces connections per worker and `-w` limits response waiting. These are not an account-lockout policy. `-f` stops after a reported success for a host; it does not verify the application's subsequent authorization. Use the appropriate service instead of `ssh` only after reading its module help.

Uppercase `-L`/`-P` read lists; lowercase `-l`/`-p` supply one value. `-C` uses explicit login:password pairs rather than the Cartesian product of two lists. Results can contain plaintext credentials; avoid verbose attempt logging when it adds no needed evidence.

A reported credential must match the intended account/protocol and be verified within the task's budget. Authentication failure, connection timeout, unsupported negotiation and account lockout are separate results. Stop on lockout/rate-limit indications and resolve them before continuing; do not turn transport failures into rejected password candidates. Preserve the tested subset when interrupted.

Use the [project guide](https://github.com/vanhauser-thc/thc-hydra) and [CLI option definitions](https://github.com/vanhauser-thc/thc-hydra/blob/master/hydra.c) for installed-release differences.
