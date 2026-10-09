# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md)** for the Linux checkout, installation, host adaptation and creating skills from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Tool skills

Skills add useful tool knowledge for agents that already use the CLI competently. Each tool has its own `skills/<name>/SKILL.md`. Copy or link only the folders a worker needs; every skill works independently of the rest of this repository.

| Skill | Current scope |
|---|---|
| [gdb](skills/gdb/SKILL.md) | Examine existing native core dumps with matching executables; interpret stacks, missing symbols and incomplete evidence. |

GDB is documentation-reviewed but has not been executed or evaluated with an agent on Linux. See the [validation record](docs/validation.md).

## Simple structure

~~~text
skills/<tool>/
    SKILL.md                   # metadata and working instructions
    references/                # optional, only when useful
        sources.md             # optional source/maintenance notes

authoring/                     # schema, prompts and optional templates
docs/                          # harness setup and validation history
evaluation/                    # optional test design and case template
scripts/                       # help capture and repository checker
tests/
profile/                       # optional shell settings
~~~

One `SKILL.md` is enough for a small skill. Use ordinary Markdown with the standard [Agent Skills frontmatter](https://agentskills.io/specification). Add references for substantial conditional detail, sources for useful maintenance evidence, or scripts for repeated executable logic. Required resources stay inside their own skill folder.

## Create or improve a skill

1. Choose a task or known mistake. Collect practical documentation, examples or transcripts using the [source guide](authoring/sources.md).
2. Use the [authoring prompt](authoring/create-skill.prompt.md) and [schema](authoring/schema.md). The [single template](authoring/skill.template.md) is optional. A short correction may be enough; skip tools with no useful guidance gap.
3. Review accuracy and remove repetition. The [review prompt](authoring/review-skill.prompt.md) and [evaluation guide](evaluation/README.md) support deeper checks when needed.
4. Add accepted skills to the catalogue above. Keep drafts/raw sources in ignored `work/` and test artifacts in `runs/`; retain useful portable findings in the skill or source notes.

Commands, interpretations and recovery advice need evidence. Documentation review, procedure execution and improved agent performance are different claims. Record only what was actually established.

## Repository checks

~~~bash
python3 scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
~~~

These validate links, basic frontmatter, standalone packaging and helper behaviour. Linux tool execution and worker usefulness need separate checks. Compare successful outcomes, recovery and total task cost against a baseline.

`AGENTS.md` and `CLAUDE.md` are for authors maintaining this repository. Workers need selected skill folders only. Optional settings in `profile/` are separate from skill installation. Add a repository license when you choose distribution terms.
