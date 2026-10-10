---
name: bbot
description: Use BBOT presets and event-driven modules for scoped reconnaissance, retaining module failures and structured scan results. Use when selecting an existing recon engine, loading a custom module or assessing preset-controlled code execution under sudo.
---

# BBOT reconnaissance and module execution

Read this entire SKILL.md before acting; reuse complete current context. Select the target scope, trusted preset/modules and output location before a scan. For custom Python modules, unexpected loading failures or a privileged BBOT grant, read [custom modules and execution authority](references/custom-modules.md) fully first. Finish with the actual enabled/failed modules and requested observations or execution marker; a banner or empty output is insufficient.

BBOT is an event-driven reconnaissance engine. Presets select modules, configuration and scope; discovered events can feed further modules. Visualization is an optional output use, not the tool's identity. Prefer its existing discovery capabilities over building a replacement collector.

Inspect the installed interface and relevant module options:

~~~bash
bbot --version
bbot --help
bbot -lp
bbot -l
bbot -mh crt
~~~

`-lp` lists presets, `-l` lists modules, and `-mh` selects module help on current versions. Check local help on 2.x deployments: module APIs, names and configuration changed in 3.x. Do not apply a current preset to an older installation without checking its selected modules/options.

For subdomain discovery, define `target` as the authorized domain, `scan_name` as a fresh unique run name and `out_dir` as the chosen evidence directory. Review the built-in preset and selected module requirements; on supporting versions:

~~~bash
bbot -t "$target" -p subdomain-enum -rf passive --no-deps -n "$scan_name" -o "$out_dir"
~~~

`-rf passive` retains modules bearing that flag; it does not promise zero network traffic. Public data services and internal DNS processing can still be contacted. Domain targets normally include subdomains; `--strict-scope` changes that to exact matches and can defeat a subdomain-discovery task. Use the supported blacklist/exclusions for actual scope boundaries rather than treating an output filter as a traffic restriction.

BBOT can install module dependencies during preparation. `--no-deps` disables that installation; it does not manufacture missing binaries/API credentials, disable all module setup effects or make arbitrary modules trusted. Record missing capabilities or select a supported alternative. Setup failure is evidence that the module did not contribute, not evidence that no assets exist. `--force` permits continuation through certain failed setups/conditions; it does not repair dependencies or grant privileges.

Use the logged output paths. Default output modules produce CSV, JSON and text in the scan directory, with source-module, scope and event information. `-om` adds output modules; remove unwanted defaults with `-eom` when appropriate. Reusing a scan name can append old results, so separate a new run from an intentional continuation.

Distinguish a discovered `DNS_NAME`, an observed URL and a confirmed reachable service. An affiliate or out-of-scope event is a lead rather than permission to probe it. Retain the source module, tags, scope distance and failures with the observation; a DNS label alone does not establish ownership or current reachability. Confirm the particular result needed for the task before handing it to the next operation.

For version recovery see the [BBOT CLI](https://www.blacklanternsecurity.com/bbot/Stable/scanning/advanced/), [presets](https://www.blacklanternsecurity.com/bbot/Stable/scanning/presets/) and [output formats](https://www.blacklanternsecurity.com/bbot/Stable/scanning/output/).
