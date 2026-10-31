---
name: "arjun"
description: "Discover hidden HTTP parameters with Arjun using reflection and response-divergence heuristics across GET, POST, JSON and XML. Use to find parameter names that path-based fuzzing cannot see; found parameters are surface, not vulnerabilities."
---

# Arjun parameter discovery

Installed invocation: `/usr/bin/arjun`, version `2.2.7` (Kali package arjun).

Read this entire SKILL.md before acting. Require an in-scope endpoint URL and an output file. Finish with discovered parameter names per method tested.

~~~bash
/usr/bin/arjun -u "$url" -o "$out" --stable
~~~

`--stable` slows requests to succeed behind rate limiting; `-m GET,POST,JSON,XML` selects the body shapes probed (default covers them). Discovered parameters are inputs the application parses — the value is what they enable next: unauthenticated behavior differences, injection surfaces for sqlmap/dalfox, or debug parameters.

Arjun's heuristics compare response divergence against baseline noise; on endpoints with high natural variance (search, render) expect false positives — confirm a parameter by observing a controlled change with two distinct values before building on it. A quiet endpoint is unprobed-shape coverage, not proof no hidden parameters exist.

References: [project documentation](https://github.com/s0md3v/Arjun).
