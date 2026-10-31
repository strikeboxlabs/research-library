---
name: "tplmap"
description: "Detect and exploit Server-Side Template Injection across template engines with tplmap, from engine fingerprinting to command execution. Use on authorized targets; successful exploitation is code execution on the application host."
---

# tplmap template injection

Installed invocation: `/usr/local/bin/tplmap` (wrapper over the upstream epinna/tplmap script with an isolated venv).

Read this entire SKILL.md before acting. Require an in-scope endpoint with a suspect parameter and explicit authorization for code execution if checks succeed. Finish with the engine identified and each exploitation step taken.

~~~bash
/usr/local/bin/tplmap -u "$url"
~~~

The default run fingerprints the template engine through benign evaluation probes across the common engines (Jinja2, Twig, Smarty, Mako, Velocity and others) and reports injection without acting further. `-os-shell` opens command execution once injection is confirmed — that crosses from detection into executing on the application host and must be inside the engagement scope.

Distinguish engine certainty: a fingerprint match on evaluation syntax (e.g. `{{7*7}}` rendering 49) proves evaluation, while full exploit confirmation requires the engine-specific payload chain tplmap builds. Record which template engine and payload class succeeded — remediation differs per engine.

References: [project documentation](https://github.com/epinna/tplmap).
