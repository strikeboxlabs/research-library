# Inspect packaged Spring Boot configuration without starting the application

Define `archive` as the preserved JAR working copy's absolute path. A JAR is a ZIP-based archive; inspect it with UnZip rather than executing `java -jar` to discover settings. Apply the entrypoint's size, path, duplicate-name and integrity checks first. Boot Loader-compatible JARs put application classes/resources under `BOOT-INF/classes/` and dependency JARs under `BOOT-INF/lib/`; other packaging can differ.

After confirming exactly one ordinary member at the name below, define `output` as a fresh private file under an existing working directory:

~~~bash
umask 077
unzip -p "$archive" 'BOOT-INF/classes/application.properties' >"$output"
~~~

Check status before consuming output; a missing member is not an empty valid configuration. This selects the one member without expanding the whole archive. Duplicate names can concatenate bytes, and a CRC failure can leave output behind. Do not treat either as a valid properties file. Use the actual listed path for another profile/configuration format; a broad wildcard can silently combine several files.

Read related profile-specific properties/YAML and external-config references only when they explain the task. The packaged values are defaults or inputs, not a verified snapshot of the running application. External files, active profiles, environment variables, system properties or command-line arguments can override them; values can also reference placeholders. Missing packaged credentials can be intentional external configuration.

**Illustrative:** `spring.datasource.url=jdbc:postgresql://localhost:5432/example` identifies a PostgreSQL connection in the application's runtime network context. It does not place that server on the analyst's workstation. A datasource username/password describes database authentication, not a web administrator or OS login. Preserve property names and provenance while keeping values out of public reports; do not test them against other services to infer reuse.

Likewise, a packaged `management.endpoints.web.exposure.include` setting is not live proof of accessible endpoints or their authentication policy. Compare against authorised current runtime evidence when the task requires that conclusion.

References: [Spring Boot archive layout](https://docs.spring.io/spring-boot/specification/executable-jar/nested-jars.html), [external configuration precedence](https://docs.spring.io/spring-boot/reference/features/external-config.html), [Info-ZIP](https://infozip.sourceforge.net/UnZip.html).
