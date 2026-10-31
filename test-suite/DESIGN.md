# Design and extension contract

The objective is independently verified useful task completion for a recorded Linux/Pi/GLM configuration, with acceptable resource use and task boundaries. No existing skill-writing convention is ground truth. Authoring contracts, examples, reference splitting and verbosity are experimentally changeable in candidate copies.

## Problem register

| Problem | Experiment | Pilot status |
|---|---|---|
| Similar descriptions capture or suppress selection | Matched target task with catalogue sizes and close/random distractors | Catalogue selection implemented; lexical similarity only |
| Too much guidance loaded | Compare outcome/cost and observable read calls across selections | Partial telemetry; shell reads and comprehension not inferred |
| Conflicting skills | Alone/pair/workflow comparisons, preserving task-specific constraints | Candidates can share a catalogue; no dedicated interaction cases yet |
| Incorrect commands and parser boundaries | Exact bytes/types, unusual filenames and meaningful failure variants | jq/tar/sqlite regression cases plus reconciliation/revision/WAL challenges |
| Partial output mistaken for completion | Late malformed input, truncated archive, missing schema | Held-out pilot cases |
| Missing references or resource identity | Standalone copy and contained resource checks | Structural checks implemented |
| Wrong environment assumptions | Pinned image, tool/Pi preflight, deliberate missing prerequisite fixtures | Executable discovery implemented; full compatibility cases pending |
| Process state, interactive blocking, stdin and leaked children | Noninteractive fixtures, independent state observations, supervisor cleanup | Supervisor implemented; dedicated task fixtures pending |
| Duplicate side effects after uncertain completion | Server-side request logs and idempotence fixtures | Pending |
| Stale evidence and workflow handoff errors | Artifact identity, provenance and scoped multi-step tasks | Input preservation covered; workflows pending |
| Context saturation and compaction | Long preceding histories and controlled compaction variants | Pending; pilot disables compaction |
| Excessive rituals, retries and re-reading | Content ablations with unchanged outcome graders | Initial easy pilot exposed token overhead and a baseline ceiling; per-case reporting implemented |
| Examples overfit or compression drops knowledge | New task families and independent regression cases | Three held-out families; broader coverage pending |
| Prompt injection through tool-returned data | Paired benign/adversarial data with unauthorized-action observation | Pending; do not use public bridge network for hostile testing |

Passing one task never means a whole skill or tool was validated. Catalogue overlap is not itself a defect; successful equivalent tools are allowed. No-skill performance is a real baseline, and a skill with no measured benefit need not be rewritten.

## Components

- [config.py](skillbench/config.py): validated JSON config; paths relative to the config file.
- [planning.py](skillbench/planning.py): fixed, interleaved conditions with paired seeds and distractors.
- [campaign.py](skillbench/campaign.py): frozen snapshots, trial lifecycle, controller lock, grading, resume and smoke orchestration.
- [runtime.py](skillbench/runtime.py): Docker/Pi boundary, reference execution, capped events and cleanup.
- [cases.py](skillbench/cases.py): public task requests, fixture preparation and controller-only truth/grading.
- [reference.py](skillbench/reference.py): real-CLI reference procedures used only for smoke checks.
- [reporting.py](skillbench/reporting.py): denominators, incomplete measurements and paired summaries.
- [optimizer.py](skillbench/optimizer.py): one bounded API request produces a validated independent Markdown candidate.

The controller never mounts this suite or its oracles into a worker. A private oracle may still contain information a worker can legitimately derive by inspecting its fixture; that is the task. Keeping an answer key in an adjacent readable directory would not be isolation.

## Adding a case

Register an instance in `CASES` with these fields:

```python
id: str
skill: str
family: str
split: str  # development or holdout
description: str
tools: tuple[str, ...]
```

Implement:

```python
prepare(workspace: Path, seed: int) -> dict  # private, JSON-serializable oracle
prompt() -> str                            # ordinary request and explicit output contract
grade(workspace: Path, oracle: dict) -> dict
solve(workspace: Path, oracle: dict) -> None
```

`grade` returns `passed`, named Boolean `checks`, and short `details`. `solve` constructs a known-good artifact for grader calibration; it is not worker performance or Linux command validation. Add a real CLI reference to `reference_commands` for `smoke` and Linux integration tests. Workers may solve the task differently from that reference.

Fixtures must be seed-reproducible, fresh, local to their assigned workspace and free of credentials. The request must state the substantive constraints used for grading. Do not grade undisclosed output layouts, chosen commands, read contracts, or stylistic conventions. Make unsupported outcomes distinguishable from ordinary empty results. Preserve original evidence where required by the task.

Grades should reject missing, wrong, partial and stale outputs, and accept alternative correct representations where the task permits them. Exercise modified inputs, type coercion, malformed late records, misleading partial data and path tricks as relevant. Use bounded regular-file reads; never execute candidate output as evaluator code. Stop all worker processes before inspecting their files.

New service/kernel/hardware fixtures need lifecycle and isolation work beyond the current file-fixture interface. Do not add host side effects to `prepare` to bypass that missing capability. Use dedicated service environments or VM adapters and add independent cleanup tests first.

The holdout split is enforced by the optimizer input path; this is not a benchmark secrecy guarantee against an operator reading the public source. Novel task mechanisms and new independently checked fixture families are needed for final claims. Never publish selected best-of-many development runs as a one-shot held-out gain.

## Limits and decisions left for deployment

Execution is serial. There is no service scheduler, production router, automatic acceptance threshold, model-judge grading, or automatic deployment. These omissions are deliberate boundaries of the executable pilot, not implemented features awaiting a switch.

Time/output/memory/PID caps bound ordinary worker execution. The writable bind mount has no filesystem quota; provision a dedicated quota-limited scratch volume before broad/adversarial testing. Docker isolation is not intended to test container escapes or privileged host operations. API errors, cleanup uncertainty and unknown usage must remain visible.

Pi usage is incomplete when its events omit billed operations. Model aliases can change upstream even while configuration strings stay fixed. Compare contemporaneously, retain unchanged controls, and start a new campaign when image, Pi, model settings or code changes. Final promotion needs workload-specific reliability margins and enough independent task families; the pilot reports descriptive results only.

## Research basis

These sources motivate hypotheses, not universal formatting requirements:

- [Lost in Implicit Routing](https://arxiv.org/html/2610.18522v1): relevant-skill use can decline as distractors grow; test discovery separately from execution.
- [One Skill Too Many](https://arxiv.org/abs/2610.11647): co-installed skills can interfere while superficial completion remains unchanged.
- [Agent Skills Can Be Harmful](https://arxiv.org/html/2608.11888v1): content and excess procedure matter alongside context length; selected attributed failures are not prevalence estimates.
- [SkillsBench](https://arxiv.org/abs/2602.12670): paired outcomes and deterministic verifiers for skill utility.
- [SkillRevise](https://arxiv.org/abs/2606.01139) and [GEPA](https://arxiv.org/abs/2507.19457): execution feedback can guide text revisions; independent confirmation remains necessary.
- [AgentDojo](https://arxiv.org/abs/2406.13352): untrusted tool output needs explicit behavioral tests.

No cited result establishes performance of this library with GLM-5.3 Flash/Pi on the deployment image.


## Challenge extension validation

The original four development cases remain controls. New challenge cases add independent mechanisms while preserving tool-neutral outcome grading. `Case.tier` is an experimental label; `split` remains the optimizer evidence boundary. A challenge is not assumed hard until contemporaneous baseline trials establish failures or material resource demands.

The SQLite fixture captures a quiescent, coherent committed DB/WAL pair before closing its construction connection. WAL salts and rolling checksums are normalized from the seed according to the [SQLite file-format specification](https://www.sqlite.org/fileformat2.html#checksum_algorithm), making within-environment byte snapshots repeatable. Both host SQLite and the pinned container's SQLite must read the normalized WAL correctly. Unit tests prove that copying only the main database gives stale results. No live service or writer is left running in the fixture.

Calibration constructs outputs from private generation state. Separate CLI references derive answers from visible inputs; they do not import the builder or read its oracle. Negative controls reject first/last/concatenated archive occurrences, accepted prefixes of rejected shards, typed-identity collapse and stale database exports. Changing fixture or controller code requires a new campaign as before.
