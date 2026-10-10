---
name: iis-shortname-scanner
description: Check scoped IIS paths for short-name disclosure with the Java IIS ShortName Scanner and turn partial 8.3 names into bounded full-name candidates. Use when response differences or uncertain enumeration results need interpretation.
---

# IIS ShortName Scanner

This procedure is for Soroush Dalili's Java IIS-ShortName-Scanner. Other tools such as shortscan have different options. Use a reviewed JAR and its matching configuration, plus a compatible Java runtime. An unsupported class-version error is a local runtime mismatch, not a target result.

Define `jar` and `config` as existing absolute paths, `url` as the scoped base URL **ending in `/`**, and `check_report` / `enum_report` as distinct fresh paths. The scanner normally trims a final path component without a trailing slash; verify the actual target printed in the result before attributing findings to a directory.

Review the supplied XML before sending requests: methods, headers/cookies, proxy, timeouts, delay, retries and name-search limits all affect the probe. Default method lists can include OPTIONS, POST, DEBUG and TRACE. Set `maxDelayAfterEachRequest` in milliseconds to fit the agreed request budget; `maxRetryTimes` is a retry count. For unattended operation, `hassleFree=true` suppresses optional prompts; it does not establish sensible delay or proxy settings for you.

## Establish a response distinction before enumeration

The two-argument form checks for disclosure without full name enumeration. It still sends active HTTP probes:

~~~bash
java -jar "$jar" "$url" "$config" > "$check_report" 2>&1
~~~

Inspect the final result and diagnostics, not just the process exit code. A useful positive result depends on repeatable differences between valid and invalid name patterns for a particular method, URL suffix and session. There is no universal rule that `404` means a matching name or `200` means no match. Login redirects, proxy responses and changing error bodies can prevent a reliable comparison. A negative check also does not establish that no files exist.

When that distinction is reliable and enumeration is in scope:

~~~bash
java -jar "$jar" 2 0 "$url" "$config" > "$enum_report" 2>&1
~~~

`2` shows progress; `0` selects serial operation, not zero requests. Keep a deliberate delay even without parallel threads. Check the reported target, selected method/suffix, completed summary and network warnings. Connection failures, uncertain `?` characters or partial results call for a narrower/slower check; do not present them as confirmed filenames.

## Convert partial names into a small candidate set

An **illustrative** `TRANSF~1.ASP` result constrains a short alias. It does not distinguish `transfer.asp` from `transfer.aspx` or identify the complete original basename. Likewise, a directory alias does not prove directory listing or file-read access.

Use the observed prefix, application framework and known naming conventions to select a small local wordlist. Test candidate full paths with the same virtual host/session and a nonexistent-path baseline. Preserve confirmed full URLs separately from guessed names and short aliases. If several names fit, keep the ambiguity; a `~1` suffix is not a reversible encoding of the original name. Coverage is limited by the configured character set, prefix/extension filters and numerical suffix range.

Consult the [project usage](https://github.com/irsdl/IIS-ShortName-Scanner), [configuration](https://github.com/irsdl/IIS-ShortName-Scanner/blob/master/release/config.xml) and [argument/response handling](https://github.com/irsdl/IIS-ShortName-Scanner/blob/master/src/main/java/iisShortNameScanner/IISShortNameScannerTool.java) when adapting a different release.
