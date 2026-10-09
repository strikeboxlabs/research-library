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

## Keep collection small

Start with the task, relevant practical material and evidence for uncertain command semantics. The [intake template](intake.template.md) is optional. A short correction may need one source; a diagnostic workflow needs enough evidence to support its decisions. Follow observed agent failures when choosing what to add.

The [help-capture helper](capture-help.md) can record installed documentation. Check the relevant manual too when short help omits meanings or combinations. For transcripts, retain the original question, environment, commands, outcomes and the reasoning that connected them.

Keep raw/private input in ignored `work/`. Map source URLs/sections, originating document/pages, review dates and actual test findings to the affected skill in existing intake reports and `docs/validation.md`. Keep actionable version conditions and useful documentation fallback links in the skill. Preserve attribution and source mappings when relocating old notes; workers need no maintenance-file dependency. Remove credentials and identifying incident data from examples. Label invented output as illustrative.

## Resolve gaps before broadening coverage

If invocation is documented but interpretation is missing, narrow the draft and identify the unanswered question. When sources disagree, compare versions, platforms, inputs and privileges; newer documentation may not apply to the installed tool.

Use real worker failures to improve the affected instruction: selection, execution, interpretation or follow-up. Preserve the smallest general lesson supported by the evidence. Avoid turning an unusual incident into a rule for every use of the tool.
