# Rails session, report-file and process boundaries

A Rails-like session-cookie name is a framework lead, not proof of a vulnerable version. `curl -I` sends HEAD and supplies headers without the GET body; capture a GET's status/headers/body when comparing rendered content or file bytes. Inspect actual cookie flags. HttpOnly prevents JavaScript reading that cookie through document.cookie; scripts already executing in the site's origin can still use the browser's session for same-origin requests.

## Reproduce the selected form request

Use the actual form route/field names and a session authorized for that task. Define `form_url`, `report_url`, `cookie_jar`, `headers`, `body` and `form_body` as exact scoped endpoints and fresh private artifacts. A legitimately acquired cookie jar is useful for CLI replay; browser session riding does not automatically give curl the browser's HttpOnly cookie.

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 --cookie "$cookie_jar" --cookie-jar "$cookie_jar" --dump-header "$headers" --output "$form_body" "$form_url"
~~~

Require a complete response from the expected session. Select its current authenticity_token using an HTML parser; preserve that exact value in a private `token_file`. Define `path_file` as the exact selected report path/input without an accidental newline. On an observed form with these names:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 --cookie "$cookie_jar" --data-urlencode "authenticity_token@$token_file" --data-urlencode "report_log@$path_file" --dump-header "$headers" --output "$body" "$report_url"
~~~

Use fresh header/body paths for each request. Curl encodes the raw field values once; do not pre-percent-encode them. A valid CSRF token does not grant an application role. Hidden form fields are still client-supplied; hiding the path does not establish a server allowlist. Compare a known accessible report/control to a selected known file before inferring arbitrary access. A 200 login/error page is not that file; status 500 after a process request does not prove the process never ran.

## Browser-only session riding

When the evidence depends on an authorized browser renderer and curl cannot reproduce that session, use the existing browser context and preserve its own responses. Curl cannot execute JavaScript or enforce browser CORS. For a controlled same-origin report test, this **illustrative browser-console procedure** fetches the selected form, obtains its token and requests one selected file; adapt routes/field names to the observed application:

~~~javascript
const formReply = await fetch(formRoute, {credentials: "same-origin"});
if (!formReply.ok) throw new Error(`form status ${formReply.status}`);
const formText = await formReply.text();
const doc = new DOMParser().parseFromString(formText, "text/html");
const token = doc.querySelector('[name="authenticity_token"]')?.value;
if (!token) throw new Error("No current form token");
const fields = new URLSearchParams({authenticity_token: token, report_log: selectedInput});
const reply = await fetch(reportRoute, {method: "POST", credentials: "same-origin", body: fields});
console.log({status: reply.status, url: reply.url, body: await reply.text()});
~~~

Define formRoute/reportRoute as same-origin observed routes and selectedInput as the single authorized file/process input. Work from known response bytes, not a hidden administration link alone. A report/review bot fetching a module is evidence of a visit; substantiate its role through an accessible action/response rather than its user-agent or source IP. If a stored rendering flaw is the activation mechanism, retain that separate input-to-DOM/execution proof before attributing this report action to it. Same-origin script can read the form token; CSRF protection is not a defense against arbitrary script already executing in that origin.

An external module needs a valid JavaScript MIME type and matching browser CORS policy. Anonymous module loading does not need a credentialed wildcard policy; `Access-Control-Allow-Origin: *` cannot authorize a credentialed browser response. CORS is separate from application authentication. Capture browser errors and whether the module actually executed, not merely whether its URL was requested.

## Follow selected file access into source and process behavior

If report_log is passed into a file-opening API, an absolute selected path can reveal whether validation constrains it to reports. `/proc/self/cwd` refers to the **server process opening the path**; it is not the client's cwd and need not be the app root. In a confirmed Rails deployment, paths such as `config/routes.rb` and the actually mapped controller under that cwd are useful selected source reads. Permission, process namespace and changed working directory can invalidate that approach. `/etc/passwd` contains account metadata, not password hashes.

Read the actual route-to-controller-to-input chain. Unqualified Ruby `open(input)` can resolve to Kernel.open, whose leading `|` form launches a process in applicable Ruby versions; File.open and a shadowed/open-uri method are different APIs. Identify the binding/version before applying the leading-pipe conclusion. For a confirmed vulnerable input and authorized execution check, put the single value `|id` in path_file or selectedInput and repeat the request above. Correlate actual identity output with that response/context before proceeding to the selected operational command. A failed child, buffered output or application exception requires separate diagnosis; do not treat all of them as proof of no execution.

The process starts with the service's available authority, not automatically root. A caller-selected command is a deliberate execution request, not an ordinary filename. Long-lived callback commands can leave the HTTP request waiting for stdout/EOF; keep their process, transport and application lifetimes separate. Shell attachment also depends on the installed nc implementation, not on the generic word Netcat.

`redirect_to` does not itself stop a Rails controller's remaining statements; inspect explicit return/exception/callback behavior. A later double-render error can occur after a file/process action. `File.basename(input)` used only for the download filename changes a label, not the preceding file path or subprocess interpretation. Source alone establishes a potential flow, while the selected response/process observation establishes the demonstrated capability.

References: [curl form encoding](https://curl.se/docs/manpage.html#--data-urlencode), [Ruby 2.7 Kernel.open](https://ruby-doc.org/core-2.7.0/Kernel.html#method-i-open), [Rails redirect behavior](https://api.rubyonrails.org/v6.1.7.10/classes/ActionController/Redirecting.html), [proc self/cwd](https://man7.org/linux/man-pages/man5/proc_pid_cwd.5.html), [HttpOnly](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie) and [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).
