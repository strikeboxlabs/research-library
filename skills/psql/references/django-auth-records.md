# Selected legacy Django/Sentry authentication records

Use a known authorized database connection and the entrypoint's startup/authentication/schema checks. A legacy `sentry.conf.py` is executable Python, not a passive settings file to import. Read the relevant `DATABASES` values and deployment overrides without running it; establish the effective engine/name/host/port/user. A file's password is a candidate for that database role. `localhost` means the executing client's network namespace and selects TCP, not a Unix socket.

Inspect the actual relation/columns before querying. The older default Django table can be `auth_user`; a custom user model, schema or authentication plugin can differ. A field named `password` is often an encoded verifier, not cleartext. `is_staff` is an application permission flag, separate from `is_superuser`, `is_active` and any OS user. Do not assume every email-like database username has an identically named Unix account.

For the confirmed illustrative `public.auth_user` schema, use a structured export for one selected account rather than copying wrapped terminal tables. Retain the entrypoint's reviewed libpq `service`, `account_label` and fresh private `output`:

~~~bash
umask 077
psql -X -w --dbname="service=$service connect_timeout=5" --set=ON_ERROR_STOP=1 \
  --set=account_label="$account_label" --quiet --csv --pset=pager=off >"$output" <<'SQL'
BEGIN READ ONLY;
SET LOCAL statement_timeout = '5s';
SELECT id, username, password, is_staff, is_active
FROM public.auth_user
WHERE username = :'account_label'
ORDER BY id
LIMIT 2;
COMMIT;
SQL
~~~

Adapt verified columns first. More than one matching account is an identity ambiguity, not an instruction to choose the first hash. Use a stable selected ID if available. `--csv` requires psql 12+; an older server can still use a compatible newer client. If the available client lacks it, choose a reviewed structured export rather than treating unaligned pipe-delimited output as CSV. Preserve exit status/stderr; empty or partial output after failure is not a completed record acquisition.

Keep the complete algorithm/cost/salt/digest field intact for its applicable offline check, mapping it to that row. `pbkdf2_sha256$...` uses a literal salt and base64 digest; it is not a base64-encoded password. Filtering `/etc/passwd` only for `/bin/bash` misses accounts with other shells and says nothing about directory/NSS users or actual SSH policy. Corroborate a proposed OS-account mapping separately before a selected authorized login. A recovered application candidate remains separate from current service authentication.

See [psql export/substitution](https://www.postgresql.org/docs/current/app-psql.html), [Django custom user model](https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#substituting-a-custom-user-model) and [Django user fields](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#user-model).
