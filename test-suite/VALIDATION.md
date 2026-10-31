# Validation record

Prepared on 2026-10-31 on Windows. Python controller tests, mock-provider tests, fixture/grader calibration and source checks are distinct from actual Linux/Pi/GLM task trials.

This host has Python 3.15.2. Docker is not on PATH and WSL is not installed. No package installation, Docker build, remote Linux connection or real model request was performed. The supported controller target is Python 3.10+; exact target-version execution remains part of Linux acceptance.

The test runner exercises seeded fixture creation, independent graders, invalid outputs, bounded path handling, randomized paired plans, snapshots/resume, usage accounting, proposal restrictions, event parsing and process supervision. API calls and Docker are mocked in controller/runtime tests. Owned Python subprocess tests verify timeout and output capture mechanics. Reference command integration tests run only on Linux with their required tools and otherwise skip explicitly.

Run these checks after copying the checkout to Linux:

```bash
python3 -B test-suite/test.py
python3 -B test-suite/bench.py doctor --config test-suite/config.local.json
python3 -B test-suite/bench.py calibrate --output runs/skillbench-calibration-linux
python3 -B test-suite/bench.py smoke --config test-suite/config.local.json --output runs/skillbench-smoke-linux
```

Inspect skips instead of treating the test process's exit code as complete coverage. Symlink tests require actual filesystem support. The smoke result must pass before using the corresponding case for a model comparison. The first real-model acceptance check should be a single baseline/current pair; inspect raw finalized events, the observed model identity, exact output artifacts and nonzero token accounting.

Actual local check counts and outcomes are recorded in the repository's [validation record](../docs/validation.md). Future run artifacts remain in ignored `runs/`; this file is not evidence of a Linux or model pass.


## Linux acceptance progress — 2026-10-31

On the Linux deployment with Python 3.14.8, all 88 suite tests passed with zero skips, including all seven real host CLI reference cases and symlink checks. The Windows-lock test initially failed because globally mocking `os.name` changed Python 3.14 pathlib behavior; its mock now replaces only the campaign module's OS reference. Production controller code and published skills were not changed.

All seven Python grader calibrations passed; artifacts are in ignored `runs/skillbench-calibration-linux-first/calibration.json`. Installed the missing Docker CLI and built the documented worker image with Pi 1.3.0, image ID `sha256:986904bbf639ff6b1f8ebf68fc838117d1f2e8b68b43401c18120a06759c9acd`. Offline preflight passed. All seven container reference CLI smoke cases passed with cleanup confirmed; evidence is in ignored `runs/skillbench-linux/smoke-all/{manifest,smoke}.json` and per-case logs. The initial root-controller smoke attempt failed on workspace write permissions and remains retained in `runs/skillbench-smoke-linux-first`; the successful run used controller/worker UID 10001 and Docker socket GID 956.

The local first-pair config selects `jq-exact-text`, one repetition, baseline/current, and explicit nonroot worker identity. Run the controller with `setpriv --reuid=10001 --regid=956 --clear-groups python3 -B test-suite/bench.py run --config test-suite/config.local.json` from the repository root, with the configured credential in its inherited environment. These numeric IDs are deployment-local facts, not requirements for other hosts.

No real GLM request, baseline/current model comparison, full pilot or optimizer search has run: `ZAI_API_KEY` was absent. Endpoint/model/credential configuration must be established before continuing those phases. Reference smoke success does not establish skill effectiveness.


## Real GLM/Pi pilot and optimizer attempts — 2026-10-31

The credential prerequisite was resolved from the protected Hermes Agent configuration. The active service was Z.ai's Coding Plan endpoint, `https://api.z.ai/api/coding/paas/v4`, with model `glm-5.3`, differing from the example's general endpoint and flash model. A local launcher loads the credential into the process environment, then drops to the worker's unprivileged identity. No key was copied into suite configuration or saved artifacts.

The first baseline/current pair passed both trials with observed model `glm-5.3` and nonzero token usage: 25,015 baseline and 26,099 current reported total tokens. Campaign: `runs/skillbench-linux/20261031T062639Z-77ad1af7`. The transcript confirms Pi expanded `/skill:jq` into the user prompt; absence of a separate read-tool call does not imply the skill was absent.

The complete 24-trial development pilot finished in approximately 1,197 controller seconds. All 12 baseline and all 12 current trials passed: 12 paired ties across four task families, no wins/losses, and no confidence interval. Baseline used 283,406 reported total tokens (23,617.17 per success), versus current's 498,438 (41,536.50 per success), approximately 76% more. Median trial duration was 37.86 seconds baseline and 50.48 seconds current. Every trial reported the requested model, nonzero token usage, unchanged inputs and confirmed cleanup. All 12 current transcripts contain the expanded skill. Dollar costs were unavailable and remain unknown. Reports and raw evidence: `runs/skillbench-linux/20261031T062816Z-05d08099/`. This small synthetic development pilot does not establish a success-rate gain or library-wide efficiency conclusion.

Two bounded one-proposal jq optimization attempts used the pilot's development evidence. The 8,192-output-token attempt (`optimization-26c9e7b5bbc6`) was rejected for an incomplete response: 19,393 total tokens, with 8,188 reasoning tokens out of 8,192 completion tokens. A retry at the supported 16,384 cap, configured with a different development seed (`optimization-f6922c1b20ef`), returned a complete response but was rejected for a path outside the permitted existing Markdown resources: 15,262 total tokens. Both requests' usage was retained, totaling 34,655 tokens. No admissible candidate was created, so zero candidate worker trials ran; candidate evaluation and independent confirmation remain incomplete. The journal's overall `complete` status means the search loop ended, not that a candidate succeeded; each candidate has `proposal_or_evaluation_error`. No published skill changed or was promoted.

Combined first-pair, pilot and proposal usage was 867,613 reported total tokens; dollar cost is unknown. A final exact-value scan found no credential matches in saved Linux artifacts. Aggregate local evidence is `runs/skillbench-linux/acceptance-summary.json`. The suite's 88 tests passed again with no skips after the runs. Remaining work includes obtaining an admissible candidate for evaluation, confirmation before promotion, and the broader fixture/selection/context/security research listed in the README. No held-out model campaign ran.


## Challenge suite extension and screening — 2026-10-31

Added three development families while retaining the original four regression controls: replayed/typed event reconciliation with whole-shard rejection; manifest-guided archive revision recovery; and latest-commit SQLite export from a coherent DB/WAL capture. Ten cases now include the three original holdouts. Correct alternative implementations remain eligible.

Added negative controls for stale exports, source sidecar creation, numeric/string identity collapse, filtering before revision resolution, accepted prefixes of bad shards, and first/last/concatenated archive occurrences. All 99 suite tests passed with zero skips, including actual Linux CLI integration. Ten Python grader calibrations and all ten pinned-image CLI smoke cases passed. New artifacts are in ignored `runs/skillbench-calibration-challenges/` and `runs/skillbench-linux/smoke-challenges/`. The repository checker passed (546 packages, zero errors), and diff whitespace checks passed.

Reports now expose per-case condition results and flag complete baseline samples at ceiling; partial runs and infrastructure gaps cannot qualify. The regular example plans 42 trials; `config.screening.json` plans eight trials with a 240-second worker deadline. The optimizer enumerates exact package-relative paths, records safe path/finish diagnostics, supports the demonstrated 16,384-token/low-effort configuration, uses fresh seeds beyond source and earlier candidate ranges, and returns nonzero with `complete_with_errors` for proposal/evaluation workflow failures. A completed evaluation that finds a losing candidate is still a completed experiment, not a successful skill improvement.

Real GLM-5.3/Pi screening used seed 49031 and the previously recorded image. Baseline and current both passed all four tasks (8/8 total), so all four are explicitly marked as observed sample ceilings. Each cell below is one trial, not an estimate of population reliability.

| Case | Baseline seconds / tokens | Current seconds / tokens |
|---|---:|---:|
| jq-exact-text | 24.1 / 17,758 | 31.8 / 20,623 |
| jq-reconcile-events | 113.7 / 101,689 | 156.7 / 145,026 |
| sqlite-wal-export | 198.9 / 189,015 | 89.7 / 74,249 |
| tar-manifest-recovery | 36.9 / 27,335 | 75.7 / 79,723 |

Total reported tokens were 335,797 baseline and 319,621 current; dollar costs remain unknown. The WAL case was faster and used fewer tokens with the skill in this single pair, while the other cases showed overhead. No general efficiency or correctness improvement is established. Screening reports: `runs/skillbench-linux/20261031T072250Z-177632a9/`.

One real bounded optimizer request produced an admissible SKILL.md candidate in 15.5 seconds using 8,610 tokens, and candidate links validated. Fresh-seed evaluation (49032) completed both worker trials: current passed (133.1 seconds, 122,351 tokens), while candidate failed with `budget_exceeded` / `model_output_limit` (116.8 seconds, 79,377 tokens). This is one paired loss; no candidate was promoted and published skills are unchanged. The request plus evaluation used 210,338 reported tokens. Journal and reports: `runs/skillbench-linux/optimization-dacd79a6f66e/`.

The real proposal focused on an easy jq case whose evidence was supplied even though only reconciliation was selected for evaluation. After this observation, feedback was restricted to selected evaluation cases and the prompt explicitly disallowed treating nominal tool choice as a benefit. Those final refinements passed regression tests; the paid optimizer was not rerun after them. The saved manifests retain the actual engine hashes used for each experiment. Aggregate evidence is `runs/skillbench-linux/challenge-acceptance-summary.json`; an exact-value scan found no credential matches in the new artifacts.

These challenge mechanisms improved coverage and exposed cost differences and a candidate regression, but GLM still passed all baseline screening cases. Further correctness discrimination needs independent representative workload families, not a claim that these cases are now sufficiently difficult. No held-out model confirmation or library-wide validation was performed.


## Installed-tool Flash observation — 2026-10-31

Following the request to skip readiness checks, used the installed Pi 1.3.0 and host tools for one bounded Pentest Ground DVWA SQL-injection task. No tools were installed for this observation. Both workers reported `glm-5.3-flash` through `https://api.z.ai/api/coding/paas/v4`, using the existing Hermes credential only through the environment. Earlier GLM-5.3 results above remain results for that different model. The example, screening and ignored local configurations now select Flash and the Coding Plan endpoint.

This was a manual local-toolbox observation, not a new calibrated suite case. An unprivileged Bubblewrap process exposed installed executables read-only, a private writable workspace, and ordinary Pi discovery over 16 frozen relevant skills in the current condition; baseline had no skills. No `/skill:` invocation forced a tool choice. The remainder of the library and private home were hidden. Order was current then baseline. Each worker had 240 seconds and a task allowance of 40 HTTP requests at no more than one per second; the request allowance was instructed and manually checked, not enforced by a network proxy. The model output cap was 8,192 tokens per response, not a campaign token quota. Two earlier launcher attempts failed before model invocation and remain separately retained.

| Condition | Process outcome | Seconds | Observed HTTP requests | Reported total tokens |
|---|---|---:|---:|---:|
| Current library subset | Completed | 197.527 | 7 | 151,322 |
| No skills | Timed out; report already written | 240.188 | 9 | 86,693 |

The current worker independently read the entire curl entrypoint. It kept TLS verification enabled and reached the unauthenticated challenge directly. Baseline attempted an unnecessary default login, used `curl -k`, and later deleted a saved security-page response and its cookie jar. Both supported SQL injection with a change from a missing-table error for ordinary input to a SQL-syntax error for malformed injected input. Current also corroborated the sink using the lab's same-origin source viewer. The missing `dvwa.users` table prevented row-result comparisons; neither trial demonstrated data extraction. HTTP 200 alone was not treated as success.

Neither trial fully satisfied the task: both saved their report outside the required `result/report.json` path. Current wrote `evidence/report.json`; baseline wrote `sqli-assessment/report.json` and never produced a final assistant response before timeout. The task artifact error is not evidence that a generic report-writing reminder belongs in each tool skill.

Baseline's report incorrectly grouped sqlmap's request pacing and total-request budget as unavailable controls. Installed `/usr/bin/sqlmap` reports `1.10.10#stable`; `-hh` documents `--delay`, and installed `lib/request/connect.py` sleeps for that interval before requests. The sqlmap skill now exposes pacing in discovery text, uses the verified executable path, and distinguishes `--delay`/single-thread pacing from an exact total request quota. For a small strict quota, a countable manual proof can still be the appropriate choice. Neither worker read sqlmap, and no worker trial of this revision has run: this is a verified documentation correction prompted by a baseline misconception, not a measured performance improvement.

Artifacts, frozen skills, manifests, transcripts, response hashes, manual review and installed-tool evidence are under ignored `runs/pentest-ground-flash-observation/`. This single pair used a shared live target without controlled resets and only a 16-skill discovery subset. It cannot establish causality, whole-library selection quality or general effectiveness. Finalized-event token totals include provider-reported usage; a timeout can omit in-flight usage. Dollar costs remain unknown. No additional paid optimizer or model campaign followed this observation.
