---
name: "dalfox"
description: "Scan for and verify XSS in scoped web parameters with Dalfox, including blind XSS callback modes. Use on authorized targets to confirm reflection contexts; a payload that fires is evidence, not a report entry until impact is shown."
---

# Dalfox XSS scanning

Installed invocation: `/usr/bin/dalfox`, version `3.2.4` (Kali package dalfox).

Read this entire SKILL.md before acting. Require authorized target URLs or a parameter wordlist context and an output file. Finish with confirmed reflection findings separated from scanner-estimated ones.

~~~bash
/usr/bin/dalfox file "$targets" -o "$out" --silent
~~~

`file` reads target URLs (one per line, with parameters); single targets take `url "https://$host/?q=FUZZ"`. Dalfox mines parameters and DOM sinks and attempts verification of reflection context — verified findings carry more weight than its parameter-mining guesses. Blind XSS modes (`-b https://callback`) deliver stored payloads to your collector: that is payload delivery into the target's storage and belongs inside the engagement's authorized actions.

WAF responses and rate limits are target signals: use `--delay` and reduce workers rather than switching to evasion-first behavior, and record which requests were blocked. A clean run reports no verified reflection under the payloads tried — not the absence of XSS.

References: [project documentation](https://github.com/hahwul/dalfox).
