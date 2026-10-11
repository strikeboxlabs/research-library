# Recover access to a trusted shared repository

Use this branch when normal Git inspection of a known trusted repository fails with `detected dubious ownership`. Establish the absolute repository path, owner and provenance first. For acquired evidence, retain the original and use the isolated inspection context; an ownership exception allows Git to read repository configuration and is a trust decision.

Distinguish this error from filesystem access denial and from a failed global-config write. A message about locking `.gitconfig` concerns the selected configuration file, not permission to read repository objects. Changing the home directory does not grant filesystem access, and a shared temporary home mixes unrelated configuration.

For the verified trusted `repo`, limit the exception to each intended read command:

~~~bash
git -c safe.directory= -c safe.directory="$repo" -C "$repo" rev-parse --show-toplevel
status=$?
~~~

The empty value clears inherited exceptions for this invocation; the following exact path selects this repository. Confirm zero status and the expected top-level path before proceeding with the selected inspection task. Repeat these command-scope options on subsequent Git reads that require the exception. They do not persist settings or change ownership. An incompatible installed Git needs version-specific documentation, not an assumed successful recovery.

Avoid wildcard trust or a broad directory-tree exception for a single repository. A local repository setting cannot authorize its own trust: this option requires protected system, global or command scope. If ordinary permissions still deny access, report the missing access/provenance condition rather than changing owners or running privileged Git as a diagnostic.

Completion records the exact trusted path, successful scoped read and any remaining object/history limitations. Follow the selected task's full reference; resolving ownership does not establish repository completeness or authorize executing hooks, checking out content or contacting remotes.

See [Git configuration scopes and safe.directory](https://git-scm.com/docs/git-config) for installed-version differences.
