# Adapt an independent tool skill to this Linux host

Use from an agent session at the repository root. Supply the tool name and the scope of any permitted disposable tests. The agent may gather environment facts itself; the user does not need to fill the machine template manually.

---

Adapt the selected tool's guidance to the actual Linux environment available to this agent.

Read `AGENTS.md`, `authoring/schema.md`, the selected `skills/<name>/SKILL.md`, its own `references/provenance.md`, and the evaluation guide. Preserve the question/decision/completion structure, independent packaging and three separate verification statuses.

1. Record the relevant OS/kernel/architecture, selected executable path, implementation/version, shell/session model and task-relevant permissions in ignored `work/machine.md`. Use `authoring/local-machine.template.md` if needed. Inspect from the agent's command environment, not assumptions about an interactive login shell. Never dump secrets or the complete environment.
2. Capture the selected tool's version/help using `scripts/capture_help.py` where its known informational invocations are suitable. Inspect capture status and streams. Supplement with built-in command help or version-matched manuals for subcommands and debugger commands absent from CLI help.
3. Check each included command and consequential interpretation against this evidence. Distinguish an unsupported switch, absent binary, missing input/artifact and missing runtime capability. Do not infer compatibility from a version string alone or invent version cutoffs.
4. Handle personal binary locations through an explicit selected executable or the account's launch environment. Keep local paths in machine notes. Put reusable implementation/version conditions and supported alternatives in the portable skill, backed by provenance. Describe any proposed launch setting without changing global configuration unless separately authorised.
5. Run only tests within the user-supplied scope. For a full procedure, use a realistic case with a known outcome and a meaningful incomplete-evidence/failure variant when feasible. Save exact commands, stdout/stderr, exit codes and relevant artifacts under `runs/`. If the fixture cannot run, record the specific limitation and preserve `not-run` or the actual partial result.
6. Update source review, procedure execution and agent evaluation independently. Preserve historical case results and clearly scope new ones to this environment. A direct fixture run is not automatically an agent evaluation; a separate agent evaluation needs its own inputs, outcome and evidence, with the answer key withheld.
7. Retain durable non-sensitive findings in the skill's provenance and repository evaluation material. Keep raw captures and local notes ignored. Run repository checks and inspect the diff. If coverage changes, update this skill's description and README catalogue row. Confirm the folder works when copied alone; do not introduce shared runtime or sibling-skill dependencies.

Report the environment selected, files changed, observed tests and unresolved gaps. Do not claim full-tool coverage or universal compatibility from one case. Follow the user's requested Git workflow; absent an explicit request, leave edits available for review without committing or pushing.

---
