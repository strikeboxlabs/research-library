---
name: nginx
description: Inspect and test a selected Nginx configuration, trace HTTP file mappings and distinguish configuration authority from live service state. Use when alternate configs, WebDAV writes, module availability or worker privileges explain unexpected behavior.
---

# Establish the instance and configuration

Read this entire SKILL.md before acting. Require the selected instance and its acquired/reviewed configuration. For proxy URI replacement or mismatched authentication boundaries, read [proxy route review](references/proxy-routing.md) fully before interpreting the route. Use the configuration-test procedure only when its file/module effects are authorized. Finish with the selected configuration, test/live evidence and unresolved mapping or visibility limits.

Define `nginx_bin` as the verified absolute executable for the relevant installation:

~~~bash
"$nginx_bin" -V 2>&1
~~~

Use its version and configure arguments to identify compiled paths and modules. Match these to the service's actual launch arguments; another binary on PATH may have different defaults. `-c` selects a configuration, `-p` changes its path prefix, and `-g` supplies global directives. A prefix is not a filesystem sandbox. Account for service-supplied overrides and follow `include` files before judging a directive in isolation.

## Test the reviewed configuration

Define absolute `config` and `prefix` for that instance, and fresh private `dump`/`diagnostics` files. Inspect unfamiliar configurations as text first: testing can load native modules and open referenced files, including logs. Do not elevate an unreviewed configuration merely to make its test pass.

~~~bash
umask 077
if "$nginx_bin" -T -p "$prefix" -c "$config" >"$dump" 2>"$diagnostics"; then
    test_status=0
else
    test_status=$?
fi
~~~

Retain any known service `-g` overrides when reproducing its test. `-T` (1.9.2+) adds configuration output to `-t` validation; use `-t` when only validation is needed. Neither is a purely textual lint. Protect the dump because included configuration can contain credentials.

| Result | Interpretation and next decision |
|---|---|
| Successful test | This invocation accepted the files currently on disk. It does not show the configuration already loaded by a running master. |
| Unknown directive | Check spelling, nesting/context and the selected binary's compiled/loaded modules. Installing a module is a separate change. |
| Permission or missing-file error | Identify the referenced path, prefix and invoking identity. An unprivileged failure does not establish that the managed service also fails. |
| Some output followed by failure | Keep diagnostics and treat the dump as incomplete evidence. Do not apply a partially validated configuration. |

## Explain a file-serving or WebDAV result

Follow the selected listener, virtual server and location, including inherited directives. With a simple `root /srv/site;`, an **illustrative** URI `/reports/check.txt` maps to `/srv/site/reports/check.txt`. `alias` replaces the matching location portion instead; rewrites and other handlers can change the route. Document root is unrelated to the worker's Unix identity.

The main-context `user` directive controls worker credentials when the master has sufficient privilege; an unprivileged master does not become root through this setting. Confirm actual process identities before attributing access. A root master alone does not prove root workers.

For an existing DAV location, check module availability, enabled methods, destination permissions and request-body temporary storage. DAV is not built by default; `--with-http_dav_module` enables the standard module. PUT writes a temporary file and then places it at the destination, potentially replacing an existing file. `create_full_put_path` defaults to off, so missing parent directories matter. Directory listing via `autoindex` does not enable uploads. Do not infer write access solely from an open port.

## Separate configuration from running state

A bare `nginx -c ...` starts an instance; it is not a configuration test or an implicit reload. A reload signals a master selected through its PID configuration. Use the existing service-management context for an authorized change, and verify its logs afterward: a failed reload can leave the old configuration serving successfully.

For a known decimal TCP `port`, inspect the relevant network namespace:

~~~bash
ss -lntp "sport = :$port"
~~~

Missing process details can reflect visibility restrictions. A listener confirms a socket, not which file mapping, worker identity or HTTP method is active. Finish with selected binary/configuration, test outcome, live-instance evidence and the unresolved request-stage check; avoid changing the service just to establish these distinctions.

See [CLI switches](https://nginx.org/en/docs/switches.html), [core directives](https://nginx.org/en/docs/ngx_core_module.html), [HTTP path mapping](https://nginx.org/en/docs/http/ngx_http_core_module.html#root), [DAV behavior](https://nginx.org/en/docs/http/ngx_http_dav_module.html) and [reload handling](https://nginx.org/en/docs/control.html).
