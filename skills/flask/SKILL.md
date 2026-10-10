---
name: flask
description: Serve a small owned HTTP form or browser-test page with the installed Flask CLI. Use when static hosting cannot handle POST fields, route/asset origins differ or a controlled opener-navigation test needs application responses.
---

# Flask for a controlled HTTP exercise

Read this entire SKILL.md before acting. Use an owned reviewed application and its existing Python/Flask environment; CLI discovery imports the application and can run its module body. For POST-field handling or browser opener tests, read [forms and browser origins](references/forms-and-origins.md) fully before serving. Finish with the route/method, received fields or browser observation and its limits, then stop the owned server. A 200 response alone proves no authentication or browser behavior.

Define `python_bin` as the intended installed interpreter and `app_file` as the absolute owned application file. Inspect that environment's CLI rather than assuming the shell's `flask` wrapper uses it:

~~~bash
"$python_bin" -m flask --version
FLASK_SKIP_DOTENV=1 "$python_bin" -m flask --app "$app_file" routes
FLASK_SKIP_DOTENV=1 "$python_bin" -m flask --app "$app_file" run --host 127.0.0.1 --port 8080 --no-debugger --no-reload
~~~

These commands use a Flask release supporting `--app`. For an older reviewed app using `app.run`, invoke its script with the same interpreter after checking its explicit bind/debug/reloader settings. `routes` also imports the app; it is not passive inspection of untrusted code. Dotenv suppression does not clear inherited Flask environment variables. Inspect those and the startup banner if behavior differs; do not inherit debug mode for a network exercise.

The development server fits a short controlled test, not a deployed public service. Bind to an explicitly authorized reachable interface only when a remote test requires it; loopback cannot receive another host's browser. A bind failure is not a running receiver, and a privileged port does not require elevating the whole application when a high port works. Stop it after the test and retain only the requested private evidence.

See [Flask CLI](https://flask.palletsprojects.com/en/stable/cli/) and [request/template API](https://flask.palletsprojects.com/en/stable/api/).
