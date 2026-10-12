---
name: magescan
description: Identify candidate Magento edition/version on one owned site with an existing MageScan PHAR. Use when several fingerprint matches or unknown output are being mistaken for a confirmed installed build.
---

# Read Magento version candidates

Read this entire SKILL.md before acting. Require a trusted existing MageScan PHAR, its compatible PHP CLI and the owner's exact site URL. No conditional resources are required. Finish with the command/status, returned edition and complete candidate list, plus unresolved deployment evidence.

Define `php_bin` as the trusted interpreter, `magescan_phar` as the installed artifact's absolute path and `site_url` as the selected owned HTTP(S) origin including any actual installation prefix. Check this installation's command interface:

~~~bash
"$php_bin" "$magescan_phar" --version
"$php_bin" "$magescan_phar" help scan:version
"$php_bin" "$magescan_phar" scan:version "$site_url"
status=$?
~~~

Invoking a PHAR executes PHP code; downloading it or recognizing the filename does not establish trust. Keep TLS certificate validation and resolve the selected site's naming/trust requirements before retrying. Do not use `--insecure` as a naming repair.

Retain every reported version when the fingerprint matches several releases. `Unknown` can reflect blocked paths, changed assets, an unexpected route or unsupported signatures; it does not prove Magento is absent. Compare with the owner's installed package/build inventory when an exact deployed version or patch status matters. A logo or copyright date is weaker evidence, and a candidate version alone does not establish applicability of a vulnerability.

This selected command requests version evidence. `scan:all` includes other checks with separate scope and results; its path-check Fail label is not proof of a failed CLI execution or verified file contents. The task is complete when the edition/candidates and uncertainty are recorded; do not create orders or retrieve configuration secrets to resolve them.

Adapted from [Steve Robbins's MageScan usage](https://github.com/steverobbins/magescan) and [version checker](https://github.com/steverobbins/magescan/blob/master/src/MageScan/Check/Version.php), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This guidance narrows the procedure and adds result/coverage interpretation.
