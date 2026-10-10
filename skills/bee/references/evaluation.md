# Bootstrapped PHP and the process running it

Require the actual installed Bee, a trusted Backdrop installation, its selected site/database access and the requested operation. Define `bee_bin` and `backdrop_root` as in the entrypoint. `eval` (aliases `ev`, `php-eval`) accepts PHP source without opening tags; it performs a full Backdrop bootstrap before evaluating it. Application code can already run during bootstrap. A recovered repository with credentials is not a ready-to-run trusted installation.

## Use the existing bootstrap

For a known node ID, define `nid` as an observed positive integer. In this illustrative example ID 42 must be replaced with the selected real ID:

~~~bash
"$bee_bin" --root="$backdrop_root" eval '$node = node_load(42); if (!$node) { fwrite(STDERR, "Node absent\n"); exit(1); } print $node->title . PHP_EOL;'
~~~

The result is that node's current title in the selected site, not every site's content. A missing node, wrong multisite or bootstrap/database error needs a different next check. Use single shell quotes around PHP `$` expressions so the invoking shell does not expand them. A parse error can expose the supplied code in Bee diagnostics; avoid embedding secrets in code or routine logs.

`php-script` runs a reviewed PHP file after the same bootstrap. Its documented path is absolute or relative to the site root. Define `script` as the selected existing absolute file:

~~~bash
"$bee_bin" --root="$backdrop_root" php-script "$script"
~~~

This includes/executes the file; it is not lint. The reviewed implementation silently returns when the file does not exist, so status/output alone must not stand in for a verified file and expected result. Bee's eval callback catches parse errors but is not a transactional rollback wrapper: earlier effects can survive later failures. Check installed-version diagnostics and resulting state independently.

## Follow a sudo grant into evaluation

Read `sudo -l` and resolve the exact permitted executable, RunAs identity, argument constraints and authentication requirement. A path-only `(ALL : ALL) /actual/path/to/bee` grant permits caller-chosen arguments under that policy; it does not imply NOPASSWD. `secure_path`/`env_reset` do not remove an allowed eval subcommand. A different wrapper or argument pattern can change the conclusion.

When authorized to test that grant, invoke its exact allowed `bee_bin` and selected trusted root:

~~~bash
sudo -- "$bee_bin" --root="$backdrop_root" eval 'system("id", $status); exit($status);'
~~~

`system` prints command output and supplies the child's exit status. This verifies the child identity only when execution and the observed result succeed. The CMS administrator identity is separate from this OS process identity. A root-owned executable called without sudo does not automatically run as root. A literal `get_current_user()` result concerns the PHP script owner, not effective UID.

The source-style alternative `echo shell_exec('id');` returns captured stdout but does not expose an exit code. Empty output can mean an error or a silent command; stderr can go elsewhere. Use the status-aware form for a diagnostic conclusion. CLI PHP and the web worker may have different disabled functions, ini files, users or namespaces. Command execution unavailable in one does not establish the same restriction in the other.

For an explicitly requested shell under the same reviewed grant, define `shell_code` as reviewed PHP source calling `system` with the verified absolute interactive shell path and propagating its status. Then:

~~~bash
sudo -- "$bee_bin" --root="$backdrop_root" eval "$shell_code"
~~~

This runs the chosen shell with the permitted process context; it is an operational action, not a policy inspection. Verify `id` there, do the selected work and exit. A noninteractive transport can lack job control; acquiring a PTY does not change the identity.

## A setuid copy is a separate artifact and execution decision

An authorized lab procedure may explicitly require reproducing a root-owned Bash copy with its setuid bit, rather than merely verifying eval. In the already established privileged context, define `bash_bin` as the verified Bash executable and `bash_copy` as a **fresh** complete pathname in the designated experiment directory. Use the selected paths, not a shared predictable /tmp filename:

~~~bash
test ! -e "$bash_copy" && test ! -L "$bash_copy" &&
  cp -- "$bash_bin" "$bash_copy" && chmod u+s -- "$bash_copy"
stat -c '%n uid=%u gid=%g mode=%a type=%F' -- "$bash_copy"
~~~

Check every status, owner, mode, parent traversal/access and content identity. Copying as root to a new file normally makes root the owner; `chmod u+s` changes a bit, not that owner. A copied shell owned by the ordinary user does not gain root from this bit. Later writes or filesystem policy can clear/ignore it.

Exit the privileged context and, only for the requested reproduction, run the selected copy from the ordinary caller's context:

~~~bash
"$bash_copy" -p -c 'id; id -u; id -ru'
~~~

Illustratively, real UID 1001 and effective UID 0 can coexist; supplementary groups need not become root. Bash `-p` preserves an effective identity already supplied by execution; without it Bash ordinarily drops differing effective IDs. `nosuid`, `no_new_privs`, tracing, interpreter handling and namespaces can change the result, so a displayed `s` or prompt is insufficient. A successful UID-zero result also does not establish unrestricted host authority. Record the artifact and observed identity separately, then clear the experiment's setuid mode/remove only that owned artifact through the established authority and verify restoration. Do not leave it merely because the identity check passed.

See [Bee's evaluation implementation](https://github.com/backdrop-contrib/bee/blob/1.x-1.x/commands/php.bee.inc), [PHP system](https://www.php.net/manual/en/function.system.php), [shell_exec](https://www.php.net/manual/en/function.shell-exec.php), [Bash privileged mode](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) and [Linux exec identity conditions](https://man7.org/linux/man-pages/man2/execve.2.html).
