---
name: wpscan
description: Inspect a scoped WordPress site with WPScan and interpret plugin/version findings. Use when enumeration sets, detection modes, API coverage or false-positive responses affect conclusions.
---

# WordPress inventory evidence

Check `wpscan --version` and `wpscan --hh`. Use the actual WordPress base URL, including any installation subdirectory and required hostname. Inspect loaded configuration for credentials, cookies and enumeration overrides before reusing a previous command.

Define `site_url` as the authorized site and `report` as a fresh JSON output. This example selects popular-plugin enumeration with passive detection and paced requests:

~~~bash
wpscan --url "$site_url" --enumerate p --detection-mode passive --plugins-detection passive --plugins-version-detection passive --throttle 500 --request-timeout 15 --connect-timeout 5 --format json --output "$report"
~~~

Passive mode still makes HTTP requests; it is not an offline analysis. The throttle is milliseconds and forces one worker in the reviewed CLI. Request/connect timeouts limit individual operations, not total scan duration. Stop at the task's overall budget and report incomplete coverage. Check redirects before continuing to another site.

Enumeration **set** and detection **mode** are separate:

| Choice | Meaning |
|---|---|
| `p`, `vp`, `ap` | Popular, known-vulnerable, or all plugins in the tool's inventory; none guarantees all installed plugins. |
| `passive` | Evidence from fetched pages and exposed references; can miss unused or hidden plugins. |
| `aggressive` / `mixed` | Direct location probes, or combined methods; more requests. Select deliberately. |

Do not omit the value after `--enumerate`: bare `-e` enables a broader default set, including user/media and backup-related checks. Supported `--plugins-list` overrides the plugin set; check local help for its accepted list syntax. Global detection mode and plugin/version-specific overrides can differ.

Keep the finding's evidence URL, detection method and confidence. A readme's stable tag may differ from deployed code; a plugin directory response can be a soft 404. Compare an absent path's response before trusting a flood of detections, and verify an advisory's actual affected/fixed version and prerequisites. Detection is not exploitation or proof of a reachable vulnerable path.

Inventory can work without vulnerability API access. Missing token, quota exhaustion or lookup failure means incomplete vulnerability annotations, not a clean site. `--update` refreshes local metadata; it does not by itself establish complete vulnerability data. Record tool/data context, selected sets/modes, lookup status and scan completion.

For a user-inventory task, select an explicit ID range such as `--enumerate u1-10` and the intended detection mode; this bounds the ID probes, not every passive discovery or request. Preserve whether a name came from an author slug, REST data or login-response behavior. A discovered author name does not prove administrator status, password reuse or a successful login. A WordPress password-protected post uses a content password; opening it does not establish an authenticated WordPress account session.

Resolve option differences with [upstream usage](https://github.com/wpscanteam/wpscan/blob/master/README.md) and [enumeration options](https://github.com/wpscanteam/wpscan/blob/master/app/controllers/enumeration/cli_options.rb); see [WordPress content visibility](https://wordpress.org/documentation/article/content-visibility-classic-editor/) for post-password semantics.
