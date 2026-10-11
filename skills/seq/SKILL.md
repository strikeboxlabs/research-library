---
name: seq
description: Generate a bounded integer sequence with GNU seq for local work lists. Use when inclusive endpoints, step direction or counting a generated list can otherwise produce missing or extra records.
---

# Generate a finite local integer list

Read this entire SKILL.md before acting. Confirm GNU coreutils with `seq --version`; choose finite integer bounds, a nonzero step and a fresh `numbers_file`. No conditional resources are required. Finish with the generator's status, bounds and actual record count; a generated list does not establish that later processing succeeded.

Define `first`, `step` and `last` as the selected integers. Keep the result separate from any downstream operation:

~~~bash
umask 077
LC_ALL=C seq "$first" "$step" "$last" > "$numbers_file" &&
wc -l < "$numbers_file"
~~~

The default separator is a newline. The endpoint is included only if the step lands on it. An **illustrative** `seq 0 1 4` produces five records, 0 through 4; `seq 0 2 5` produces three, ending at 4. With one argument, the starting value defaults to 1. A descending range needs a negative step: the omitted step remains positive even when the endpoint is smaller. A direction mismatch can successfully produce an empty file; zero is an invalid step.

Check status before consuming the list. Keep an incomplete result on generator failure separate from accepted input. Prefer these bounded integers to floating-point steps when exact identifiers matter; decimal rounding, formatting and locale can change displayed values. Do not infer a complete external inventory from the highest observed identifier, and do not combine list generation with unbounded service requests. Record downstream success/failure separately if another authorized task consumes the list.

See the packaged [GNU seq manual](https://manpages.debian.org/testing/coreutils/seq.1.en.html).
