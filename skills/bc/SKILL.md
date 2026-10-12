---
name: bc
description: Compare bounded decimal measurements with GNU bc while distinguishing its printed boolean result from command success and rejecting calculator program text as numeric data.
---

# Compare two selected decimal measurements

Read this entire SKILL.md before acting. Require trusted GNU bc, Bash, two selected nonsecret decimal fields and fresh result/error paths. Validate the complete fields, evaluate the fixed comparison, then check both status and output. No conditional resources are required. Finish with the operands, comparison result and diagnostics; a calculator failure is neither comparison branch.

Check `bc --version`. This procedure uses GNU bc's top-level relational-expression extension; another implementation or POSIX-only mode may reject it. Define `left` and `right` as the selected measurements, and `result` and `errors` as fresh files in an owned directory. This illustrative field grammar permits up to 12 integer digits and 9 fractional digits; select narrower bounds when the producer requires them:

~~~bash
if [[ $left =~ ^[0-9]{1,12}([.][0-9]{1,9})?$ &&
      $right =~ ^[0-9]{1,12}([.][0-9]{1,9})?$ ]]; then
  if (
    set -o pipefail
    unset BC_ENV_ARGS POSIXLY_CORRECT
    printf '%s > %s\n' "$left" "$right" | bc -q >"$result" 2>"$errors"
  ); then
    status=0
  else
    status=$?
  fi
else
  printf 'Invalid decimal field\n' >&2
  status=2
fi
~~~

Reject signs, exponent notation, delimiters and program statements under this grammar. Do not pass acquired text as a bc program or filename. `BC_ENV_ARGS` can add options and files before ordinary arguments; `POSIXLY_CORRECT` enables strict POSIX mode. Clearing them inside the subshell confines the change to this selected calculation; no math-library loading is needed for this comparison.

Accept only status0, an empty diagnostics file and one boolean result, 0 or 1. The printed 1 means `left` is greater; 0 means it is not. A successful process printing 0 is not a failed command. GNU bc can recover from diagnostics, so status alone is insufficient. Keep the original fields and units: 0.131 seconds equals 131 milliseconds. A timing threshold does not identify the cause of the measured duration.

See the [GNU bc relational expressions, environment and diagnostics](https://manpages.debian.org/bookworm/bc/bc.1.en.html). Missing bc is a prerequisite gap, not permission to install it or silently substitute another calculator.
