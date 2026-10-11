# Review the intended proxy route as configuration

Require the selected server/listener and its complete location, proxy_pass, include/rewrite and authentication configuration. Inspect acquired text first. A response banner differing from the front-end service is a routing lead, not a reconstruction of that configuration.

For a simple prefix location with proxy_pass containing a URI, Nginx replaces the matching normalized location prefix with the configured URI. In an **illustrative** reviewed mapping from location `/reports/` to an upstream URI `/archive/`, the ordinary request `/reports/month.csv` maps to `/archive/month.csv`. Preserve both trailing-slash choices; they are part of the mapping. This is separate from filesystem root/alias handling.

Without a URI in proxy_pass, forwarding instead depends on whether the original or rewritten URI is being processed. Regex/named locations, rewrite break and variable-containing proxy_pass have additional rules; do not apply the simple prefix substitution indiscriminately. Determine the actual selected location before asserting where a request goes.

For try_files, inspect each candidate under the applicable root/alias in order; a trailing slash tests a directory. Only when none exists does the final URI produce an internal redirect, or the selected named location/status apply. A fallback to a PHP handler therefore does not mean every request immediately reaches PHP. Follow the new URI, arguments and location selection. A prefix location matching a script name is not an exact-match location.

When request-body buffering matters, identify client_body_buffer_size and temporary-file directives. A body exceeding the buffer can be written wholly or partly to disk; file lifetime depends on configuration and the actual implementation. A fixture with modified source code does not establish stock cleanup behavior. Keep body-storage observations separate from a demonstrated application result.

Trace access checks on the front end and upstream separately. A reachable service at loopback:port does not prove its listener cannot be reached through another allowed proxy route. Authentication attached to one front-end location is not automatically inherited by every upstream resource. Conversely, a403 or branded error body alone does not prove a file exists, a bypass occurred or that the guessed upstream transformation is correct.

For a task permitting runtime verification, use the existing approved ordinary request, retained headers/body and correlated front-end/upstream logs. Do not broaden it into an invented traversal probe. A status page may show current or last worker requests and can be modified/simulated in a fixture; it is not inherently a complete historical access log. Missing configuration or logs remains an explicit routing uncertainty. Configuration testing and reload do not substitute for the existing live request evidence.

References: [proxy_pass URI rules](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass), [location selection](https://nginx.org/en/docs/http/ngx_http_core_module.html#location), [try_files](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files), [body buffering](https://nginx.org/en/docs/http/ngx_http_core_module.html#client_body_buffer_size), [Apache status semantics](https://httpd.apache.org/docs/2.4/mod/mod_status.html).
