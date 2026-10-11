---
name: truncate
description: Resize one selected owned regular file with GNU truncate and verify its resulting size. Use for an explicitly requested disposable-file reset or size adjustment without confusing truncation with deletion or log recovery.
---

# Resize the selected file

Read this entire SKILL.md before acting. Require the exact existing regular file and authority to discard or extend its bytes. Preserve required original contents first and coordinate any writer; no conditional resources are required. Finish with status and actual size, reporting discarded bytes as unrecoverable through this operation.

For an explicitly requested reset of one disposable owned file, define `file` as its verified absolute path in a controlled directory, with no unexpected symlink:

~~~bash
truncate --version
truncate --no-create --size=0 -- "$file"
status=$?
stat --format='%F %s %n' -- "$file"
~~~

Verify the object still exists as the intended regular file with size0. No-create suppresses creating an absent path; status alone is not that existence check. Shrinking discards bytes rather than deleting the pathname. Extending to a larger absolute byte size produces a sparse region reading as zeros; it does not restore discarded data. A concurrent writer can change size again or keep an old offset. Do not rerun an acquired rotation script to test this one phase; its other operations need separate scope and results.

Reference: [GNU truncate](https://manpages.debian.org/bookworm/coreutils/truncate.1.en.html).
