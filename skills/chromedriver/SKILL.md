---
name: chromedriver
description: Read an owned ChromeDriver service's WebDriver status and distinguish driver readiness, build metadata and browser-session success.
---

# Read the existing driver's status

Read this entire SKILL.md before acting. Require the owner's exact existing driver endpoint and approved read access. Finish with the actual HTTP status, parsed readiness/message and available driver metadata; preserve connection or parsing failures as unresolved. No conditional resources are required.

Define `driver_url` as the approved service base URL without a trailing slash. A common port or an unknown-command response at `/` is only a lead; request its actual status route. Use a fresh private capture directory:

~~~bash
umask 077
capture=$(mktemp -d) || exit 1
curl --silent --show-error --max-time 10 \
  --dump-header "$capture/headers" --output "$capture/body.json" \
  --write-out 'http_status=%{http_code}\n' "$driver_url/status"
~~~

Check curl's exit status, HTTP status and complete JSON before interpreting it. A redirect, HTML page, authentication failure or error object is not driver readiness. WebDriver returns the status object under `value`: inspect its boolean `ready`, human-readable `message` and any implementation-specific metadata. Keep the capture private and retain only the required summary according to the task's evidence policy.

`ready: true` says the service considers itself ready; it does not guarantee a New Session command will succeed. Driver build/version and operating-system fields are self-reported metadata, not proof of the selected browser's version or the server process's effective UID. An omitted process owner in a socket listing does not establish that UID either. Correlate service identity with the owner's process/service inventory when attribution is required.

A status request does not start a browser. Creating a session starts processes and needs its own reviewed test configuration and lifecycle; do not use session creation as a health check. ChromeDriver should run under a dedicated unprivileged test account with deliberate network exposure. Preserve the configured endpoint rather than widening its listener to diagnose access.

References: [WebDriver status semantics](https://www.w3.org/TR/2018/REC-webdriver1-20180605/#status), [ChromeDriver deployment guidance](https://developer.chrome.com/docs/chromedriver/security-considerations).
