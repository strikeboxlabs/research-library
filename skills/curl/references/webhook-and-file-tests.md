# Keep outbound behavior, authentication and source transformations separate

Use the actual API request construction from SKILL.md, preserving private status/headers/body captures. A token returned inside JSON `message.x-access-token` is a response-body value, not a response header. A later request may send it as `x-access-token`; another route may instead require `x-api-key`. A valid login, a decoded role and authorization to create a webhook are different observations. Reuse the established schema rather than guessing token location from a label.

For an authorized webhook test, define a unique controlled object/marker and an owned listener reachable from the service, with the documented action, URL and ordinary method. Save the returned identifier. Confirm creation separately from invocation and callback receipt. Observe the callback's request line, headers, body, connection source and marker before claiming SSRF reachability. A successful HTTP file-server response can also expose its whole served directory; use a dedicated owned tree.

If source evidence suggests an unvalidated method field is inserted into the outbound request, use an inert marker test against the owned listener first. The following is **illustrative JSON request content**, requiring the application's actual surrounding schema:

~~~json
{"url":"http://owned-listener.example:8000/marker","method":"GET\r\nCLI_MARKER\r\n"}
~~~

Construct it with a JSON serializer and deliver that JSON as the outer API's body. Do not pass the injected inner value to curl's `--request`: curl is the API client, while the vulnerable application constructs the second request. Save actual callback bytes. A 400 from the API can coexist with an emitted callback/effect; inspect state before retrying. CRLF injection in an outbound request line is not by itself proof of HTTP desynchronization/request smuggling or acceptance by another protocol. A rejected `gopher:` URL says little about method validation on accepted HTTP URLs. Redis delivery additionally depends on framing, authentication and receiver policy; no callback body is not proof of no command execution.

## Follow the exact path/field transformation

For an authorized selected path test, preserve the literal URL with `--path-as-is` when dot-segment normalization matters, capture the response, and compare a known control. NGINX alias traversal can arise when a location prefix lacks the intended trailing slash while its alias names a directory. A 403 for a directory does not rule out accessible child files. A status alone is weak evidence; compare expected file content without broadening the path scope. See [NGINX alias mapping](https://nginx.org/en/docs/http/ngx_http_core_module.html#alias).

For a JSON file-reading endpoint, trace validation and transformation in order. Rejecting literal `../` before deleting spaces can admit `.. /` which becomes `../` later. Requiring a substring such as `log` does not confine the resolved file to a log directory. Send only one scoped owned fixture/control pair using the actual `file` field, then verify which bytes returned. Trimming leading/trailing whitespace alone does not fix embedded-space normalization or directory confinement; validate the final canonical path and allowed root, including symlink/race policy. `/proc/self/environ` concerns the file-serving process's namespace and initial environment, not automatically the host or all current variables.

A profile update that removes only password/CSRF keys and mass-assigns the remainder can admit an unintended field if the deployed model does not guard it. Reproduce only the approved account-field change with its current cookies/CSRF token; verify stored state and a selected resulting action, then restore it when intended. A changed form response or later token claim is insufficient alone. Treat recovered source as a hypothesis about the deployed handler, not confirmation that every route/build matches it.
