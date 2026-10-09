# Tool skill schema, MVP v0.4

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

These are content considerations, not mandatory headings. A single correction may need only a paragraph and example. A debugger investigation may need a sequence and decision table. Skip a tool if no useful guidance gap has been identified. There are no tiers, recipe quotas or word-count targets.

Keep meaningful limitations visible. If a workflow is untested, a short note is sufficient; do not make the worker read an authoring report. Remove repeated scope statements, general shell lessons and instructions that merely restate the harness's rules.

## Optional supporting material

Keep the ordinary workflow in `SKILL.md`. Add a reference only for substantial conditional detail, or a script when repeated executable logic warrants one. All required resources must remain inside this skill's folder when copied alone.

Source evidence can be a couple of links inline or a short `references/sources.md` for maintainers. Record useful source sections and version/review context. Detailed claim maps are optional for disputed or complex guidance. Sources must support commands and interpretations even when no separate source file is needed. Raw input stays in ignored `work/`; retain enough durable evidence to review consequential guidance later.

## Review and testing

Check commands and consequential interpretations against applicable documentation or observations. A captured help screen, an executed procedure and a successful agent investigation establish different things. Report exactly what was reviewed or run, with versions and case scope where relevant. One local success does not establish universal compatibility.

Use a focused check for a small correction. For a diagnostic workflow, include an inconclusive case when it tests a real decision. The [evaluation guide](../evaluation/README.md) explains how to compare outcomes and cost against a baseline. Add only material that earns its place.
