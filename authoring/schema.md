# Tool skill schema, MVP v0.5

The default deliverable is **one independently installable `skills/<name>/SKILL.md`**. Use the [GDB skill](../skills/gdb/SKILL.md) as an example, not a required length or layout.

## Required format

Use the standard [Agent Skills format](https://agentskills.io/specification): YAML frontmatter with `name` and `description`, followed by Markdown instructions. The name matches the folder; use lowercase letters, digits and hyphens. Describe the tool's actual supported tasks and symptoms. Keep those fields on one line each for the repository's simple checker.

## What belongs in the instructions

Include only what helps a capable agent use this tool better:

| Content, when relevant | Purpose |
|---|---|
| Applicability, required inputs and important version/environment conditions | Choose and apply the right guidance. |
| Useful commands or an adaptable procedure | Execute with defined inputs and understood effects. |
| Interpretation, pitfalls and next checks | Continue an investigation and recover from misleading or incomplete results. |
| Evidence sufficient to finish | Answer the user's question accurately. |

These are content considerations, not mandatory headings. Describe the tasks actually supported; a narrow procedure does not establish general mastery of the tool. Before expanding an existing skill, identify the task or decision the new material improves. Skip additions that repeat existing coverage. There are no tiers, recipe quotas or word-count targets.

## Worked guidance

Connect the situation, command, relevant result, interpretation and next action when teaching a workflow. Use short output excerpts or a decision table where they clarify what to do. A small correction may need only a paragraph; a complex investigation can need several distinct examples. More switch combinations alone do not improve coverage.

Label invented output as **illustrative**. Identify the fixture/environment for captured output in the maintenance record; do not present a hypothetical transcript as an executed test. Keep example-specific names, addresses and results visibly separate from reusable commands. Include a failure or incomplete-evidence branch when it changes the next decision.

Keep operational limits beside the affected procedure: supported versions/formats, missing prerequisites and what the result can establish. Review dates, originating PDF pages and historical test status belong in maintenance records rather than routine worker footers. If an unresolved uncertainty affects use, state the specific uncertainty and what would resolve it. Remove generic warnings and repeated harness policy.

## Optional supporting material

Keep the ordinary workflow in `SKILL.md`. Add a reference only for substantial conditional detail, or a script when repeated executable logic warrants one. All required resources must remain inside this skill's folder when copied alone.

Keep primary-documentation links in the skill when they help a worker resolve an option, version difference or unexpected result. Store the fuller source trail, review date and test history in existing intake reports and `docs/validation.md`, identifying the affected skill. Preserve source-to-skill mapping and any required attribution when relocating old footers. Workers must not depend on these repository maintenance files. No per-skill provenance file or mandatory bibliography is required. Raw input stays in ignored `work/`.

## Review and testing

Check commands and consequential interpretations against applicable documentation or observations. A captured help screen, an executed procedure and a successful agent investigation establish different things. Report exactly what was reviewed or run, with versions and case scope where relevant. One local success does not establish universal compatibility.

Use a focused check for a small correction. For a diagnostic workflow, test the supported conclusion and a meaningful incomplete-evidence case. The [evaluation guide](../evaluation/README.md) explains how to compare outcomes and cost against a baseline. Record those results in maintenance records; packaging checks cannot establish worker usefulness.
