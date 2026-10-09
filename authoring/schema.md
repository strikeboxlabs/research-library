# Tool reference schema, MVP v0.2

Use a standard `SKILL.md` wrapper plus Markdown references. This is an authoring contract, with no custom parser or one discovered skill per executable.

## Discovery wrapper

The actual [entrypoint](../skills/linux-cli/SKILL.md) uses standard YAML fields `name` and `description`. Name the symptoms, tasks and tools the installed content covers. Avoid wording that requires the model to recognise that it needs help. Keep the description aligned with accepted coverage in the index; future tools belong in the planning backlog.

The current description names native crashes, existing cores, stack traces and GDB. It does not advertise the planned service, network or performance workflows. The name matches the skill folder. See the [Agent Skills specification](https://agentskills.io/specification).

Use one entrypoint initially. Domain playbooks can be references inside it; they do not require separate discoverable skills. At roughly 30-40 indexed tools, review discovery results and context cost. This is a checkpoint, not an automatic split. Split earlier or later when symptom-based evaluation shows missed or competing routes, and keep each resulting skill self-contained.

## Choose the coverage tier

| Tier | Use when | Required deliverable | Why this effort is justified |
|---|---|---|---|
| A: full card | A task needs several decisions, non-obvious interpretation, recovery or persistent-session handling. | Full card, provenance companion, index row, and a proposed outcome/failure evaluation case. | The agent needs an investigation it can continue and verify. |
| B: delta card | Ordinary usage is familiar but a specific flag, failure, effect or variant repeatedly causes mistakes. | Short card, compact provenance companion, index row, and a focused check of the correction. | Record the knowledge that changes behaviour without repeating a tutorial. |
| C: index only | No useful guidance gap has been identified for the intended tasks. | Index row with selection terms, bounded scope and `No card; ordinary tool usage` in the reference cell. | Avoid writing material the agent already uses competently. This is not a verification claim. |

Use observed baseline failures where available. Otherwise record that the tier is provisional. Familiarity alone does not prove safe composition or correct interpretation. Promote a tool when failures justify a card; shorten or demote a card with no demonstrated value. The suggested 40 A / 100 B / 60 C distribution is a planning estimate, not a quota.

The runtime index is the single maintained tier catalogue. Keep candidate tools outside it until accepted; no second hand-maintained status database is required.

## Tier A contract

Use [tool-card.template.md](tool-card.template.md).

| Section | Minimum useful content | Reason |
|---|---|---|
| Identity and selection | Executable, aliases, applicable question and a meaningful boundary. | Find and choose the tool. |
| Preconditions | Inputs, relevant environment/privileges/effects and execution mode. | Avoid applying a correct command in the wrong setting. |
| Procedure | A practical outcome, defined inputs, concrete actions, decision branches and completion evidence. | Support a sustained investigation. |
| Failure and recovery | Likely failure, a discriminating check and a next action. | Recover without repeating commands or guessing. |
| Verification and gaps | Three independent statuses, material limits and a provenance link. | Keep uncertainty visible while detailed sources remain available on demand. |

Every procedure retains these named items:

1. **Question:** What must be established?
2. **Inputs and effects:** What values, paths and artifacts are used, and what can change?
3. **Actions:** Supported commands or an adaptable sequence, with defined and quoted inputs.
4. **Observe and decide:** Observation, meaning and limits, next action. Include a relevant inconclusive branch.
5. **Finish when:** Evidence sufficient to answer, or the specific missing artifact/check that blocks a conclusion.

One well-supported task is enough. Add procedures only for distinct useful outcomes. A domain playbook uses the same decision structure, links to accepted tool cards, and explains why an observation calls for another tool. Do not introduce a fixed sequence solely to include more tools.

## Tier B contract

Use [delta-card.template.md](delta-card.template.md). Keep identity/scope, the behaviour-changing guidance, relevant failure/recovery or version differences, and the same verification section with a provenance link. A complete procedure is optional. If a recommendation makes a diagnostic claim or changes important state, include its limits, relevant effect and outcome check even in a short card.

Use a small source packet and a compact source-to-claim map. Review semantics and run one focused fixture for the correction when available. Add a failure/control variant when the correction depends on that distinction. Do not demand a full multi-workflow authoring report or invented evaluation cases for an elementary correction. Keep execution `not-run` when no fixture ran, and record only the coverage that did run.

## Sources loaded on demand

Put durable citations, source locators and claim mappings in `references/provenance/<tool>.md`, using [provenance.template.md](provenance.template.md). Link that file from the card's verification section. Both ship inside the portable skill. Raw captures and drafts stay in ignored `work/`; durable evidence must not depend on an ignored path.

Use stable IDs S1, S2, etc. in the companion and map them to commands and consequential interpretation/recovery guidance. The runtime card does not need a marker on every row. Keep an inline citation only when its immediate availability materially helps the investigation. Distinguish documented behaviour, a source's observed example and a newly assembled procedure or inference.

For every option, subcommand and debugger command, record a supporting capture or applicable manual section, including version scope when known. A spelling match does not validate meaning, combinations, defaults or interpretation. Rolling documentation can support a source-reviewed draft; an unknown relationship to the installed version remains a gap. Capture labels are documentation evidence, not tested workflow versions. See [capture guidance](capture-help.md).

## Three independent verification records

- **Source review:** `pending` or `checked`, with date and scope actually reviewed.
- **Execution:** `not-run`, `partial`, `passed` or `failed`, naming actual cases, environment/version, date and durable evidence summary when available.
- **Agent evaluation:** `not-run`, `partial`, `passed` or `failed`, with the observed evaluation scope and result when available.

`passed` applies only to named cases. A tool can have checked sources, failed execution and no agent evaluation. Never convert a help capture, review date, link check or successful command into a broader verification claim. Tier C does not have a card or imply these checks occurred.

## Size and limits

Write only material that changes a capable agent's choices. A cards will usually be longer than B cards; word counts are editorial aids, not gates. Do not impose a recipe quota. Common execution guidance belongs in the shared runtime reference; optional user-side defaults belong outside the portable skill in `profile/`.

This schema supplies no automatic freshness, universal compatibility or guarantee of good reasoning. Sources, procedure execution and discovery still need the [evaluation process](../evaluation/README.md). Defer formal dependency graphs, embeddings, numerical confidence and a large environment matrix until observed problems justify them.
