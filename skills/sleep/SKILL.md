---
name: sleep
description: Use GNU sleep for a bounded delay between selected local checks. Use when fractional durations, interrupted waits or fixed-delay readiness assumptions obscure a task's result.
---

# Delay without asserting readiness

Read this entire SKILL.md before acting. Require a selected finite delay and the check that follows it. Confirm GNU sleep with `sleep --version`; no conditional resources are required. Finish with delay status and the actual subsequent condition, reporting an interrupted wait separately.

For a short local delay:

~~~bash
sleep 0.2
status=$?
~~~

The unsuffixed number is seconds; GNU sleep supports fractional values. Check `status` before dependent work. Scheduling can delay the next command beyond the requested interval. Completion establishes that the delay returned, not that a background process initialized, a file became complete or a service is ready. Check that intended condition explicitly, with a bounded overall retry window if necessary.

Reference: [GNU sleep manual](https://manpages.debian.org/bookworm/coreutils/sleep.1.en.html).
