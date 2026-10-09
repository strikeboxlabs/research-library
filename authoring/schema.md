# Independent tool skill schema, MVP v0.3

Each accepted tool skill is a standard, self-contained `skills/<name>/` folder with its own `SKILL.md`. Install any folder independently. Shared schemas, prompts and checks stay in this repository for authors; installed skills do not need them.

## Packaging and discovery

The [GDB skill](../skills/gdb/SKILL.md) is the first example. Its standard YAML fields `name` and `description` identify the tool and supported tasks. Use the executable's familiar name when suitable, match the folder name, and describe the actual symptoms and capabilities. A tool-named skill can have narrow coverage: `gdb` currently covers existing native core dumps only. Do not advertise unimplemented modes.

Use the [Agent Skills specification](https://agentskills.io/specification). For this MVP, keep `name` and `description` on one line each so the repository's simple checker can validate them. No harness-specific metadata is required.

Put the useful procedure or correction directly in `SKILL.md`. A short skill needs no routing file. Longer skills can link to substantial, tool-specific modes under their own `references/`; sources belong in `references/provenance.md` and are read when needed. Keep every required file inside the skill folder. Do not link to sibling skills or repository-level runtime instructions as dependencies. Include a small repeated instruction locally when it is essential to portability; omit generic CLI teaching.

The repository README lists available skills for humans and installers. An installed skill must work without that catalogue, the rest of the checkout, an umbrella skill, or other installed skills. If a real multi-tool workflow later deserves its own skill, give it its own name and self-contained instructions; it does not become a parent of the individual tool skills. Document required executables as environment prerequisites.

## Choose the coverage tier

| Tier | Use when | Required deliverable | Why this effort is justified |
|---|---|---|---|
| A: full skill | A task needs several decisions, non-obvious interpretation, recovery or persistent-session handling. | Standalone `SKILL.md`, provenance companion, README catalogue row, and a proposed outcome/failure evaluation case. | The agent needs an investigation it can continue and verify. |
| B: compact skill | Ordinary usage is familiar but a specific flag, failure, effect or variant repeatedly causes mistakes. | Standalone `SKILL.md` with a narrow description and correction, compact provenance, catalogue row, and focused check. | A small skill is independently reusable too. |
| C: defer | No useful guidance gap has been identified for the intended tasks. | A short reason in the source intake or authoring report; no installed folder and no accepted catalogue row. | Avoid generating empty skills or material the agent already uses competently. This is not a verification claim. |

Use observed baseline failures where available. Otherwise record that the tier is provisional. Familiarity alone does not prove correct interpretation. Promote a deferred tool when failures justify guidance; shorten or defer a skill with no demonstrated value. Tiers determine authoring depth, not packaging or a dependency hierarchy. Do not turn a goal of researching 200 tools into a quota of 200 installed skills.

The README catalogue lists accepted skills and their bounded coverage. Keep drafts and candidate tools in authoring material, outside `skills/`. Verification records live in each skill; no second hand-maintained verification database is required.

## Tier A contract

Use [skill.template.md](skill.template.md) as `skills/<name>/SKILL.md`. Fill its frontmatter as well as its body.

| Section | Minimum useful content | Reason |
|---|---|---|
| Identity and selection | Executable, aliases, applicable question and a meaningful boundary. | Find and choose the tool. |
| Preconditions | Inputs, relevant environment/privileges/effects and execution mode. | Avoid applying a correct command in the wrong setting. |
| Procedure | A practical outcome, defined inputs, concrete actions, decision branches and completion evidence. | Support a sustained investigation. |
| Failure and recovery | Likely failure, a discriminating check and a next action. | Recover without repeating commands or guessing. |
| Verification and gaps | Three independent statuses, material limits and a skill-local provenance link. | Keep uncertainty visible while detailed sources remain available on demand. |

Every procedure retains these named items:

1. **Question:** What must be established?
2. **Inputs and effects:** What values, paths and artifacts are used, and what can change?
3. **Actions:** Supported commands or an adaptable sequence, with defined and quoted inputs.
4. **Observe and decide:** Observation, meaning and limits, next action. Include a relevant inconclusive branch.
5. **Finish when:** Evidence sufficient to answer, or the specific missing artifact/check that blocks a conclusion.

One well-supported task is enough. Add procedures only for distinct useful outcomes. A multi-tool workflow uses the same decision structure and explains why an observation calls for another tool. Its required instructions must ship in its own folder. Do not introduce a fixed sequence solely to include more tools.

## Tier B contract

Use [delta-skill.template.md](delta-skill.template.md) as `skills/<name>/SKILL.md`. Keep precise frontmatter, identity/scope, the behaviour-changing guidance, relevant failure/recovery or version differences, and the same verification section with a provenance link. A complete procedure is optional. If a recommendation makes a diagnostic claim or changes important state, include its limits, relevant effect and outcome check even in a short skill.

Use a small source packet and a compact source-to-claim map. Review semantics and run one focused fixture for the correction when available. Add a failure/control variant when the correction depends on that distinction. Do not demand a full multi-workflow authoring report or invented evaluation cases for an elementary correction. Keep execution `not-run` when no fixture ran, and record only the coverage that did run.

## Sources loaded on demand

Put durable citations, source locators and claim mappings in the individual skill's `references/provenance.md`, using [provenance.template.md](provenance.template.md). Link it from `SKILL.md` with `references/provenance.md`; link back with `../SKILL.md`. Both files ship inside that skill. Raw captures and drafts stay in ignored `work/`; durable evidence must not depend on an ignored path.

Use stable IDs S1, S2, etc. in the companion and map them to commands and consequential interpretation/recovery guidance. The runtime skill does not need a marker on every row. Keep an inline citation only when its immediate availability materially helps the investigation. Distinguish documented behaviour, a source's observed example and a newly assembled procedure or inference.

For every option, subcommand and debugger command, record a supporting capture or applicable manual section, including version scope when known. A spelling match does not validate meaning, combinations, defaults or interpretation. Rolling documentation can support a source-reviewed draft; an unknown relationship to the installed version remains a gap. Capture labels are documentation evidence, not tested workflow versions. See [capture guidance](capture-help.md).

## Three independent verification records

- **Source review:** `pending` or `checked`, with date and scope actually reviewed.
- **Execution:** `not-run`, `partial`, `passed` or `failed`, naming actual cases, environment/version, date and durable evidence summary when available.
- **Agent evaluation:** `not-run`, `partial`, `passed` or `failed`, with the observed evaluation scope and result when available.

`passed` applies only to named cases. A tool can have checked sources, failed execution and no agent evaluation. Never convert a help capture, review date, link check or successful command into a broader verification claim. Tier C does not have a skill or imply these checks occurred.

## Size and limits

Write only material that changes a capable agent's choices. A skills will usually be longer than B skills; word counts are editorial aids, not gates. Do not impose a recipe quota. Keep essential execution facts local to the skill; optional user-side defaults remain separate in `profile/` and are never a skill dependency.

Independent packages let each worker install only the relevant subset. Many installed descriptions still cost discovery context, so keep them precise and test ordinary symptom requests as well as explicit invocation. Catalogue size is not a reason to merge tool skills into an umbrella.

This schema supplies no automatic freshness, universal compatibility or guarantee of good reasoning. Sources, procedure execution and discovery still need the [evaluation process](../evaluation/README.md). Defer formal dependency graphs, embeddings, numerical confidence and a large environment matrix until observed problems justify them.
