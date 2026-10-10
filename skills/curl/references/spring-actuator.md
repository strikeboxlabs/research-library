# Inspect an authorised Spring Boot management response

Use this branch for one known management endpoint or a framework clue that warrants a scoped check. An error-page label is a lead, not proof of the Spring Boot version, Actuator availability or exposed session data. Actuator provides management operations; some change state. A listed route is not an instruction to invoke every operation.

Define `management_url` as the approved discovery URL and `headers`/`body` as fresh private files. `/actuator` is the usual discovery path, but the management port/base path can differ and discovery can be disabled. Preserve the intended hostname, TLS trust and approved authentication context:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 20 --max-filesize 1048576 --dump-header "$headers" --output "$body" --write-out 'status=%{http_code}\n' "$management_url"
~~~

Check curl's exit, response status, content type and body together. With curl 8.4.0 or later the size limit also stops unknown-length transfers; older versions cannot enforce it when the size is not known before download; a rejected/truncated large response is incomplete, not malformed server JSON. Do not follow redirects or cross-origin discovery links without checking their destination and credential scope.

**Illustrative:** a successful JSON discovery body contains `_links` with a `health` entry but no `mappings` entry. This supports what discovery advertised to that caller, not that mapping code is absent. Distinguish implementation availability, management exposure and request authorization. A 401/403 is not an absent endpoint; a 404 can reflect the management address, proxy route or disabled exposure. A login/fallback HTML body is not management JSON even with status 200.

For an advertised and authorised read-only `mappings` URL, use the same capture pattern with that exact URL and new output files. Servlet responses commonly group entries by application context and dispatcher servlet, with a handler and a predicate describing paths/methods/content conditions. Reactive layouts differ. Preserve that structure and inspect the matching version's API schema; a handler mapping describes registration, not permission, successful execution or the external URL after proxy rewriting. Do not turn a mapped POST/DELETE into a verification request merely because it is listed.

Session endpoints depend on Spring Session and deployment/version details. The documented built-in retrieval supports a selected username; do not generalise a custom ID-to-username map into a universal unauthenticated session inventory. Session identifiers are credentials, not ordinary discovery labels. Similarly, masked environment values are not their literal secrets. Record unexpected disclosure with minimal redacted evidence rather than replaying a session or requesting unrelated dumps.

References: [Actuator availability, exposure and discovery](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html), [mapping response structure](https://docs.spring.io/spring-boot/api/rest/actuator/mappings.html), [session API](https://docs.spring.io/spring-boot/api/rest/actuator/sessions.html), [curl size/status options](https://curl.se/docs/manpage.html).
