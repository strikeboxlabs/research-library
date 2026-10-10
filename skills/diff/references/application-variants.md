# Compare application variants and follow the changed capability

Use for acquired application archives/source trees whose changes may expose a different operational task. Required inputs are corresponding extracted roots, acquisition provenance and the selected application context. A tree named main is not automatically a trusted/pristine baseline; dev is not automatically the running build.

Inventory the archives and extract only to separate working directories with the appropriate archive controls. Match inner roots before comparing. Use SKILL.md's recursive summary with the older/reference variant on the left and selected variant on the right, then its unified-file comparison for relevant source/configuration. Preserve status 1 as ordinary differences and status 2 as trouble/partial coverage. A bare `diff main dev` compares immediate files but can miss changes in common subdirectories.

Follow the capability across files, rather than collecting isolated added lines:

- Command/route registration: which name becomes selectable, with which argument grammar?
- Handler: what input reaches a file, shell, database or other effect?
- Guards: is the check tied to an authenticated identity, a command-specific secret, a role or just a string?
- Path/process context: working directory, normalization, containment, execution user and actual read/execute permissions.
- Deployment: listener/interface, configured port and evidence that this variant is running.

For example, a new `file` command registered in one Go file may call a handler in another that obtains cwd, joins it with a user path, checks a password, stats/opens the file and emits scanner lines. `filepath.Join` performs path cleanup; it does not enforce a directory boundary. A hardcoded function password does not automatically grant chat administration or an OS login. Trace guard order and returns, and preserve the relevant secret privately rather than embedding it in reusable guidance.

A changed port plus a `127.0.0.1` listener may mean the variant is available only from that host/network namespace. Confirm the actual listener and application interface separately. Source ownership, archive date or a filename can guide selection, but cannot identify the live process's UID or current build on their own.

For an authorized selected-file procedure, verify the running command's help/grammar, actual working directory and permitted path, then request one expected text artifact. Distinguish argument/guard failure, missing path, denied read and returned content. Line-by-line chat output may add prefixes or truncate on a scanner error; collect completion evidence before treating it as the full file. Recovered key material still needs format inspection and separately authorized login verification.

Read surrounding branches even when a diff highlights only one guard: an earlier return can prevent the effect, while an error path can hide partial output. Default bindings, environment variables, startup options and later configuration can override a source constant. Finish with the actual supported new behavior, source conditions and deployment evidence, identifying any unresolved runtime assumption.

References: [GNU diff behavior](https://man7.org/linux/man-pages/man1/diff.1.html), [Go path joining](https://pkg.go.dev/path/filepath#Join), [Go line scanning](https://pkg.go.dev/bufio#Scanner).
