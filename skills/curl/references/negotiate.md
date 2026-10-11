# Request the authorized Negotiate resource

Require an authorized HTTP resource, an existing usable credential cache, correct service hostname/realm and a curl build supporting GSS-API/SPNEGO. Check `curl --version`; Windows SSPI support uses a different credential-provider context from Linux GSS-API. A challenge advertising Negotiate does not itself prove which underlying mechanism succeeded.

Define `krb_config` as the established absolute Kerberos configuration, `cache` as the existing cache representation supported by its provider, and `url` as the selected resource URL containing its actual service hostname. Define `headers` and `body` as fresh private files. For a Linux GSS-API build and existing MIT file cache, use the provider's `FILE:` prefix in `cache`:

~~~bash
umask 077
KRB5_CONFIG="$krb_config" KRB5CCNAME="$cache" \
  curl --negotiate --user : --silent --show-error \
  --connect-timeout 5 --max-time 30 --dump-header "$headers" \
  --output "$body" --write-out 'status=%{http_code}\n' "$url"
status=$?
~~~

`--user :` activates curl's authentication code; its empty username/password are not a new login or anonymous-access request. The GSS provider supplies credentials from its actual context. Check cache principal, service and expiry before diagnosing a 401 as a wrong password. A service-only cache for another hostname does not establish permission to obtain or use this service's ticket.

Keep the hostname in the URL: substituting an IP or unrelated alias can select an incorrect HTTP service principal. A hostname-resolution override does not necessarily change the GSS provider's canonicalization. Diagnose the actual selected principal and name lookup rather than globally disabling canonicalization or adding unrelated host aliases. Proxy authentication has separate `--proxy-negotiate` settings.

Check curl status, the final HTTP response and expected body together. Header capture can include the initial authentication challenge and later responses; an initial 401 is not automatically the final result. A completed request can still return an authorization denial. Negotiate authentication identifies a client to the web application; any operation the application performs can run as a different service account.

Use HTTPS and the established certificate trust when the service supports it. SPNEGO does not itself guarantee HTTP body confidentiality. Do not follow an unexpected cross-host redirect with credentials; inspect its destination and scope first. Keep authentication-bearing header/trace captures private. Record the selected cache/principal, URL, final status and result without copying tickets or authentication blobs into the report. Missing GSS support, cache, compatible provider or service naming leaves this branch unavailable.

Reference: [curl Negotiate and authentication options](https://curl.se/docs/manpage.html#--negotiate).
