# Finding practical material

The useful unit of collection is a task or investigation. Begin with a question such as "why does this process wait indefinitely?" and look for material showing how someone narrowed it down. The tool reference should preserve the decisions and evidence that made that investigation work.

## Sources for the four gaps

| Gap | Best starting material | What to extract | How to check it |
|---|---|---|---|
| Selection | Diagnostic methodologies, tool-selection guides, original incident write-ups. | The symptom, alternative hypotheses, why this tool was selected, and when another tool was more informative. | Check that the procedure can actually observe the condition; distinguish a heuristic from a guaranteed rule. |
| Reliable execution | Maintainer tutorials, working example repositories, recorded sessions, focused help/manual sections. | Required inputs and setup, supported options, environment/version assumptions, bounded execution, output location and relevant effects. | Verify option semantics with official documentation or installed help; run a small fixture when available. |
| Interpretation | Walkthroughs that explain real output, maintainer diagnostic replies, worked examples with a known cause. | Which output mattered, its units/scope, what changed the hypothesis, and what the output could not establish. | Preserve the circumstances of the observation. Use a healthy/control case to test an interpretation. |
| Follow-up and verification | Complete investigations, bug reproductions plus fixes, regression tests, your own successful or failed agent transcripts. | The discriminating next check, failed approaches, recovery, and evidence that the explanation or correction was valid. | Reproduce the outcome or expected limitation. A plausible final explanation is insufficient. |

## Concrete starting points

These are source leads, not automatically accepted procedures. Check the exact section and target version during authoring.

| Area | Source | Why it is useful |
|---|---|---|
| Selecting performance tools | [Brendan Gregg: USE Method](https://www.brendangregg.com/usemethod.html) and [Linux Performance](https://www.brendangregg.com/linuxperf.html) | The author's diagnostic method and Linux tool maps help turn symptoms into measurement choices. |
| GDB | [GNU GDB sample session](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Sample-Session.html), followed by the relevant manual sections | A worked debugging sequence supplies task context; focused command documentation verifies the mechanics. |
| ripgrep | [Maintainer's user guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md) | Practical searches and filtering behaviour provide useful material for both usage and "why was this missed?" recovery. |
| jq | [Project tutorial](https://jqlang.org/tutorial/) | A concrete JSON transformation task with intermediate output. Extend it with task-specific missing/null/error cases. |
| curl | [Everything curl: verbose output](https://everything.curl.dev/usingcurl/verbose/) | The project book explains what connection and protocol messages mean. Pair it with the task-specific chapters and current option documentation. |
| bpftrace | [Project one-liner tutorial](https://bpftrace.org/tutorial-one-liners) | Explains tracing examples and output. Check current probe availability and environment requirements separately. |
| GNU find | [Findutils worked examples](https://www.gnu.org/software/findutils/manual/html_node/find_html/Worked-Examples.html) | A source lead for tasks and command composition. Check the selected example and GNU-specific assumptions during intake; this page could not be fetched in this preparation session. |
| Broad command coverage | [tldr-pages](https://github.com/tldr-pages/tldr) | Useful for seed recipes and discovering common tasks. Add interpretation and recovery evidence before treating a recipe as a complete investigation. |

For `strace`, `ss`, `lsof`, `ps`, `systemctl`, and `journalctl`, use their upstream examples and manuals for semantics, then find a complete investigation or reproducible issue matching the intended task. A general list of commands usually supplies only the execution portion.

Search patterns that help:

~~~text
<tool> <symptom> debugging example
<tool> <specific error> maintainer issue
site:<upstream-project-domain> <task> example
site:<upstream-repository> <error> reproducer
<tool> investigation output root cause
~~~

Follow search results to the original material. A search result, an article copying another article, or an LLM-generated explanation is a lead to verify.

## A small intake process

Use [intake.template.md](intake.template.md). Collect:

- one concrete task the agent should handle;
- relevant passages or a retrievable link to a practical source;
- a semantics reference for uncertain flags/defaults;
- an example of failure, ambiguity, or verification when available;
- known environment/version constraints.

Three sources are a useful starting shape, not a quota. A strong maintainer walkthrough may cover everything. Ten shallow lists may still leave interpretation missing.

Match intake effort to the tier. A needs evidence for the investigation and its decisions. B may need only a documented correction and the failure that motivated it. C needs no fabricated source packet or card. Capture real baseline failures early and use them to choose the next useful addition.

Use the [help-capture helper and workflow](capture-help.md) for version-labelled output, then pair it with applicable manual sections. Record both successful and failed captures accurately. A captured option's existence does not validate a pipeline, diagnostic inference or combination of flags.

For a supplied transcript, retain the initial question, environment, commands, stdout/stderr and exit codes when available, revisions to the hypothesis, and the final verification. A transcript that ends after a command ran cannot prove task completion.

Store only the needed source material or locators in a private/local intake area when appropriate. Remove credentials and identifying incident data before turning a private transcript into reusable examples. Publish concise paraphrases and citations; retain any required attribution for reused material.

Keep durable sources and command/claim mappings in the tracked [provenance companion](provenance.template.md) inside the portable skill. Raw intake can stay in `work/`; accepted provenance must not rely on that ignored directory. Keep verification statuses and material limitations in the runtime card so ordinary loading stays concise.

## When evidence is incomplete

If the sources explain invocation but not interpretation, produce a draft covering invocation and name the missing diagnostic evidence. Do not invent a root cause or a recovery sequence.

Prefer one well-supported workflow over a broad claim of tool expertise. It is legitimate to say: "This card covers examining an existing native core dump; live attach and reverse debugging are outside its current coverage."

If sources disagree, first compare versions, platforms, inputs, and privileges. Record an unresolved contradiction and exclude the disputed command or interpretation until checked. Newer material is not automatically more applicable to an older installed tool.

## Your best source after the first release

Use real agent runs as a backlog:

- The agent chose a tool that could not answer the question: improve selection.
- A command failed because of a version or environment assumption: improve preconditions.
- Correct output led to a wrong conclusion: improve interpretation.
- The agent stopped too soon or repeated itself: improve the next-step or completion criteria.

Keep the original run evidence outside the installed skill. Promote only the smallest general lesson supported by the run. Do not turn a single unusual incident into a rule for every use of the tool.
