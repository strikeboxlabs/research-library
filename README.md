# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md).** It covers the Linux checkout, installing selected skills in Pi/Claude Code/Codex, adapting them to the actual machine, and creating a new skill from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Independent Linux tool skills

Design date: 2026-10-09. Schema: v0.3. Target: agents that already use the Linux CLI competently.

Each tool's guidance is its own installable skill under `skills/<name>/`. The useful procedure goes directly in that skill's `SKILL.md`, with its own discovery description. Sources and any substantial optional detail stay inside that same folder. Copy or link the folders a worker needs; each works independently of the rest of this repository.

There is no umbrella skill, required runtime index or shared runtime dependency. Shared authoring prompts, templates and checks stay at repository level for maintainers. Progressive loading still works inside an individual skill: the agent discovers its description, reads its instructions, then consults supporting references when needed. See the [Agent Skills specification](https://agentskills.io/specification).

## Available skills

| Skill | Tier | Current scope |
|---|---|---|
| [gdb](skills/gdb/SKILL.md) | A | Examine an existing native core dump with its matching executable; interpret stacks, missing symbols and inconclusive evidence. |

The GDB procedure is source-reviewed. Linux execution and agent evaluation are **not-run**; its skill and provenance contain the full record. A source-reviewed skill may be useful to evaluate, but it is not a claim of tested compatibility or improved agent performance. See the [validation record](docs/validation.md).

This catalogue is an overview for maintainers and installers. Installed skills do not read or depend on it. It lists accepted coverage only; no placeholder skills have been created for planned tools.

## Repository layout

~~~text
research-library/
├── README.md                         # available skills and project overview
├── GETTING_STARTED.md                # Linux setup and authoring workflow
├── AGENTS.md                         # instructions for repository maintenance
├── CLAUDE.md                         # imports AGENTS.md
├── authoring/
│   ├── schema.md
│   ├── create-skill.prompt.md
│   ├── review-skill.prompt.md
│   ├── skill.template.md             # full skill (A), including frontmatter
│   ├── delta-skill.template.md       # compact skill (B), including frontmatter
│   ├── provenance.template.md
│   ├── intake.template.md
│   ├── adapt-to-host.prompt.md
│   ├── local-machine.template.md
│   ├── sources.md
│   └── capture-help.md
├── docs/                             # harness setup and validation record
├── evaluation/                       # cases and evaluation method
├── profile/                          # optional user-side shell settings
├── scripts/                          # authoring capture and repository checks
├── tests/
├── methodologies/
│   └── arcanum-llm-assessment.md
└── skills/
    └── gdb/                          # copy this folder alone to install GDB
        ├── SKILL.md
        └── references/
            └── provenance.md
~~~

A future strace skill would have its own `skills/strace/SKILL.md` and local resources. A simple skill needs no additional routing document. Larger tool skills may keep substantial mode-specific guidance in their own `references/`; they still ship as one independent folder.

## Create another skill

1. Choose a useful task and the guidance gap. Select A (full procedure), B (compact correction) or C (defer) using the [schema and rationale](authoring/schema.md).
2. For A/B, fill the [source intake](authoring/intake.template.md). Gather practical examples and focused semantics evidence using the [source strategy](authoring/sources.md) and, when useful, [help capture](authoring/capture-help.md).
3. Give the authoring agent the [generation prompt](authoring/create-skill.prompt.md), [A template](authoring/skill.template.md) or [B template](authoring/delta-skill.template.md), [provenance template](authoring/provenance.template.md), schema and packet. It creates an independent skill package. C records a deferral reason and creates no installed skill.
4. Use the [review prompt](authoring/review-skill.prompt.md), then the [evaluation process](evaluation/README.md). Record source review, procedure execution and agent evaluation separately.
5. Place accepted content in `skills/<name>/`, add its README catalogue row, and install only that folder using the [deployment guide](docs/harnesses.md). Drafts stay in ignored `work/`.

A and B differ in the amount of useful guidance; both are independently discoverable and portable. Do not produce a full tutorial when one correction is enough. Do not produce an empty skill just to reach a tool-count target.

The getting-started guide includes a complete strace authoring request, exact source-packet paths, host-adaptation steps and Git commands.

## The four knowledge gaps

| Gap | What useful guidance supplies |
|---|---|
| Selection | The question this tool can answer, conditions where it applies, and an alternative when it cannot answer that question. |
| Reliable execution | Relevant prerequisites, supported commands, defined inputs, effects, output handling and session requirements. |
| Interpretation | What an observation supports, what it cannot establish, and common misleading results. |
| Follow-up and verification | A next action tied to the observation, a way to test the explanation, and evidence for finishing or identifying a specific blocker. |

Start with real tasks: search/filtering failures (`rg`, `find`, `jq`), HTTP/connectivity failures (`curl`, `ss`), service failures (`systemctl`, `journalctl`), stuck processes (`ps`, `lsof`, `strace`), native crashes (`gdb`) or CPU usage (`perf`). These are candidates, not claims of implemented coverage. Use observed agent failures to prioritise which tools deserve skills.

## Authoring companions and checks

`AGENTS.md` and `CLAUDE.md` apply to maintaining this repository. They are not global instructions for machines installing a skill. The optional [display profile](profile/display-env.sh) and [shell instruction snippet](profile/agent-shell.md) can be applied separately; installing a skill does not apply or require them.

The [capture helper](scripts/capture_help.py) records known help/version invocations. Help output is evidence about documentation and invocation, not a successful diagnostic workflow. Keep raw captures and machine facts in ignored `work/` and run artifacts in ignored `runs/`; retain durable citations and non-sensitive findings in each skill's provenance.

From the repository root:

~~~bash
python3 scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
~~~

The [checker](scripts/check_repository.py) validates local links, per-skill boundaries, source IDs and simple frontmatter. Tests include copying each skill alone to an isolated directory and checking it there. These are structural/helper checks; Linux fixtures and actual agent behaviour need separate evaluation.

`.gitattributes` keeps text suitable for Linux checkouts. Add a repository license when you choose distribution terms; no license choice is assumed here.

## Current limits

- GDB covers existing cores only. Live attachment, stepping, core collection and other debugger modes need their own supported procedures before being advertised.
- Tool versions, GNU/BusyBox differences and kernel/session capabilities need checks on the actual host. A skill cannot provide missing executables or permissions.
- Independent skills let workers install a relevant subset. Keep descriptions concise and evaluate ordinary task discovery as well as explicit invocation; publishing many skills does not require loading all of them into every worker.
- Source review, command execution and useful agent performance are different results. Measure outcomes, recovery and unnecessary commands against a baseline; shorten or defer guidance that adds no value.
- Freshness and source maintenance are manual initially. Use source locators, recorded versions, review dates and Git history; add automation when actual maintenance work justifies it.
