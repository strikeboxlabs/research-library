# Validation record

Date: 2026-10-09. Current packaging/schema: v0.3. Earlier starter and migration checks are retained below. This is not a completed tool catalogue or a measured agent-performance result.

## Independent tool skills, v0.3

GDB is now an independently installable folder with its procedure directly in `skills/gdb/SKILL.md` and its source companion in `skills/gdb/references/provenance.md`. The old umbrella, runtime index and shared runtime guide have been removed. The authoring schema, A/B templates, generation/review prompts and Linux setup guide now create and install individual tool skills. Tier C records a deferral without creating a runtime package.

Executed on Windows:

- Sixteen tests passed: six capture-helper tests and ten repository checks. The new checks cover copying the actual GDB folder into an isolated directory without the repository, rejecting sibling-skill dependencies, requiring each skill folder's own entrypoint, checking local provenance source IDs, and checking template links after materialisation.
- The repository checker resolved all local links, checked each skill boundary and parsed 19 Bash blocks with Git Bash. Template destinations are deferred until instantiated in a skill folder. Shell examples were parsed only, not executed.
- The skill-creator validator accepted `skills/gdb/`. Its name matches its folder and its description remains scoped to existing native core dumps.
- Compared with the pre-refactor Git version, the GDB procedure, executable commands, decision branches and failure recovery are unchanged. Source review remains recorded separately from unrun execution and agent evaluation.
- `git diff --check` passed, and the existing methodology has no changes.

These checks establish local packaging and helper behaviour. They do not establish Linux GDB compatibility, discovery in a live harness or improved worker performance. No installed agent configuration, commit or push was performed by this refactor.

## Earlier starter checks, v0.2

- Six capture-helper tests passed using Python 3.12 on Windows. They exercised real child processes for version/help output, separate stdout/stderr and nonzero status, partial output on timeout, a missing executable, rejection of invalid timeouts, and refusal to overwrite an existing capture.
- The skill-creator validator accepted the skill's frontmatter and structure. Runtime references contain no unfinished template placeholders.
- Local Markdown links resolved; runtime links stayed inside the installed skill directory. Template destinations containing placeholders were identified separately.
- GDB provenance source IDs S1-S7 resolved within the companion's claim map. The executable GDB batch command is identical to the earlier starter's command.
- The JSON and TOML profile snippets parsed and matched the shell profile's six display settings.
- Seven documented Bash blocks parsed successfully. The display profile was sourced in a Git Bash child shell on Windows: display defaults were set, while seeded editor, authentication and package-operation settings were preserved.

The Windows sandbox's default temporary directory initially prevented the subprocess tests from creating their capture files. Running them with a writable workspace temporary directory passed. Git Bash required execution outside the sandbox to initialise; the check changed only its child-shell environment.

## Still untested

- GDB procedures and proposed diagnostic cases on Linux.
- Help collection in the prepared distro containers.
- The capture helper's POSIX process-group timeout path.
- Actual loading, automatic discovery and task completion in Pi, Claude Code or Codex on Linux.
- Any claim of improved agent performance or broad tool-version compatibility.

The GDB skill therefore retains checked source review, `Execution: not-run` and `Agent evaluation: not-run`. Harness configuration examples were checked against the official documentation linked in the [deployment guide](harnesses.md); successful snippet parsing is not proof of runtime application.

Run the [evaluation process](../evaluation/README.md) on the intended Linux system before claiming those outcomes.

## Repository-root migration and Linux guide

On 2026-10-09, the 27-file starter was placed directly at the existing `research-library` Git root. All 81 original starter, archive and preparation files were copied and hash-checked before edits. The previous ZIP and scratch material remain in ignored `work/`; runtime and authoring files are at the root's documented locations. The pre-existing assessment methodology's contents were preserved.

The [getting-started guide](../GETTING_STARTED.md) now contains checkout/install commands, host adaptation, source ingestion, reusable agent requests and Git publication steps. A saved host-adaptation prompt and local-machine template support that workflow.

Eleven subprocess/repository-check tests passed on Windows. The [portable checker](../scripts/check_repository.py) found no broken local links or runtime references outside the skill, and the skill-creator validator accepted the skill. The Linux shell examples were syntax-checked using Git Bash; no clone, installation link, Linux fixture or Git publication command from the guide was executed here. Linux runtime and harness validation remain pending as listed above.
