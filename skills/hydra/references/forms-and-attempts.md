# HTTP forms and attempt accounting

## Build a response classifier before using a list

Capture the application's actual login method, endpoint, field names, cookies and CSRF behavior. Compare a known-invalid response and, when available, an authorized known-valid test account. A redirect or HTTP 200 alone does not classify success.

The `http-post-form` module takes a path, encoded form fields containing `^USER^`/`^PASS^`, optional parameters and a result condition. For an **illustrative** test application whose authenticated response contains a verified `Logout` marker:

~~~bash
form_spec='/login:username=^USER^&password=^PASS^:S=Logout'
hydra -l "$login" -P "$candidate_file" -t 1 -W 3 -f \
  -s "$port" -o "$results" "$target" http-post-form "$form_spec"
~~~

Replace that entire application-specific specification with observed values. Use `https-post-form` for TLS; a port number alone does not select TLS. `S=` matches an observed success condition; `F=` identifies a failure condition. With `F=`, an unexpected error, block page or expired-session page lacking the failure marker can look like success. Select one condition and validate controls before interpreting hits.

Colons delimit module fields; escape literal colons inside header values as required by the installed parser. `H=` replaces a header and `h=` adds one in the reviewed module; inspect `hydra -U http-post-form` rather than assuming curl header syntax. Cookie-fetching options do not solve every rotating CSRF/JavaScript challenge. If the module cannot reproduce the required request state, identify that specific limitation and use a session-aware tool instead of presenting a list of false hits.

## Control the actual attempt set

`-u` iterates across users for each password; it changes order, not the number of attempts or the lockout window. With multiple targets, per-target concurrency and overall concurrency differ. Do not infer a safe aggregate rate from `-t` alone. Plan attempts per account against the known policy, including failed attempts from other workers. Bound the input lists and track completed attempts, errors and skipped work.

For SSH, distinguish password authentication from keys and keyboard-interactive/MFA. A server requiring a second factor can reject a correct password through the selected path. For web forms, bind every hit to the response/session that produced it and verify the intended authenticated operation.

Hydra can write `hydra.restore` and resume with `-R`; inspect whether that state belongs to this exact task before resuming. A restored run can continue an old target/candidate set. Keep its sensitive state private and do not erase it merely to force an unrelated new run.

See [HTTP-form module help and response handling](https://github.com/vanhauser-thc/thc-hydra/blob/master/hydra-http-form.c).
