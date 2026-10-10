---
name: sucrack
description: Test a bounded local password-candidate list against one selected Linux account through su with Sucrack. Use when no offline verifier is available and worker count, PAM behavior, prompt matching or compile-time options changes the result.
---

# Selected local su password check

Read this entire SKILL.md before acting; reuse complete current context. This is live local authentication through su. Select the authorized OS account, finite candidate set, attempt/time budget and applicable PAM/lockout conditions before running it. Read [build, prompts and option choices](references/build-and-prompts.md) fully if the binary is missing, statistics switches warn, prompts do not match or candidate rewriting is needed. Keep unrelated build work unloaded when the installed CLI already supports the task.

Define `sucrack_bin` as the verified existing binary invocation, `account` as the selected OS account, `wordlist` as the private finite line-based candidate file, `workers` as the chosen concurrency and `log` as a fresh private result file. Inspect `"$sucrack_bin" -h` for this build. Start with one worker when actual account policy permits the selected check; increase only within the task's authentication budget.

~~~bash
umask 077
"$sucrack_bin" -w "$workers" -u "$account" "$wordlist" > "$log" 2>&1
status=$?
~~~

Explicit `-u` avoids the legacy default account of root. `-w` controls workers, not a maximum number of attempts. The finite input limits the unrevised candidate space; duplicates still cause repeated attempts. The command has no demonstrated per-account lockout-safe rate or general time-budget flag. Monitor the authorized budget and stop on policy denial, lockout symptoms, parser stalls or expiry; an interrupted run is incomplete, not exhausted. Confirm stopped parent/worker/su processes before starting a replacement run.

If a password pattern is already supported by acquired evidence, a rule-generated shortlist can reduce work. Prefer an available offline verifier for candidate checks when appropriate to the task; offline recovery and live Sucrack results establish different things. A pregenerated list should not automatically get another rewrite pass: `-r -l ...` can multiply and change the actual online candidate space.

The legacy implementation looks for failure/success strings in su's terminal output. Its `password is:` line is a candidate result, and the log contains that secret. Do not report every zero exit as recovery: help/usage and some errors can also exit zero. Check the full log and build behavior, then, if selected-account access is required, independently authenticate once using the candidate and inspect `id` in that session. Sucrack does not leave an interactive authenticated shell for the worker.

Keep the outcome specific: selected candidate recovered and independently confirmed, selected candidates exhausted under functioning prompt detection, or incomplete/unsupported because of policy, prompts, interruption or build behavior. Application accounts/roles with the same name do not identify an OS account. Do not silently change PAM, enable an account or disable protection to make a check succeed.

See the [upstream Sucrack usage/build guide](https://github.com/hemp3l/sucrack/blob/master/README.md) and [CLI implementation](https://github.com/hemp3l/sucrack/blob/master/src/sucrack.c) for the supported legacy behavior.
