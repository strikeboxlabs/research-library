---
name: ln
description: Create one selected symbolic link in an owned Linux working tree with GNU ln. Use when target text, link-parent resolution or an existing destination directory can change the resulting object.
---

# Create the selected link without replacing an entry

Read this entire SKILL.md before acting. Require the intended target, fresh link pathname beneath a verified owned parent and permission to create that entry. All task instructions are inline. Finish with command status, the actual symlink and its stored target; creation does not prove the referent exists or is readable.

Confirm ln --version for GNU coreutils. Define target as the intended existing owned absolute file/directory and link_path as a new absolute entry, with no trailing slash:

~~~bash
ln -s -T -- "$target" "$link_path"
status=$?
~~~

Check status/stderr before using it. -s creates a symbolic link; default ln creates a hard link. -T treats the final operand as the exact entry instead of creating a link inside an existing directory. A collision remains an error; inspect it rather than adding -f or deleting it. Parent-directory access/filesystem restrictions are distinct from a missing referent.

Inspect the resulting entry's type and stored link text with the selected metadata/readlink procedure. An absolute target is interpreted in the resolving process's namespace; a relative target is resolved from the link's parent, not the creation shell's working directory. Moving a relative link can therefore change its referent. A successful symbolic-link creation can leave a dangling link; check the intended referent separately without following an unexpected target.

When cleanup is required, remove only this tracked link entry, without a trailing slash, after verifying its identity; deleting a symlink entry differs from deleting its target. No recursive replacement is part of this task.

Reference: [GNU ln manual](https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html).
