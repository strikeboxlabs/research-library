# Linux deployment across harnesses

Documentation checked on 2026-10-09. These are documented discovery paths; the three harnesses were not launched on Linux during this preparation.

## Install selected independent skill folders

Each `skills/<name>/` folder is an independent runtime package. Install the complete folder, including any local resources, for each tool a worker needs. The current example is `skills/gdb/`; it needs no other skill or repository files. For the Linux edit/commit workflow, follow [GETTING_STARTED.md](../GETTING_STARTED.md): link selected folders from the checkout so edits and pulls update one source. Ordinary complete copies also work when deployment should be independent of the checkout.

| Harness | Project destination | User destination | Explicit invocation |
|---|---|---|---|
| Codex | `.agents/skills/gdb/` | `~/.agents/skills/gdb/` | `$gdb` |
| Pi, current documented layout | `.agents/skills/gdb/` | `~/.agents/skills/gdb/` | `/skill:gdb` |
| Claude Code | `.claude/skills/gdb/` | `~/.claude/skills/gdb/` | `/gdb` |

Codex documents repository and user discovery under `.agents/skills`. See [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills). Pi also documents these shared locations and explicit skill invocation. See [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md). Claude Code documents its own project and user skill directories. See [Claude Code skills](https://code.claude.com/docs/en/skills).

If Pi and Codex run as the same Linux user, one user-level installation of GDB in `~/.agents/skills/gdb/` serves both. Claude uses its own discovery location pointing to or copied from the same source. A project-level installation instead confines discovery to the applicable project. Repeat per selected tool; do not install the repository root or an umbrella folder as a skill.

Pi also has native skill locations, normally `~/.pi/agent/skills/` and `.pi/skills/`. Older installed releases or customised agent directories may need those locations or an explicit resource path. Choose one route per harness so the same skill is not registered twice. See [Pi configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md).

For each installation, inspect an existing destination and avoid overwriting local changes. Keep the source revision in the deployment record. For symlinks, confirm the target checkout and reload/start a fresh agent session after updates. For copies, review and replace the complete owned copy; blindly overlaying directories can leave removed references behind. The getting-started guide also covers replacing the earlier `linux-cli` installation with `gdb`.

## Skill loading and the first read

Our authoring rule is to put the activation contract and any task map near the top. A worker must read the whole `SKILL.md` before acting, then read the references required by the selected workflow. Required steps/helpers and conditional branches should be distinguishable from the opening. Completion means the requested result is evidenced, with missing prerequisites or unperformed steps reported honestly. This improves navigation and makes omissions easier to detect; Markdown checklists do not enforce execution.

This rule adopts the practical pattern in the Jason Haddix post and screenshot supplied by the user on 2026-10-10: an early mandatory contract, an explicit list of required work, and separate references loaded only when their conditions arise. The original X post was not independently retrieved. Its reported 150-line reading pattern is treated as an operational observation worth designing for, rather than a verified hard limit across products.

Official documentation and upstream code reviewed on 2026-10-10 distinguish three things: discovery metadata, loading the body, and the model actually following it:

| Harness | What the reviewed source establishes |
|---|---|
| Codex | Names/descriptions appear first; full SKILL.md instructions load when the skill is selected. The listing itself has a context budget and can shorten descriptions or omit entries. [Official skills documentation](https://learn.chatgpt.com/docs/build-skills). |
| Claude Code | Normal discovery exposes descriptions; invocation loads the skill. Supporting files are loaded as needed. Its guidance recommends keeping SKILL.md below 500 lines; it does not establish the claimed 150-line invocation cutoff. [Official skills documentation](https://code.claude.com/docs/en/skills). |
| Pi | Discovery exposes metadata. Current upstream `/skill:name` expansion reads the entire file and inserts the body. Ordinary `read` calls accept a chosen line limit; default truncation is 2,000 lines or 50 KiB, whichever comes first. [Skills documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md), [explicit expansion](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/agent-session.ts), [reader](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/tools/read.ts), [default limits](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/tools/truncate.ts). |

These are documentation/source findings, not an evaluation of the installed Linux workers. The local Codex installation exposed executables, not loader source; Pi and Claude Code were not on the inspected PATH. Upstream `main` can change. Model-selected partial reads, wrappers, context budgets and missed instructions can still make an early contract useful even when the full body is available.

The [schema](../authoring/schema.md) makes the **first 150 lines a review boundary**: every workflow and required resource must be discoverable from the opening, preferably long before that boundary. It is neither a required length nor a reason to read every reference. Avoid generic obligations such as running a version check for every trivial invocation unless the task needs it. A required helper should have its exact skill-relative path and purpose stated early; if unavailable, report the specific gap rather than silently replacing the workflow.

The completion pattern scales with the task. A multi-stage assessment can need a persisted checklist and artifacts. A CLI inspection may need only a command result and a supported conclusion. Mark not-applicable branches with a reason and missing required evidence as blocked or incomplete; never invent artifacts or execute unrelated steps merely to clear boxes.

Verify reading behavior with both explicit invocation and automatic selection on the actual worker: observe what was loaded, required helper use, the handling of a missing reference, and whether conditional references stay unopened when irrelevant. The [evaluation guide](../evaluation/README.md) describes the comparison. Do not claim reliability gains from a line count or passing Markdown checks.

## Repository companion files

`AGENTS.md` contains instructions for agents editing this repository. It is not a global operating policy for systems that install the skill.

`CLAUDE.md` contains:

~~~markdown
@AGENTS.md
~~~

This keeps one maintained instruction file and supports Claude configurations that use the import. Current Claude documentation also describes direct AGENTS.md support; the import remains a compatible option. See [Claude Code memory documentation](https://code.claude.com/docs/en/memory).

Do not copy either file into the user's global instruction directory as part of installing the runtime skill.

## Portable runtime assumptions

Each skill uses file reads and Linux command execution without naming a harness's internal tool API. It needs access to its own installed directory and the intended target. Runtime links stay within that directory; shared authoring templates remain repository-only.

Keep necessary output, timing and session requirements in the skill that uses them. The [GDB skill](../skills/gdb/SKILL.md) reads an existing core dump in batch mode and includes its own artifact, output and follow-up instructions. Optional general shell advice stays outside installed skills in `profile/`.

No plugin manifest, MCP configuration, model setting, tool allowlist, or global instruction change is required for this packaging. Existing harness permissions and launch flags still control what is available.

## Optional user-side shell profile

The files in `profile/` are separate from all installed skills. They address defaults that can matter before skill discovery. Apply them only if wanted; skills do not require them and never edit harness configuration or shell startup files automatically.

The [display profile](../profile/display-env.sh) sets pager/colour defaults only. To try it for one Pi launch from this repository on Linux:

~~~bash
(
  . ./profile/display-env.sh
  pi
)
~~~

The subshell confines the exports to that launch and its children. The same launch pattern can be used for another CLI harness where environment inheritance is appropriate. Application configuration can override shell defaults; check the variables inside the agent's actual command execution environment.

For Claude Code, merge these entries into the existing `env` object in the settings file at your chosen scope. This is a fragment, not a replacement for the whole file:

~~~json
{
  "env": {
    "PAGER": "cat",
    "MANPAGER": "cat",
    "GIT_PAGER": "cat",
    "SYSTEMD_PAGER": "",
    "LESS": "-FRX",
    "NO_COLOR": "1"
  }
}
~~~

Claude documents environment configuration under the `env` settings key; scope and managed settings can affect what applies. See [Claude Code environment variables](https://code.claude.com/docs/en/env-vars) and [settings precedence](https://code.claude.com/docs/en/settings).

For Codex, merge the same entries into its existing configuration table, preserving unrelated settings:

~~~toml
[shell_environment_policy.set]
PAGER = "cat"
MANPAGER = "cat"
GIT_PAGER = "cat"
SYSTEMD_PAGER = ""
LESS = "-FRX"
NO_COLOR = "1"
~~~

Current [official OpenAI configuration documentation](https://learn.chatgpt.com/docs/config-file/config-reference) defines `shell_environment_policy.set` as explicit environment values; include filters can still remove them. Check the documentation for the installed release and confirm the values in a shell call. These snippets were documentation-checked, not launched in the three Linux harnesses here.

The [short instruction snippet](../profile/agent-shell.md) can be merged into the instruction file your harness already loads before skill discovery. It covers bounded execution, retained output, session state and unattended prompts. Do not install this repository's maintenance `AGENTS.md` as a user operating policy.

Authentication and package-operation settings are separate choices. `GIT_TERMINAL_PROMPT=0` can suppress terminal credential prompts; `PIP_NO_INPUT=1` and `DEBIAN_FRONTEND=noninteractive` change interaction for their respective tools. Use them only for the intended unattended operation, with required input supplied and outcome checked. They are not exported by the display profile. Consult the applicable [Git environment documentation](https://git-scm.com/docs/git#Documentation/git.txt-codeGITTERMINALPROMPTcode), [pip general options](https://pip.pypa.io/en/stable/cli/pip/#general-options) and [debconf frontends](https://manpages.debian.org/bookworm/debconf-doc/debconf.7.en.html).

No editor is replaced with `true`: that returns success without editing and can let a command continue with unchanged content. Use explicit command-specific options for the desired operation. See [GNU true](https://man7.org/linux/man-pages/man1/true.1.html).

## Verify each actual installation

1. Confirm the installed harness/version and selected discovery path.
2. Start or reload a session and explicitly invoke the selected skill. Ask it to identify its loaded path, supported scope and execution status.
3. Use an ordinary symptom-based request to check automatic discovery separately.
4. Run a permitted fixture with only that skill installed and confirm guidance/resource loading, command output/exit-status capture, and cleanup. File visibility alone is not a successful execution test.
5. Record the harness version, model, source revision, target environment and result. If discovery fails, inspect that release's documentation and launcher settings before adding configuration.

Optional later: package distribution, an installer with conflict handling, and harness-specific UI metadata. Keep the independently installable skill folders intact when adding distribution conveniences.
