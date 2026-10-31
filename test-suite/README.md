# Linux CLI skill test suite

An executable pilot for comparing the research-library's skills with **GLM through Pi**. It runs disposable Linux workers, grades their artifacts independently, records usage, and can ask a separate GLM request to propose and evaluate bounded Markdown revisions.

**Status:** prepared for Linux installation; no real GLM/Pi benchmark result is claimed. The controller has no third-party Python dependencies. The first fixtures cover three tools, not the entire library. See [validation](VALIDATION.md) and [remaining work](#finish-on-your-linux-system).

## What is implemented

- Seeded, resettable fixtures with private answer data and independently checked artifacts.
- No-skill/current/candidate comparisons, randomized within matched task/seed blocks.
- Explicit skill invocation or ordinary discovery with a configurable catalogue size.
- Random or lexically similar distractors; similarity only selects test candidates, never grades correctness.
- Frozen skill packages, resource containment checks, image identity and controller-code hashes.
- One Docker/Pi worker at a time, bounded time/output/memory/PIDs, process cleanup and crash markers.
- Restartable campaigns; interrupted worlds are recorded and never blindly replayed.
- JSON/Markdown reports, failure-inclusive usage, paired outcome differences and visible missing measurements.
- Bounded proposal/evaluation cycles, with development evidence separated from held-out cases.
- Canonical `skills/` is never edited, installed, committed or promoted by this suite.

These are experimental mechanisms. Reading a whole skill, following a checklist, choosing a particular command, or minimizing skill count does not by itself earn a pass. A valid alternative CLI or small program can pass the outcome grader.

## Linux quick start

Run from the repository root as an ordinary Linux user with permission to use Docker. Python 3.10+, a Linux Docker daemon, and a worker image containing Python 3 and Pi are required. Host-installed tools are **not automatically present inside a container**. The optional Ubuntu 24.04 image below contains the three pilot tools. For the rest of the library, prepare an image matching your controlled toolbox; see [image details](docker/README.md).

```bash
python3 -B test-suite/test.py
cp test-suite/config.example.json test-suite/config.local.json
docker build -f test-suite/docker/Dockerfile -t research-library-skillbench:local test-suite
python3 -B test-suite/bench.py list
python3 -B test-suite/bench.py plan --config test-suite/config.local.json
python3 -B test-suite/bench.py doctor --config test-suite/config.local.json
python3 -B test-suite/bench.py calibrate --output runs/skillbench-calibration-first
python3 -B test-suite/bench.py smoke --config test-suite/config.local.json --output runs/skillbench-smoke-first
```

Output directories for calibration/smoke must be new. Calibration constructs reference artifacts in Python and tests graders; **smoke executes reference commands using the real Linux utilities**. Neither command uses a model API key or establishes that a skill helps an agent. Doctor runs offline and checks image/Pi availability, not authentication.

Edit `config.local.json` for your actual endpoint/model, Pi build, toolbox image and budgets. The example uses the general Z.ai API endpoint; a Coding Plan or other provider may require another endpoint. `runtime.base_url` has no `/chat/completions` suffix; `optimizer.endpoint` is the complete chat-completions URL. The example's context/output budgets are experimental caps, not a claim about the model's maximum capabilities. Credentials belong only in the environment:

```bash
read -rsp 'Z.ai test API key: ' ZAI_API_KEY
export ZAI_API_KEY
printf '\n'
python3 -B test-suite/bench.py run --config test-suite/config.local.json
```

The default plan is **24 trials: four development cases × three seeds × two conditions**. `run` prints the campaign directory. On a first deployment, reduce cases to `jq-exact-text` and repetitions to 1 to verify the actual provider/Pi interaction before the full pilot.

```bash
run_dir='runs/skillbench/REPLACE_WITH_PRINTED_CAMPAIGN'
python3 -B test-suite/bench.py report "$run_dir"
python3 -B test-suite/bench.py run --resume "$run_dir"
```

Resume uses the saved configuration and image ID. Changing controller/fixture code or frozen skill contents requires a new campaign. A stale controller lock is removed automatically only on the same POSIX host after confirming its PID is gone. PID reuse can require manual inspection. Interrupted attempts have unknown usage; a token-limited campaign stops rather than treating them as free.

## Included task coverage

| Case | Split | Independent evidence |
|---|---|---|
| `jq-exact-text` | Development | Exact UTF-8 bytes, including newline preservation |
| `jq-record-filter` | Development | Boolean versus string/null/missing distinctions, record order and duplicates |
| `jq-late-malformed` | Holdout | Late parse failure is reported; a valid prefix is not accepted as complete |
| `tar-selected-members` | Development | Exact selected members with unusual names; unrelated input preserved |
| `tar-truncated` | Holdout | Recoverable member distinguished from complete archive success |
| `sqlite-typed-export` | Development | Correct selected rows, JSON types and multiline text |
| `sqlite-schema-gap` | Holdout | Missing requested table distinguished from an empty valid result |

All fixtures are synthetic. Inputs are hashed and checked for mutation. Graders reject unbounded files, symlinks and unexpected artifact structure. Source files and answer keys are outside worker mounts. Graders check the requested machine-readable outputs; **they do not independently assess every assertion in the final prose response**.

The bundled holdouts are public code, withheld from worker mounts and optimizer requests. They provide a useful workflow boundary, not an unlimited secret benchmark. Keep fresh independently designed task families for final confirmation.

## Test selection and competition

Set `selection.mode` to `discovery` to give the worker the ordinary task prompt. Set `catalog_size` to, for example, 8, 32, or 546 to expose the target plus distractors. `distractors` is `similar` or `random`. Explicit mode prefixes the nonbaseline task with `/skill:name`; discovery mode does not. Baseline has no advertised or mounted skill packages.

Run separate campaigns at each setting. The same selected set/order is used for current/candidate within a block. Candidate wording cannot change the preselected distractor set. Selection experiments test a catalogue with the intended target present; they do not implement a production retrieval router, no-skill-needed cases, or multi-stage workflows yet. A missed read does not fail an otherwise correct task.

## Generate and test candidate improvements

First complete a development campaign. Then run a bounded search:

```bash
python3 -B test-suite/bench.py optimize \
  --config test-suite/config.local.json \
  --campaign "$run_dir" --skill jq --iterations 2
```

The optimizer gets the complete selected Markdown and bounded development result evidence. It can replace existing `SKILL.md` or reference Markdown only. It cannot change helpers, add paths, change the skill identity, delete files, edit graders, or execute commands. Responses are validated before a complete independent candidate package is written.

Each candidate is compared with the frozen current package on fresh matched development fixtures. All proposals start from the published package; previous candidate results provide additional development evidence. This is a bounded candidate search, not automatic production evolution. Proposal costs are recorded separately and counted toward configured aggregate token budgets when known. Failed/rejected paid proposals are retained in the accounting.

Candidates live under the printed optimization directory. `optimization.json` records proposals, generation usage, evaluation campaigns and comparisons. **There is no automatic promotion:** the tiny pilot cannot support a reliable general acceptance rule. Review a chosen candidate, run independent confirmation, and apply it deliberately later.

To compare a candidate manually, set `candidate_root` to the directory containing its skill folder, choose cases for that skill, and use conditions `["baseline", "current", "candidate"]`. For confirmation, select that skill's held-out case and run with `--allow-holdout`. `optimize` refuses campaigns containing held-out cases. User-selected paths in JSON are relative to the configuration file, so keep local configuration beside the example or use absolute paths.

## Budgets and evidence

`max_trials` and `max_campaign_seconds` bound campaigns. Optimization applies these across its candidate evaluations, with proposal request time included. A token budget is checked **between calls/trials**; an in-flight request can overshoot it. Provider-side spending limits remain the hard monetary control. Missing token usage stops a token-limited campaign. No USD budget is enforced from possibly inaccurate Pi price metadata.

Timeouts and output-budget exhaustion count as failed worker attempts. Infrastructure/grader errors are separately visible, with both evaluated and all-recorded success rates. Reports include all recorded attempt costs; unknown usage is never zero. Zero successes yield an undefined cost-per-success, not a cheap result. Reported API cost is an estimate, not a billing reconciliation.

Paired results show wins/losses/ties and family-macro pass-rate differences. A family bootstrap is emitted only with at least five evaluated families; the default pilot has four. Seed repeats are not new task families. No statistical-significance claim or universal optimal format follows from a small pilot.

Raw events, stderr, fixture inputs/results and private oracles stay under ignored `runs/`. Keep them private. Docker bridge networking permits outbound access; it is not an egress allowlist. The API key is in the worker environment and can be read by worker commands. Use a dedicated bounded test key and a restricted network/proxy before adversarial or externally sourced fixtures. See [runtime details](docker/README.md).

## Finish on your Linux system

1. Run unit tests, build the image, and run doctor plus CLI smoke. Resolve image/tool/Pi mismatches before model experiments.
2. Verify one real GLM baseline/current pair. Inspect model identity, raw events, credential configuration and token accounting.
3. Run the pilot and one candidate search. Inspect outcomes and failure classifications before scaling.
4. Add independent realistic cases for the tools you use most. Start with curl/SSH/protocol fixtures, tracing/core analysis, and actual cross-skill handoffs.
5. Add negative selection cases, long-session/compaction trials, prompt-injection fixtures and output-claim evaluation. The current suite does not claim those are covered.
6. Establish trusted fixture families and acceptance margins before adding automatic promotion, parallel scheduling or a recurring service.

Case extension instructions and the problem register are in [DESIGN.md](DESIGN.md). The earlier [evaluation guide](../evaluation/README.md) remains background; its authoring advice is not encoded as a passing criterion.
