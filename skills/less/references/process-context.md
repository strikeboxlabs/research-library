# Shell commands in the actual pager context

Use when a permitted program enters less and the task calls for diagnosing or exercising its process-execution feature. Require the actual pager implementation, calling program/identity, inherited secure-mode settings and explicit authority for the selected child operation. Do not remove secure mode or change system pager configuration to make a historical example work.

Ordinary less is an interactive application, not just a text renderer. Its `!command` feature invokes a shell, `!` alone opens an interactive shell, and `v` can invoke an editor. These features operate with the pager's actual process context, which may differ from the parent if the launcher dropped identity. Newer versions may selectively re-enable otherwise disabled features with `LESSSECURE_ALLOW`; check the installed configuration, not a guessed default.

Within the identified less prompt, a bounded authorized identity query is:

~~~text
!id
~~~

This is typed into less, not Bash or the parent's menu. Use the verified identity command if PATH lookup differs. Preserve numeric real/effective IDs and relevant context; a sudo-launched parent does not prove a root pager. Percent signs and `#` in less shell commands can expand to current/previous filenames; avoid placing untrusted names into a constructed command.

If the selected task authorizes an interactive Bash child and that executable exists:

~~~text
!/bin/bash
~~~

Inside it use `id`, `id -u` and `id -ru` before attributing authority. Bash can drop a differing effective UID without privileged mode; the shell must be observed, not inferred from a prompt. Exit back to less, then `q` back to the caller and complete/cancel that caller's selected operation. A child exit does not necessarily end the parent's report UI.

| Observation | Meaning / next decision |
|---|---|
| Shell command disabled | This execution feature is blocked by this build/configuration; record it rather than changing protections. |
| Child stays at originating UID | The parent may have dropped identity for the pager; useful negative evidence for this branch. |
| Child has requested elevated UID | Evidence for that context/action, still bounded by namespace/capability policy. |
| Pager exits or no interactive prompt appears | Short input, launcher options or terminal context can leave this branch untested. |

`LESSSECURE=1` ordinarily disables shell, editor, preprocessor and other features. The entrypoint's literal-text command sets secure mode deliberately for source inspection; that task should not execute shell commands. Keep local report output, shell execution and a privileged parent as separate observations. Apport's CVE-2023-1326 fix, for example, changes who runs sensible-pager rather than disabling less globally.

See [upstream less shell/security semantics](https://github.com/gwsw/less/blob/master/less.nro.VER) and the [Apport identity-drop patch](https://github.com/canonical/apport/commit/e5f78cc89f1f5888b6a56b785dddcb0364c48ecb) for unexpected parent/child differences.
