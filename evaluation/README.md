# Evaluate useful behaviour

Use two distinct checks: whether the commands work in the target environment, and whether an agent using the skill completes the task more reliably. A structural check cannot establish either.

First check packaging: copy only the selected `skills/<name>/` folder into an isolated installation and verify all required resources are available. Keep the rest of the repository and other skills out of the agent's context. The repository tests exercise local link portability; actual discovery and task completion still require the harness checks below.

## Minimum per-tool check

For tier A, choose one realistic task with a known result and one materially different failure or incomplete-evidence variant. Use [case.template.md](case.template.md). A case may be small; its outcome must be observable.

For tier B, check the command semantics and run one focused fixture for the correction when available. Add a failure/control variant when needed to establish that correction's meaning. Record the exact limited coverage; one fixture is not verification of the whole tool. Tier C is deferred and has no installed skill to test; observed baseline failures should trigger reconsideration. Agent evaluation remains a separate status for all published skills.

Use an isolated fixture appropriate to the tool. A directory or container may suffice for file processing. Kernel tracing, systemd, capabilities, and live debugging may require a suitable VM or host; container success does not demonstrate host compatibility.

For each executed case, retain the task, tool/environment versions, exact commands, output and exit status, relevant artifacts, result, and cleanup. The reference's execution record names the cases that actually ran.

## GDB starter: proposed cases

These cases have not been constructed or executed:

| Case | Fixture | Expected behaviour |
|---|---|---|
| GDB-CORE-01 | A small native program with a known assertion failure, matching debug executable, source, and an existing core. | Establish the artifact relationship, identify the relevant application frame, inspect state, and explain the supported cause with evidence. |
| GDB-CORE-02 | A comparable core with its matching debug artifacts deliberately unavailable. | Detect the evidence limitation, preserve what can be established, and request or identify the missing artifacts without inventing a source-level cause. |

Keep the fixture's known cause and evaluator rubric out of the agent's inputs. Give the agent the skill, the user request, and the ordinary artifacts a real investigation would have.

## Does the skill help?

Within one harness, compare:

- **Baseline:** the same model, shell access, ordinary help/man pages, and the same permitted documentation access.
- **Skill:** that same setup with only the proposed tool's independent skill installed.

When assessing the optional shell profile, use three conditions: baseline, profile only, and the same profile plus skill. This separates the effect of execution defaults from the effect of written guidance. Record the actual applied profile variables/instructions. Retain the baseline-versus-skill comparison when no profile is being assessed.

Use fresh sessions and reset fixtures. Keep model, reasoning settings, permissions, tool versions, prompt, and time/token budgets matched. Do not let the baseline read the skill repository. Give both conditions the same network/documentation policy.

Run a few repeats or related unseen variants before attributing an improvement to the skill. Report how many runs occurred; a single good example is an initial signal. If different models are used across harnesses, report those results separately rather than treating them as a controlled harness comparison.

Score:

| Measure | Observable evidence |
|---|---|
| Correct outcome | The fixture's result or evidence limit was correctly established. |
| Evidence quality | Claims follow from the collected artifacts; unsupported causal claims are counted. |
| Recovery | The agent responds usefully to the error/incomplete-evidence variant. |
| Efficiency | Elapsed time, model usage if available, and failed/repeated/unnecessary commands. |
| Scope | Operations remain within the task and fixture; relevant cleanup is complete. |
| Discovery | The right standalone skill loads for an ordinary request and can be explicitly invoked. |

Do not grade on matching prescribed wording or a fixed command sequence when another method reaches the correct outcome.

## What the result changes

- Command failure: fix or narrow the procedure and retest that part.
- Wrong conclusion from correct output: repair interpretation or the verification criterion.
- Failure to load the relevant skill: revise that skill's description and test both the tool name and ordinary symptoms.
- Competing or crowded descriptions: narrow overlapping scopes and install the subset relevant to the worker. Preserve independent tool packages.
- No measurable benefit: shorten the skill, change the targeted task, or defer that tool.
- Repeated session-related failures: fix the harness capability or use a valid batch workflow; more prose is unlikely to supply missing process control.

Before claiming support for all three harnesses, exercise discovery and one representative procedure in each actual Linux installation. The current starter has not passed those tests.

## Authoring helper checks

The capture helper has separate subprocess tests in [test_capture_help.py](../tests/test_capture_help.py). Passing those tests validates capture/error handling in the tested environment, not the Linux procedures or their usefulness to an agent. See the [capture guide](../authoring/capture-help.md) for the command and limits.
