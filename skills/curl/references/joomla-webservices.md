# Joomla version, webservice access and configuration disclosure

Use for a scoped Joomla HTTP assessment where its hostname/base path and webservices deployment are known. Preserve host routing and the actual request's authentication context. An XML manifest, administrator login page and API response establish different things. Joomla's [CVE-2023-23752 advisory](https://developer.joomla.org/security-centre/894-20230201-core-improper-access-check-in-webservice-endpoints.html) identifies affected 4.0.0–4.2.7 installs and the 4.2.8 fix; backports, disabled routes or a stale manifest can change applicability.

Define `base_url` as the scoped Joomla application URL without a trailing slash, including any subdirectory. Use fresh private `headers`/`body` files for each request:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' \
  "$base_url/administrator/manifests/files/joomla.xml"
~~~

Require transport completion and an actual Joomla XML manifest before interpreting its version element. A 200 login/fallback page, blocked manifest or copied file is not an exact running-version observation. Keep this GET's body/status together. For an IP-backed virtual host, use the intended URL hostname with the established `--resolve` routing; editing `/etc/hosts` is not necessary for this selected request. `-k` affects TLS verification, not HTTP access checks, and does nothing useful for an ordinary HTTP URL.

## Compare the actual configuration endpoint

Where this specific information-disclosure check is in scope, choose fresh captures for an unauthenticated baseline without query/authentication, then a second request with the known query:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --dump-header "$baseline_headers" --output "$baseline_body" \
  --write-out 'status=%{http_code}\n' \
  "$base_url/api/index.php/v1/config/application"
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --dump-header "$test_headers" --output "$test_body" \
  --write-out 'status=%{http_code}\n' \
  "$base_url/api/index.php/v1/config/application?public=true"
~~~

Define all four capture paths before running. Check each exit/status separately and ensure inherited cookies, headers or curlrc have not turned this into an authenticated request. Do not add PATCH or a credential merely to make a failed disclosure check succeed. The historical `public` query targets an access-control error; public in the URL is not an authorization assertion.

In affected Joomla 4 configuration responses, inspect the JSON:API `data` list and each item's `attributes`. Configuration entries can appear as separate items such as `host`, `user`, `password`, `db` and `dbprefix`, not a single top-level credentials object. Preserve values exactly in private evidence; PDF wrapping or a regex over the rendered page can corrupt them. Follow returned pagination only for the selected configuration evidence, with the same scope/authentication, before claiming completeness. A partial page missing a key is not evidence the deployment lacks that key.

**Illustrative interpretation:** an unauthenticated control is rejected while the query returns real configuration fields. That establishes disclosure for this route/context, not arbitrary administrator access or command execution. A 200 containing an `errors` object or fallback HTML is not disclosure. A deny response can reflect patching, route/plugin availability, proxy policy or authentication; retain it and narrow the finding rather than claiming a specific patch solely from the status.

Treat database `host`/`user`/`password`/`db` as that application's connection configuration. `localhost` is evaluated on the application server, not the worker, and its database client may use a socket. A database username is not automatically a Joomla superuser, SSH account or OS root. Any separately authorized credential-reuse check needs the selected endpoint/account and its own authentication/identity evidence; a database value alone is only a candidate. Avoid verbose traces or reports which unnecessarily reproduce the secret.

Finish with route, method/authentication, version evidence, compared captures, actual exposed fields and incomplete/pagination conditions. Remediation can include updating and rotating exposed credentials, but is a separate authorized action. The [Joomla mitigation notes](https://docs.joomla.org/J4.x:Webserver-level_mitigations_for_CVE-2023-23752) explain why a blocked public query can be deployment policy. The pinned [config route](https://github.com/joomla/joomla-cms/blob/4.2.6/plugins/webservices/config/config.php), [JSON view](https://github.com/joomla/joomla-cms/blob/4.2.6/api/components/com_config/src/View/Application/JsonapiView.php) and [configuration model](https://github.com/joomla/joomla-cms/blob/4.2.6/administrator/components/com_config/src/Model/ApplicationModel.php) resolve historical response shape.
