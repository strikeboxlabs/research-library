# Start on a Linux machine

Use a normal Git checkout for editing and install individual skill folders for workers. Choose tools and supported tasks from the [catalogue](README.md#tool-skills); each skill has a deliberately bounded scope.

1. [Check out and install](#1-check-out-and-install)
2. [Adapt to this machine](#2-adapt-to-this-machine)
3. [Create a skill from documentation](#3-create-a-skill-from-documentation)
4. [Check and commit](#4-check-and-commit)

## 1. Check out and install

Recommended location: `~/src/research-library`, owned by the Linux account running the agent. Publish your Windows changes to GitHub first so the clone contains them.

~~~bash
mkdir -p "$HOME/src"
git clone https://github.com/strikeboxlabs/research-library.git "$HOME/src/research-library"
cd "$HOME/src/research-library"
~~~

For an existing clone, preserve local work and use `git pull --ff-only`. Git and the chosen agent must already be installed. Authoring helpers require Python 3.10+; using a skill requires its actual executable. Installation does not install Linux tools.

Link the selected skill from the repository root. The later Linux pass updates these same packages for the controlled distribution; no separate per-host copy is required. Change `skill=gdb` when installing another tool. Existing destinations are left untouched:

~~~bash
(
  set -eu
  repo=$(pwd -P)
  skill=gdb
  test -f "$repo/skills/$skill/SKILL.md"
  for parent in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
    mkdir -p "$parent"
    destination="$parent/$skill"
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      printf 'Already exists; inspect before using: %s\n' "$destination"
    else
      ln -s "$repo/skills/$skill" "$destination"
      printf 'Linked: %s\n' "$destination"
    fi
  done
)
~~~

| Harness | User-level destination | Explicit invocation |
|---|---|---|
| Codex | `~/.agents/skills/gdb/` | `$gdb` |
| Pi, current documented layout | `~/.agents/skills/gdb/` | `/skill:gdb` |
| Claude Code | `~/.claude/skills/gdb/` | `/gdb` |

See [harnesses.md](docs/harnesses.md) for official sources, older Pi layouts and project-level alternatives. Keep one installation of each skill per harness. Inspect skipped destinations; they may point elsewhere. Complete copies also work: copy the selected folder and all resources it contains, then refresh it after updates.

If an older `linux-cli` installation exists, preserve any custom edits and remove that owned symlink or move its copied folder outside the harness's skill directories. Install `gdb` at the new path. Updating the checkout does not change old installation links.

Start a fresh session and explicitly invoke the skill. Ask it to identify the loaded path and supported task, then try an ordinary symptom-based request. If the agent connects to Linux over SSH, its own environment still needs access to the skill files.

Use this repository for authoring. Run ordinary workers in their actual task workspace and expose only the selected skills; do not install the repository's maintenance `AGENTS.md` globally. The shell settings in `profile/` are optional.

## 2. Adapt to this machine

This is a **later pass on the specific Linux distribution/image we deploy and control**. The task graph does not currently provide a reliable tool/path inventory. During source ingestion, improve the guidance and leave unknown target paths unclaimed; do not delay ingestion or create placeholder environment references.

On the Linux box, an authoring agent will locate the actual binaries and inspect the relevant versions/options from the worker's own environment. Enrich the corresponding task references directly. When several workflows share executable context, use a concise `references/environment.md` inside that skill and link it from the opening. It should contain the verified absolute invocation, relevant implementation/version and real option or permission constraints, without an exhaustive machine inventory.

Because we control the image, stable non-sensitive paths and image facts can be committed with the skill and distributed normally. Node-specific exceptions, secrets and raw observations stay in ignored `work/` or `runs/`. The skill remains independently installable as one complete folder. Reuse known context and revisit it when the image changes or behavior contradicts it, rather than repeating discovery on each invocation.

From an authoring agent in the checkout, inspect the environment its commands actually use. A login shell may have a different PATH or permissions.

~~~bash
cat /etc/os-release
uname -srm
command -v gdb
type -a gdb
gdb --version
~~~

Keep useful local facts in ignored `work/machine.md`; the [machine template](authoring/local-machine.template.md) is optional. Capture installed help/version output when useful:

~~~bash
capture_id=$(date -u '+%Y%m%dT%H%M%SZ')
python3 scripts/capture_help.py gdb --output "work/sources/gdb/$capture_id"
~~~

Pass an actual absolute binary path instead of `gdb` when deliberately selecting an executable outside PATH. Inspect the capture's status and streams. See [capture-help.md](authoring/capture-help.md) for alternate switches and container capture. Debugger commands may need built-in help or matching manual sections beyond CLI `--help`.

| Finding | Adaptation |
|---|---|
| Different binary path/name or multiple implementations | Record the verified shared-image invocation in the skill reference; use its absolute path. Keep node-specific exceptions in local notes. |
| Different options or behaviour | Verify meanings in installed help/applicable manuals. Add only relevant version/feature conditions; do not guess version cutoffs. |
| Missing symbols, permissions, architecture support or session control | State the missing prerequisite and narrow the conclusion. |
| A procedure works here | Record the case, versions and outcome; this does not establish other environments or agent performance. |

Paste this job, or use the saved [host-adaptation prompt](authoring/adapt-to-host.prompt.md):

~~~text
Adapt skills/gdb/SKILL.md to this Linux machine using
AGENTS.md and authoring/adapt-to-host.prompt.md.

Inspect the real binary/version/options and save detailed facts in work/machine.md.
Enrich existing skill references, or references/environment.md when useful,
with verified absolute invocations and relevant facts of our controlled image.
Keep node-specific/private observations ignored; shared image facts may be committed.
You may create, compile and run disposable programs you own under runs/ and
inspect their cores with GDB. Do not attach to unrelated processes or change
system-wide core-dump, security or service settings.

Test useful normal and incomplete-evidence cases where feasible. Keep useful
corrections concise and report what actually ran. Leave changes for Git review;
do not commit, push or alter global configuration.
~~~

A C compiler and usable core-generation setup are needed for those fixtures. If unavailable, record that limitation. Proposed GDB cases are in [evaluation/README.md](evaluation/README.md).

## 3. Create a skill from documentation

Example: create a `strace` skill. Start a source folder:

~~~bash
mkdir -p work/sources/strace
~~~

Put practical walkthroughs, documentation, notes, command transcripts or agent failures there. A `links.txt` with one URL per line works when the agent can fetch them. Supply readable extracts for formats the agent cannot open. The [source guide](authoring/sources.md) lists useful starting points.

For a batch of documents covering several tools, `ingest/` is a local, Git-ignored inbox. Process the requested files sequentially and fully; extract the operational lesson before choosing which tool to improve. Separate source observations from explanations and compare against current coverage. When revisiting an existing skill, bring its whole affected task into the current schema: correct, merge, trim and move substantial alternative tasks to references when useful. Do not merely append an example, add mandatory fields or rewrite unrelated skills. Record the schema version and skills actually reviewed (including conforming/no-change outcomes) in the batch report; at batch end identify any library skills not yet reviewed. A fully reviewed document with no useful runtime delta is completed intake.

Account for tools actually used in the source, including tools whose purpose overlaps an existing skill. Link each demonstrated task to existing coverage, an addition or a specific evidence gap in the intake report. Use accumulated sources and upstream documentation to fill gaps; do not demand complete tool coverage or a Linux test before accepting documentation-reviewed guidance. Preserve deeper operational procedures in conditional references. Restrictions on what the authoring agent may execute do not remove those procedures from the documentation scope. See the [coverage rules](authoring/schema.md#coverage-decisions-during-ingestion).

Verify consequential semantics against applicable upstream sources. Apply the [first-read authoring rule](authoring/schema.md#make-the-first-read-sufficient-to-choose-and-load-the-task) to every skill created or enriched: whole-entrypoint reading, early required steps/helpers, conditional references and evidence-based completion. Review the first 150 lines for discoverability, then the complete selected workflow for hidden requirements. Originals stay local; extracted notes belong in `work/`. Record source-to-skill mappings and coverage decisions in the existing batch reports under `docs/`. The [first PDF batch](docs/ctf-writeups-ingestion.md) shows an intake record.

Tell the agent the task, target environment if known, whether it may research further, and what it may execute. You can use the optional [intake template](authoring/intake.template.md) or put those facts directly in your request. No full man page or formal source packet is required.

Launch an authoring agent in the repository root and paste:

~~~text
Create an independent strace skill using the material in work/sources/strace/.
The useful task is investigating file-access failures in a native program.

Read AGENTS.md, authoring/schema.md and authoring/create-skill.prompt.md.
You may retrieve upstream documentation and inspect the installed strace.
If installed, test only disposable programs owned by this task under runs/;
do not attach to unrelated processes or install packages.

Create or update skills/strace/SKILL.md with concise selection and starting guidance.
Reconcile existing content with the current schema instead of only appending.
Use conditional references for substantial deeper tasks and operational knowledge. Connect commands
to meaningful output, interpretation and the next decision where an example
helps. Label invented output as illustrative. Keep operational limits in the
skill; save fuller source trails and test history in docs/ maintenance records.
Put the activation contract near the top: read the whole SKILL.md before acting,
identify required steps/helpers and completion evidence for the selected task.
Link conditional references with their triggers; read them before their procedure.
Review the first 150 lines for discoverability, then the whole selected workflow.
Add skill-local references only for substantial conditional working detail.
Review commands and interpretations, remove repetition, check independent
packaging and update the README catalogue. Keep incomplete drafts in work/.

Report what was reviewed, what actually ran and remaining gaps.
Leave changes for Git review; do not commit, push or change global settings.
~~~

For supplied-only research, replace the permission to retrieve documentation with that constraint. Missing binaries need not prevent a documentation-based draft; mark untested behaviour accurately. Optional help capture:

~~~bash
capture_id=$(date -u '+%Y%m%dT%H%M%SZ')
python3 scripts/capture_help.py strace --output "work/sources/strace/$capture_id"
~~~

The result starts with `skills/strace/SKILL.md`. A conditional working reference or useful helper script is optional; every required resource stays inside that skill. Keep useful documentation fallback links and compatibility conditions near the relevant procedure. Put review dates, source-document/page trails and actual test history in intake/validation records under `docs/`, mapped to the skill. Workers do not need those records. Keep raw/private inputs in `work/` and raw test output in `runs/`.

Use the [review prompt](authoring/review-skill.prompt.md) for another review when useful. Test a small correction with a focused check; test a diagnostic workflow's conclusions and relevant incomplete-evidence branch. The [evaluation guide](evaluation/README.md) covers comparisons with an unassisted worker.

## 4. Check and commit

~~~bash
python3 scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
git diff --check
git status --short
git diff
~~~

These checks validate helper behaviour and packaging, including copying skills alone. They do not run the Linux procedures. New files are absent from plain `git diff`; inspect them before staging and review `git diff --cached` afterwards.

To publish the current project changes from Windows after review (these Git commands work in PowerShell too):

~~~bash
git add .gitattributes .gitignore AGENTS.md CLAUDE.md GETTING_STARTED.md README.md authoring docs evaluation profile scripts skills tests
git diff --cached
git commit -m "Simplify independent Linux tool skills"
git push origin main
~~~

For a later strace addition, stage only its intended files:

~~~bash
git add skills/strace README.md
git diff --cached
git commit -m "Add strace guidance"
git push
~~~

Include deliberately changed evaluation/docs files as needed. Keep machine notes and raw captures out of commits. On other checkouts, preserve local work before pulling. Skill symlinks follow checkout updates; newly added skills need their own links. Start a fresh session after changes; Pi also documents `/reload`. Refresh complete copies deliberately.
