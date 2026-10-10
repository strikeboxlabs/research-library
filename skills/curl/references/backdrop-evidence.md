# Backdrop version and route evidence

Require the actual scoped `base_url`, expected hostname routing and fresh `headers`/`body` files. A CMS generator tag suggests the family, not an exact patch. Request the selected packaging file from the same deployment:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' \
  "$base_url/core/profiles/testing/testing.info"
~~~

Check transport status, HTTP response and the .info content together. Illustrative `project = backdrop` and `version = 1.27.1` identify packaging metadata in those bytes, not every live component or vendor patch state. A 404 may reflect removed files or access policy; a 200 HTML login/fallback body is not version evidence. Reconcile available acquired source/release metadata without running the application.

When clean URLs fail but the application exposes query routing, define `route` as an observed internal CMS path or alias and request it with explicit query encoding:

~~~bash
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --get --data-urlencode "q=$route" \
  --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$base_url/"
~~~

Use new output files per request. `q` supplies the routed path; aliases map alternate names onto internal paths, while clean URLs depend on rewrite handling. Thus an admin route via q does not bypass its authorization, and profile aliases depend on the site's generation pattern. Add only the actually required current session cookies. Inspect redirects/login/error bodies before asserting a route or account exists.

An account alias returning 403 can be a candidate when known absent controls differ; a blanket access rule invalidates that inference. A protected administrative route, exact version string and recovered database credential are three independent observations. An authorized code-installation test additionally requires actual install authority and verified artifacts/effects, rather than only a version match.

See [Backdrop clean URLs](https://docs.backdropcms.org/documentation/clean-urls), [aliases](https://docs.backdropcms.org/documentation/url-aliases) and [curl encoding options](https://curl.se/docs/manpage.html).
