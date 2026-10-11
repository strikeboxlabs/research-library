---
name: df
description: Inspect space reported by the filesystem containing a selected Linux path with GNU df. Use when rounded disk figures, the wrong mount or fixed-column parsing obscure a capacity observation.
---

# Inspect the selected path's filesystem capacity

Read this entire SKILL.md before acting. Select an existing path in the intended mount namespace and confirm GNU coreutils with `df --version`. No conditional resources are required. Finish with the filesystem, mount, units, available space and status; a failed lookup is not zero capacity.

Define `path` as that selected path. Request explicit fields and byte units:

~~~bash
LC_ALL=C df -B1 --output=source,fstype,size,used,avail,pcent,target -- "$path"
status=$?
~~~

Read stderr and `status` before accepting the row. The path selects its containing filesystem, not the size of that file or directory. A mount namespace or nested mount can change which filesystem answers. The source and target columns may contain spaces; fixed whitespace-column extraction is not a general pathname-safe parser.

`-h` gives rounded powers-of-1024 units for human inspection; `-H` uses powers of 1000. Explicit `-B1` avoids environment-dependent block units. Available space is a filesystem observation, not proof that this account can write a requested file: permissions, read-only policy, quotas and concurrent allocation remain separate. When a write reports inode exhaustion, a separate `df -i -- "$path"` answers that capacity question. Do not infer service health or perform a write merely from positive space.

See the packaged [GNU df manual](https://manpages.debian.org/bookworm/coreutils/df.1.en.html).
