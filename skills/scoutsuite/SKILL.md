---
name: "scoutsuite"
description: "Audit cloud accounts for configuration weaknesses with ScoutSuite across AWS, GCP, Azure, Aliyun, OCI, Kubernetes and DigitalOcean using provided credentials. Read-only CIS-style review that produces findings, not exploitation."
---

# ScoutSuite multi-cloud auditing

Installed invocation: `/usr/local/bin/scoutsuite` (console command is `scout`; pipx package scoutsuite 5.14.0), version `5.14.0`.

Read this entire SKILL.md before acting. Require credentials whose account is in scope for configuration review and a report output directory. Finish with the generated HTML report and the provider/regions actually covered.

~~~bash
/usr/local/bin/scoutsuite aws --profile "$profile" --report-dir "$report"
~~~

The first argument selects the provider (`aws`, `gcp`, `azure`, `aliyun`, `oci`, `kubernetes`, `do`); credentials come from the provider's own CLI profile or explicit flags. The run is a read-heavy API crawl: it enumerates resources across regions, so on large accounts expect duration and API cost, and prefer reusing one run's report over repeating scans.

Findings are configuration observations mapped to benchmark checks (open security groups, over-permissive IAM, unencrypted storage). A finding is a lead for the engagement, not a confirmed exploitable path — verify impact with the account owner's scope before acting on any item. Reports aggregate credentials-adjacent detail: store them with engagement evidence handling, not in shared folders.

References: [project documentation](https://github.com/nccgroup/ScoutSuite).
