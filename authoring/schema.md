# Tool skill schema, MVP v0.8

The default deliverable is **one independently installable `skills/<name>/SKILL.md`**. Use the [GDB skill](../skills/gdb/SKILL.md) as an example, not a required length or layout.

## Target environment

These skills target **one Linux distribution/image that the user deploys and controls**, including binary placement. Independent packaging serves different workers/harnesses; it does not require a generic multi-distribution compatibility layer.

There are two passes: source ingestion improves selection and operational guidance now; a later agent on the Linux image discovers actual binaries and enriches the relevant skill references with verified absolute invocations, versions and consequential option differences. Do not block current ingestion on that future pass or invent target facts from this Windows host.

## Purpose: selection and on-demand operational knowledge

Help a capable CLI worker recognize an existing tool that fits its task, then supply the operational knowledge needed to use it well. Prefer the installed tool's supported capability over reimplementing it; small glue scripts or another approach remain reasonable when the tool does not fit. A skill's presence alone does not establish that the binary is installed.

Workers operate within a task graph, revisit skills and can adapt their investigation. Teach useful conditions, system behavior, observations and next decisions; do not prescribe a complete investigation or duplicate the task graph. A supported partial result can be enough for the current task. Preserve essential ordering where correctness depends on it, while leaving incidental command choices flexible.

The entrypoint carries selection, a useful starting point and routes to deeper tasks. Package-local references carry substantial conditional procedures, option choices, examples/output interpretation and domain detail. Keep a short cohesive workflow inline: neither an empty link directory nor a reference for every paragraph improves use.

## Coverage decisions during ingestion

Tool discovery and task depth are separate acceptance questions. An actively used tool with a useful, verifiable task deserves its own discoverable package even when another tool serves a similar purpose. Do not reject it because its invocation is short, its flags are familiar, or accepting it would not introduce a novel technique. A name-only mention still does not justify inventing a workflow. Accumulate evidence across earlier sources before deferring a repeatedly demonstrated tool.

For each tool actually used in the source, account for the demonstrated task in the existing intake report: already covered (identify its skill/section), added/enriched, or deferred with a concrete missing fact. Group incidental shell plumbing where appropriate; no new runtime fields or per-skill ledger are required. Reading all PDF pages and covering its useful operational lessons are different claims. A no-change outcome must explain where the useful task is already supported or why it cannot yet be supported.

Do not let a concise entrypoint erase domain knowledge. Preserve useful prerequisites, reasoning, command choices, successful and failed results, recovery and next decisions in conditional references. If the source demonstrates an operational action, do not silently replace that task with merely inspecting whether the action might be possible. Scope the actual procedure and its effects, or record the specific evidence missing. A Linux CLI that operates on Windows services remains in scope.

Restrictions on authoring execution govern what the ingestion agent may run. They do not by themselves prohibit documenting authorized administration or security-testing procedures. Documentation-reviewed commands can be accepted with honest runtime limitations; an unavailable Linux fixture is not a blanket rejection gate. Require a fixture before claiming behavior that documentation cannot establish, rather than before admitting the entire tool. Remove source secrets and target-specific assumptions, not the operational lesson.

Reject duplicate text, not useful overlapping tools. Keep exclusions such as missing command semantics, an unidentified implementation, or a genuinely GUI-only workflow specific and actionable. Avoid a generic requirement for a broader workflow, complete tool mastery, or extra examples. Packaging checks verify packaging; only a source-to-task coverage review and eventual worker trials assess whether knowledge was retained and helps the worker.

## Required format

Use the standard [Agent Skills format](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, followed by Markdown instructions. The name matches the folder; use lowercase letters, digits and hyphens. Describe the tool's actual supported tasks and symptoms. Keep those fields on one line each for the repository's simple checker.

## What belongs in the instructions

Include only what helps a capable agent use this tool better:

| Content, when relevant | Purpose |
|---|---|
| Applicability, required inputs and important version/environment conditions | Choose and apply the right guidance. |
| Non-obvious system model or discriminating observation | Avoid a likely mistake and choose a useful next check. |
| Useful commands or an adaptable procedure | Execute with defined inputs and understood effects. |
| Interpretation, pitfalls and next checks | Continue an investigation and recover from misleading or incomplete results. |
| Evidence sufficient to finish | Answer the user's question accurately. |

These are content considerations, not mandatory headings. Describe the tasks actually supported; a narrow procedure does not establish general mastery of the tool. Before expanding an existing skill, identify the task or decision the new material improves. Skip additions that repeat existing coverage. There are no tiers, recipe quotas or word-count targets.

## Make the first read sufficient to choose and load the task

The description is discovery text: lead with the supported task and useful trigger, not instructions that the worker must execute. Put an activation contract near the top of the body, before procedure commands. It tells the worker to read the **entire SKILL.md before acting**, and makes applicable prerequisites, required steps/resources and completion evidence discoverable. Loading or invoking a skill does not itself establish that the model followed it. Complete, current material already available in context need not be re-read mechanically; recheck environment facts when context is missing, has changed or an observation contradicts them, not on every command.

For several workflows or substantial resources, add a compact task map or checklist. Distinguish:

- **Required:** the steps and resources needed for the selected task, including an exact skill-relative helper/template path when it is part of the workflow. State when to use it and what result it produces; do not replace a required supplied helper silently.
- **Conditional:** name the situation that requires the section/reference, with a direct link. Read that material completely before its procedure, including any dependencies it requires. Keep unrelated references unloaded. An external documentation link for troubleshooting is not automatically a mandatory read.
- **Completion:** identify the requested evidence or artifact. Report a missing prerequisite, failure or unresolved step honestly; never convert a summary of intended work into a successful result. For a multi-step checklist, record done with evidence, not applicable with a reason, or blocked with the missing requirement. Do not invent a separate report file for a task that does not need one.

A short single-task skill may express this in two or three sentences; do not add empty checklists or a standard ritual. Keep shared requirements early and specific caveats beside their command. Whole-entrypoint reading remains affordable by moving substantial alternative workflows into conditional files within the same skill, when useful.

During ingestion/review, inspect only the **first 150 lines**, including frontmatter, and ask whether every supported workflow and required resource can be found from there. Put the route near the beginning, well before line 150. Then read the full skill and selected references to check for hidden requirements. Treat 150 as our conservative partial-read review boundary, **not a documented universal harness cutoff**, a target length or proof of compliance. Do not compress commands onto long lines to meet it. See [loading behavior and rationale](../docs/harnesses.md#skill-loading-and-the-first-read).

## Worked guidance

Connect the situation, command, relevant result, interpretation and next action when teaching a workflow. Use short output excerpts or a decision table where they clarify what to do. A small correction may need only a paragraph; a complex investigation can need several distinct examples. More switch combinations alone do not improve coverage.

Label invented output as **illustrative**. Identify the fixture/environment for captured output in the maintenance record; do not present a hypothetical transcript as an executed test. Keep example-specific names, addresses and results visibly separate from reusable commands. Include a failure or incomplete-evidence branch when it changes the next decision.

Keep operational limits beside the affected procedure: supported versions/formats, missing prerequisites and what the result can establish. Review dates, originating PDF pages and historical test status belong in maintenance records rather than routine worker footers. If an unresolved uncertainty affects use, state the specific uncertainty and what would resolve it. Remove generic warnings and repeated harness policy.

## Optional supporting material

Keep enough in `SKILL.md` to select the tool and start the common task. Put substantial alternative procedures or deeper domain knowledge into descriptive `references/<task>.md` files. Link each from the opening with the situation that requires it. A selected reference must include its necessary inputs, command/options, consequential interpretation and stopping/continuation conditions without depending on a sibling skill. Do not duplicate the whole entrypoint or force unrelated reference reads. Scripts remain optional and should save useful repeated execution.

During the later Linux pass, put stable facts about the controlled image directly in the tool's existing relevant reference or a concise `references/environment.md` when shared across its tasks. Record the actual absolute executable/interpreter invocation, relevant version/options and real constraints; link that file near the entrypoint when it exists. Reuse context already available and recheck when the image changes or observed behavior disagrees. Do not create empty required references or dangling links now.

These shared image facts can be committed with the skill and distributed to workers. Node-specific exceptions, secrets, raw inventory and captures stay in ignored `work/` or `runs/`; workers must not depend on authoring notes. Keep the complete skill folder self-contained. No separate host-copy/overlay mechanism is needed for this controlled target. The saved [Linux adaptation prompt](adapt-to-host.prompt.md) describes the later pass.

Until that pass, commands may use the recognizable tool name or a defined executable variable. Once verified, use the chosen absolute invocation consistently, including interpreter/wrapper arguments where applicable. A missing tool is recorded as a capability gap; installation is a separate action.

Keep primary-documentation links in the skill when they help a worker resolve an option, version difference or unexpected result. Store the fuller source trail, review date and test history in existing intake reports and `docs/validation.md`, identifying the affected skill. Preserve source-to-skill mapping and any required attribution when relocating old footers. Workers must not depend on these repository maintenance files. No per-skill provenance file or mandatory bibliography is required. Raw input stays in ignored `work/`.

## Conform existing skills when revisiting them

During ingestion, review the existing package for the operational task before adding material. Bring it into this schema while it is in scope: correct or merge overlapping advice, trim filler and repeated history, tighten discovery text, add missing early routes, and move substantial independent branches into conditional references where useful. Do not merely append the new source's example. Preserve useful earlier workflows and attribution; remove weaker text only when the evidence supports the replacement.

Choose correction, merge/replacement, extension, conditional reference, new independent skill or no runtime change. A fully reviewed source with no useful new lesson is valid; an already conforming skill needs no cosmetic rewrite. Record the schema version and skills actually reviewed for conformity in the existing intake report, including unchanged ones. At batch completion, identify skills not yet reviewed; do not claim the whole library migrated because the new authoring rules exist. No per-skill compliance file or new mandatory YAML field is needed.

Keep meaningful cross-tool lessons in the intake report when they do not fit one tool. Do not recreate an umbrella skill or add a task skill without a concrete supported gap.

## Review and testing

Check commands and consequential interpretations against applicable documentation or observations. A captured help screen, an executed procedure and a successful agent investigation establish different things. Treat source observations, the writeup author's explanation and verified tool semantics separately. Report exactly what was reviewed or run, with versions and case scope where relevant. One local success does not establish universal compatibility.

Use a focused check for a small correction. For a diagnostic workflow, test the supported conclusion and a meaningful incomplete-evidence case. The [evaluation guide](../evaluation/README.md) explains how to compare outcomes and cost against a baseline. Record those results in maintenance records; packaging checks cannot establish worker usefulness.
