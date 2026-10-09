# Linux deployment across harnesses

Documentation checked on 2026-10-09. These are documented discovery paths; the three harnesses were not launched on Linux during this preparation.

## One portable runtime folder

Install the complete `skills/linux-cli/` folder, including `references/`. Maintain it in one source repository. For the Linux edit/commit workflow, follow [GETTING_STARTED.md](../GETTING_STARTED.md): link the complete skill folder from the checkout so edits and pulls update one source. Ordinary complete copies also work when deployment should be independent of the checkout. Internal runtime references stay inside the skill in either case.

| Harness | Project destination | User destination | Explicit invocation |
|---|---|---|---|
| Codex | `.agents/skills/linux-cli/` | `~/.agents/skills/linux-cli/` | `$linux-cli` |
| Pi, current documented layout | `.agents/skills/linux-cli/` | `~/.agents/skills/linux-cli/` | `/skill:linux-cli` |
| Claude Code | `.claude/skills/linux-cli/` | `~/.claude/skills/linux-cli/` | `/linux-cli` |

Codex documents repository and user discovery under `.agents/skills`. See [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills). Pi also documents these shared locations and explicit skill invocation. See [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md). Claude Code documents its own project and user skill directories. See [Claude Code skills](https://code.claude.com/docs/en/skills).

If Pi and Codex run as the same Linux user, one user-level installation in `~/.agents/skills/linux-cli/` serves both. Claude uses its own discovery location pointing to or copied from the same source. A project-level installation instead confines discovery to the applicable project.

Pi also has native skill locations, normally `~/.pi/agent/skills/` and `.pi/skills/`. Older installed releases or customised agent directories may need those locations or an explicit resource path. Choose one route per harness so the same skill is not registered twice. See [Pi configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md).

For each installation, inspect an existing destination and avoid overwriting local changes. Keep the source revision in the deployment record. For symlinks, confirm the target checkout and reload/start a fresh agent session after updates. For copies, review and replace the complete owned copy; blindly overlaying directories can leave removed references behind.

## Repository companion files

`AGENTS.md` contains instructions for agents editing this repository. It is not a global operating policy for systems that install the skill.

`CLAUDE.md` contains:

~~~markdown
@AGENTS.md
~~~

This keeps one maintained instruction file and supports Claude configurations that use the import. Current Claude documentation also describes direct AGENTS.md support; the import remains a compatible option. See [Claude Code memory documentation](https://code.claude.com/docs/en/memory).

Do not copy either file into the user's global instruction directory as part of installing the runtime skill.

## Portable runtime assumptions

The skill uses file reads and Linux command execution without naming a harness's internal tool API. It needs access to the complete installed skill directory and the intended target.

The [shared runtime guide](../skills/linux-cli/references/runtime.md) covers output, time limits, and session requirements. The supplied GDB workflow reads an existing core dump in batch mode; it does not depend on a persistent terminal.

No plugin manifest, MCP configuration, model setting, tool allowlist, or global instruction change is required for this packaging. Existing harness permissions and launch flags still control what is available.

## Optional user-side shell profile

The files in `profile/` are separate from the installed skill. They address defaults that can matter before skill discovery. Apply them only if wanted; the starter never edits harness configuration or shell startup files automatically.

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
2. Start or reload a session and explicitly invoke the skill. Ask it to identify its loaded path, available tool coverage, and the GDB reference's execution status.
3. Use an ordinary symptom-based request to check automatic discovery separately.
4. Run a permitted fixture and confirm reference retrieval, command output/exit-status capture, and cleanup. File visibility alone is not a successful execution test.
5. Record the harness version, model, source revision, target environment and result. If discovery fails, inspect that release's documentation and launcher settings before adding configuration.

Optional later: package distribution, an installer with conflict handling, and harness-specific UI metadata. None changes the underlying tool reference schema.
