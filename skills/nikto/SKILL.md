---
name: nikto
description: Survey a scoped web server for configuration and vulnerability candidates with Nikto.
---

# Nikto web server survey

Read this entire SKILL.md before acting. Select the authorized scheme, host, port and test categories before sending requests. Preserve the report and distinguish candidates from independently confirmed findings. Finish with the target, selected categories, scan completion or time limit, and supporting request/response evidence for any confirmed finding.

## Installed implementation

Use `/usr/bin/nikto`, version 2.6.1. It needs no separate server process. Plain-text file output uses `-Format txt`; `text` is not the documented format name. Bound testing time with `-maxtime`, using an explicit unit such as `300s`.

## Survey command

Define `target` as the full scheme and authority, such as `https://app.example:8443`, and `output` as a fresh text-report path. This example selects information-disclosure tests:

~~~bash
/usr/bin/nikto -h "$target" -Tuning 3 -maxtime 300s -o "$output" -Format txt -ask no -nocheck
~~~

`-ask no` disables result submissions; `-nocheck` skips startup update checks. `-h` accepts a URL including scheme and port; when passing a bare host, specify a nondefault port and TLS explicitly as needed.

Choose the tuning categories for the requested survey. `3` is information disclosure, `4` is XSS/script/HTML injection, and `9` is SQL injection. Omitting `-Tuning` uses the default test selection and broadens the survey. These are active HTTP probes; category selection does not turn them into passive observation. See the [upstream tuning guide](https://github.com/sullo/nikto/wiki/Scan-Tuning) when choosing categories; installed help is authoritative for this version's options.

## Reading the output

Interpret finding lines in their response context:

- Missing-header messages are configuration observations. Explain the header's applicability to the actual response and transport before assigning impact.
- An outdated-component message based on a banner is a version hypothesis. A banner alone does not establish the installed or patched version.
- A CVE reference identifies a candidate issue. Confirm the relevant response and affected behavior within scope before reporting the vulnerability as established.
- Repeated directory-listing or product-specific matches may describe the same response pattern. Compare the responses before counting them as separate issues.

A finding absent from the report means no reported match under this test selection, not a secure service. A timeout or interrupted scan is partial evidence; retain it, report the limitation and repeat only the missing authorized work when needed.
