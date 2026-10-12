# Review a tarfile restore wrapper without extracting

Require the acquired wrapper, exact permitted interpreter, its package/patch provenance and the intended restore policy. Read the source as text; invoking its help or importing it can execute startup code. Keep the archive unopened for this source review.

Trace the backup-name validation, actual base directory, selected archive, staging-directory creation and extract/extractall call. Help text can name a different directory from the constant the code uses. An allowlist on the archive filename or restore tag says nothing about its members. `isfile()` and `exist_ok=True` do not prove a fresh, exclusively controlled destination. Follow exception handling and any subsequent success message or deployment step.

Identify the explicit filter, instance/class extraction_filter and errorlevel together. Filters arrived in Python 3.12 and may be backported; the default changed to data in 3.14. Filter availability alone does not establish patch status. The data filter restricts filesystem features but provides neither publisher authentication nor comprehensive resource limits. Consult the [deployed-version tarfile documentation](https://docs.python.org/3/library/tarfile.html#extraction-filters), not assumptions based only on a version banner.

An aborted extraction can leave earlier files in place; extractall does not roll them back. With errorlevel zero, some refusals can be logged and skipped while processing continues. Thus a wrapper's completion label does not prove every intended member was restored. Preserve the existing result and diagnostics before planning a retry; do not automatically extract into the same staging tree or delete an ambiguous directory.

For remediation, require a patched interpreter, a fresh controlled destination, explicit member policy and external resource limits; use ordinary privilege for initial processing. Verify the expected artifact set before a separately authorized deployment. Do not weaken a filter or fall back to fully_trusted to make an unknown backup pass.

Finish with the wrapper's input/destination/filter/error map, evidenced runtime provenance and remaining deployment or partial-state gaps. This review establishes what the code permits; it does not claim a successful restore or reproduce an archive exploit.
