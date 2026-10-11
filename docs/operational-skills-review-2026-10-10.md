# Review: on-demand operational knowledge

Reviewed 2026-10-10 against the user's supplied paper, **From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills**, Hong, Imani and Ahmed, arXiv:2607.01456v2 (3 July 2026). [Public paper](https://arxiv.org/abs/2607.01456v2).

**Status: the user accepted the lean direction on 2026-10-10; authoring now follows [schema v0.7](../authoring/schema.md).** The findings and proposals below preserve the original assessment. This is not a claim that every existing skill has already migrated. This document is authoring material, not a runtime dependency. The PDF ingestion queue remains separate; the paper was not added to it.

## Purpose and main conclusion

The repository should supply **on-demand operational domain knowledge that helps a capable agent make a better decision on a real system**. A command is one way to obtain evidence. The valuable knowledge often concerns identities, protocols, formats, execution context, causal relationships, misleading observations and the next discriminating check.

Keep independent installation, concise descriptions, early activation contracts, selective references and maintenance records outside the runtime. Change the emphasis of ingestion and evaluation before adding structural machinery. Our existing schema already supports much of this; a larger template would not solve the remaining problem.

The acceptance question should be: **What operational decision will this addition improve, under what conditions, and how would we tell?** A newly encountered command, an additional example and an additional skill are not automatically improvements.

## What the paper establishes, and its limits

The authors studied 238 selected public skills, derived authoring practices from 29 online sources, and defined 26 categories of potential quality problems. Their semantic detector was evaluated against 53 manually labelled skills, with reported weighted F1 of 0.78. They examined version histories as well. The useful result for us is a vocabulary for reviewing ambiguity, unnecessary context, missing checks and excessive prescription; this is not a runtime experiment establishing the benefit of each proposed remedy. Section V explicitly leaves the direct effect of individual smells on agent performance open. See pp. 3-5 and 7-10 of the supplied paper.

Treat the reported prevalence as a result under that sample, taxonomy and detector. It is not evidence that 99% of all skills fail. The sample favors popular English-language marketplace skills, and the practices come from practitioner literature. Table IV's heading says 228 whereas the surrounding account says 238; its displayed percentages broadly follow 238. This discrepancy does not invalidate the qualitative lessons, but it is another reason not to treat the percentages as a precise operational benchmark.

The following adaptations are our engineering judgment, not experimentally established prescriptions from the paper:

| Paper concern | Appropriate application here |
|---|---|
| Missing decisions, context or validation | Preserve the domain fact, relevant observations, alternative explanation and completion evidence when needed. |
| Excessively fixed command sequences | Explain the objective and invariant; let the worker choose equivalent commands where appropriate. Keep exact ordering when byte integrity, privilege boundaries or irreversible effects depend on it. |
| Unnecessary detail in the entrypoint | Move substantial independent task branches into directly linked local references. Keep a useful short procedure inline. |
| Weak discovery text | Describe the operational symptom or artifact and bounded capability. Avoid extending the description with every new source-specific case. |
| Missing scripts, templates, planning or feedback | Add these only when they solve an actual workflow problem. Their absence alone is not a defect in a short diagnostic skill. |
| Poor follow-through | Require the evidence needed for the requested conclusion; do not require irrelevant work to satisfy a checklist. |

Do not implement the taxonomy as 26 mandatory headings or hard-failing lint rules. In particular, do not require routine permission questions, a planning ceremony, a script or a persisted checklist for every tool. The paper's example of an unclear `dig` name concerns a library-documentation lookup skill, not the DNS utility; our `dig` name and DNS-specific description are coherent.

Do not inherit numerical limits mechanically. The paper defines its lengthy-body smell using 5,000 **words**. The current [Agent Skills specification](https://agentskills.io/specification) describes a recommendation below 5,000 **tokens** and below 500 lines. Neither supplies a measured optimum for this repository. Our 150-line check serves discoverability, not size optimization. [Anthropic's authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) also explicitly varies procedural freedom according to task fragility; command sequences are not intrinsically bad.

## Current repository findings

The inventory below was measured from all 165 entrypoints. Word counts use whitespace splitting and include frontmatter and code; they are not tokenizer measurements or observed harness context costs.

| Measure | Observed value |
|---|---:|
| Independently packaged skills | 165 |
| Median entrypoint length | 450 words |
| Words across all entrypoints | 83,209 |
| Words in description values across the catalogue | 4,714 |
| Characters in those description values | 33,942 |
| Largest entrypoint, Git | 1,642 words / 146 lines |
| Hashcat entrypoint | 1,591 words / 104 lines |
| Packages with supporting files | 7, containing 12 reference files |

These figures do not show that every worker loads all descriptions or bodies. They show the available catalogue's cost and why selected installation still matters. Most entrypoints are already short. The highest-value optimization is likely selective discovery and task cohesion, rather than indiscriminate compression of every file.

Representative content review covered GDB, strace, dig, ip, TShark, Git, Hashcat and PHP, alongside the authoring and evaluation documents. This was not a semantic audit of all 165 skills.

| Finding | Concrete example and implication |
|---|---|
| Operational reasoning already exists | [dig](../skills/dig/SKILL.md) distinguishes server response, authoritative/cached views and application resolution. [ip](../skills/ip/SKILL.md) distinguishes a route lookup from successful delivery. Preserve this content. |
| Examples can teach evidence limits | [GDB](../skills/gdb/SKILL.md) distinguishes locating an assertion from explaining its origin and handles missing debug evidence. This is a stronger model than a command catalogue. |
| Repeated enrichment creates unrelated branches | [Git](../skills/git/SKILL.md) combines historical evidence, remote configuration, hooks, patch validation and stored link/submodule modes. Its top-level navigation is useful, but whole-file reading loads all branches. Consider extracting substantial alternatives with their own required inputs. |
| Specialized formats accumulate in common paths | [Hashcat](../skills/hashcat/SKILL.md) keeps an inline OFBiz conversion while Gitea conversion already lives in a conditional reference. Use the latter approach where it saves real task context. Preserve the common input/run/result logic. |
| Some modes have an obvious conditional boundary | [PHP](../skills/php/SKILL.md) includes a PostgreSQL fallback program alongside configuration, upload, PHAR and encoding guidance. The database fallback is a candidate for selective loading. |
| Documentation quality is ahead of performance evidence | The [evaluation guide](../evaluation/README.md) and [pilot cases](../evaluation/pilot-cases.md) define useful comparisons, but no Linux worker comparison has established benefit yet. |
| Catalogue metadata can drift | README referred to 144 skills while the actual inventory contains 165. Prefer avoiding a hand-maintained total in narrative text. |

The first-read policy is partly migrated: GDB, for example, has useful prerequisites and a conditional reference but lacks the newer explicit whole-entrypoint instruction. This should be corrected during its next substantive review; a missing sentence does not by itself prove runtime failure. Do not claim that passing a line-count check validates the contract across the library.

## Proposed minimal schema adjustment

Keep `name`, `description`, Markdown and optional package-local resources. Do not add required YAML properties, a knowledge database or per-skill provenance files.

Add this purpose statement near the beginning of the schema and authoring prompt:

> Supply on-demand operational knowledge for a capable CLI agent. Retain the non-obvious system model, conditions and evidence that change its next decision. Commands implement those decisions. Prefer a small supported lesson over comprehensive tool coverage.

Expand the existing content guidance with the following considerations, **not mandatory sections**:

| Consideration | Question the author should answer |
|---|---|
| Operational question and applicability | What symptom, artifact or uncertainty makes this useful? Which environment conditions matter? |
| Relevant system model | What non-obvious protocol, identity, format or causal relationship prevents a likely mistake? |
| Discriminating action | What observation separates plausible explanations? What is a sensible default and when should it change? |
| Evidence and next decision | What does the result support, what remains unknown, and when can the worker stop or change course? |

Keep precise commands when they save trial and error. Identify which constraints are essential and which values are examples. Do not turn an explanation into a compulsory extra step. For example, understanding cached DNS does not require enumerating every resolver on every invocation.

A proposed lean body pattern is: a short activation/applicability statement; the useful domain fact and starting action; interpretation and the consequential alternative; completion evidence. Longer tasks may use a small task map with conditional references. The shape follows the task.

Retain recognizable tool names and independent folders. A coherent operational task may eventually deserve its own independent skill if cross-tool selection is the actual capability gap. Do not reintroduce `linux-cli`, install a master router, or require sibling skills. For now, preserve such cross-tool lessons in the intake report as candidates instead of forcing them into a random tool file or discarding them. Packaging a task skill should follow a concrete supported use case and evaluation.

## Proposed ingestion workflow

Continue sequential processing and full document coverage. Efficiency comes from better synthesis and less duplication, not skipping pages or labelling partial work complete.

1. **Extract the operational lesson before assigning a tool.** In the current PDF's working notes, capture the question, relevant conditions, consequential observation, why it mattered and next decision. Preserve any important connection between tools. Several commands can teach one lesson; a tool mention can teach none.
2. **Separate evidence from the author's explanation.** Distinguish what the source demonstrates, what its author infers and what upstream documentation establishes. A successful CTF chain does not establish that each explanatory claim is true or that its sequence is generally appropriate.
3. **Compare with current coverage.** Choose correction, replacement/merge, useful extension, conditional reference, new independent skill, or no runtime change. Record the decision in the existing intake report. A fully reviewed PDF with no useful delta is a legitimate completed intake.
4. **Verify the consequential new claim.** Reuse a mapped, applicable prior primary-source verification when its conditions still match. Retrieve new evidence for changed options, versions, interpretation or unresolved claims. A cached reference to an unpinned upstream branch is not permanent verification. No new citation database is required.
5. **Write for transfer.** Remove source-specific paths, secrets, incidental tool order and unjustified certainty. Keep the conditions that explain success. Preserve a useful healthy, failed or incomplete-evidence branch when it changes the decision. Do not manufacture a worked transcript to fill a template.
6. **Review the whole affected task.** Merge overlapping guidance instead of appending another paragraph for each source. Check that new material does not contradict older advice or widen the description beyond actual coverage. Move substantial alternative workflows only when doing so reduces irrelevant reading; include their inputs, relevant invariants and completion evidence so the reference is usable.
7. **Validate, record and checkpoint.** Use the existing focused checks and repository checks appropriate to the edits. Record page coverage, new or corrected decisions, affected files, sources, checks and limitations before completing the queue item. Keep raw extraction and detailed fixtures outside runtime skills.

The authoring prompt should explicitly permit both **no change** and **replacement of weaker existing text**. “Enrich existing skills first” must not be interpreted as “append something to an existing skill for every PDF.”

The intake note needs only a concise sentence such as: “This source corrects interpretation X under condition Y; merged into task Z; verified against source A; worker benefit remains untested.” Use the existing record, not another required companion file.

## Operational sources and testing priorities

CTF writeups are useful evidence for unusual tool behavior, but this intake is heavily selected for successful attack paths. They provide limited evidence for production constraints, ordinary healthy behavior, alternative causes, failed investigations and the cheapest useful diagnostic path. Keep their useful lessons, then prioritize maintainer incident analyses, operational postmortems, reproducible support issues and actual Pi worker failures for the next collection phase. The existing [source guide](../authoring/sources.md) already identifies much of this material; the change is what we prioritize in practice.

Do not equate this operational focus with excluding source code. Reading a wrapper or implementation can establish why a running system behaves as it does. The question is whether that knowledge supports an operational task, rather than teaching generic software development.

Run a small Linux pilot before refactoring the whole library. Start with:

- GDB: recorded failure with matching artifacts versus missing debug evidence, using the existing pilot.
- DNS: authoritative and consuming resolver views disagree; a different case is a server/transport error rather than a missing record.
- Hashcat input preparation: synthetic records with correct versus mismatched format/cost/salt evidence; no online authentication or recovery is necessary to evaluate the input decision.

For a proposed restructuring, compare **no skill**, **current skill**, and **revised skill** in fresh equivalent sessions. Keep the model, harness, documentation access, permissions, fixtures and budgets equal. Grade supported conclusions and recovery, not whether the worker copied our commands. Change names, values and important conditions between cases so reproduction of the writeup cannot masquerade as transfer.

Measure separate costs: discovery metadata available to the worker; entrypoint and references actually loaded; tool calls, retries and irrelevant reads; elapsed time and model usage where exposed. Count incorrect confident conclusions separately from justified incomplete results. Prefer equal or better task outcomes at lower cost; a shorter file that increases retries is not an efficiency win. Existing checks establish packaging and syntax, not these benefits.

Test discovery as well as execution: a normal symptom request, explicit invocation, and a nearby task where the skill should remain unused. Test the actual worker's installed skill set. This checks whether shorter descriptions preserve useful selection and whether adding similar task skills causes competition.

## Suggested implementation order

1. Amend the schema, create/review prompts and source guidance with the operational purpose, evidence separation, no-change/merge decision and transfer check. These are small authoring edits; most of the current process remains suitable.
2. Apply them during subsequent intake. Keep a short list of cross-tool lessons and repeated worker mistakes in the existing report rather than growing a second runtime catalogue.
3. Pilot conditional extraction in Hashcat, PHP and Git, one at a time. Choose coherent task boundaries; do not split every paragraph or duplicate the entrypoint into each reference.
4. Run the Linux comparisons and improve the observed weak points before mass migration. Add context-cost reporting to existing maintenance checks only if recurring measurements justify it. Do not introduce an LLM “smell score” as a release gate.

## Review coverage and status

Read text from all 12 pages of the supplied PDF and visually inspected pp. 7-9, including Figure 2 and Tables III-IV. Checked the public v2 record, current Agent Skills specification and applicable Anthropic authoring guidance. The supplementary repository linked by the paper was unavailable through the browser tool; its code and detector were not evaluated.

Inspected the current schema, creation/review prompts, templates, getting-started instructions, source guide, harness rationale, evaluation guide/cases and representative skills. Inventoried all entrypoints. No Linux fixture, live harness comparison or causal performance test was run. No blanket skill migration or automatic detector-based rewrite is claimed.

Post-save repository check passed: 165 skills, 207 Markdown files, 271 local links and 382 Bash blocks. Bash was parsed only; examples were not executed. Active schema v0.6 and runtime skills were unchanged by this review. README gained the review link and its stale numeric total was removed. Compromised.pdf remains honestly checkpointed in_progress for the next intake continuation.

## Accepted direction and rollout

The user clarified that capable Pi workers operate in a task graph, retry and revisit skills. The goal is useful support at low repeated context cost, not exhaustive procedures or mandatory fields. Preserve two functions: discover an existing tool before reimplementing its capability, then load deeper operational knowledge on demand. Keep short common guidance in the entrypoint and substantial task procedures/options/examples/interpretation in conditional references.

The user confirmed that no reliable tool/path inventory reaches workers, then clarified that these skills target one Linux distribution/image whose binary placement they control. The later on-box pass will enrich the existing skill references, or a concise references/environment.md, with actual absolute invocations and relevant version/options. Stable shared-image facts may be committed with the package. The initially proposed per-host deployment-copy layer was removed as unnecessary. No actual Linux inventory or deployment was performed here; path enrichment remains for later.

Schema v0.7, authoring/review and host-adaptation prompts, setup/source guidance and the continuation workflow now encode this direction. Every existing package revisited during intake is reconciled with the schema, not merely appended to. Existing intake reports record which skills were reviewed and what changed; conforming/no-change outcomes count as reviews. At batch completion, report remaining unreviewed skills rather than assuming the entire library migrated. The user's future 300+ PDFs are not silently added to the current fixed queue.

Small operational comparisons remain useful for repeated weaknesses, but are not a prerequisite to each ingestion or incremental cleanup. No universal performance gain, live worker evaluation or complete-library conformity is claimed.


## Hermes contributions and controlled-image review — 2026-10-10

Reviewed four new Hermes-authored packages against schema v0.8: **binwalk, chntpw, nikto and sslscan**. All four were untracked files in the shared checkout reached by the Hermes and Pi skill-directory symlinks. Existing GitHub changes were retained before integrating this batch. These four complete entrypoints, including their first 150 lines, were reviewed; the other 265 packages were not reviewed for schema conformity in this batch. No new supporting resources are required by these short, independent workflows.

| Package | Accepted task and corrections |
|---|---|
| binwalk | Signature identification, entropy interpretation and selected extraction/carving. Clarified Python implementation versus Binwalk release numbering, current-directory output base, regex carving and root/extractor identity. A local fixture exposed an entropy JIT failure despite exit status zero; documented the tested per-command workaround and remaining diagnostics. |
| chntpw | Offline local-account listing and selected edits on a preserved hive copy. Separated account selection from the interactive menu, save evidence from login success, and allocation constraints from safe logical edits; documented the manual's automatic-save behavior for `-L`. |
| nikto | Scoped web survey and candidate interpretation. Corrected `-Format txt` and information-disclosure tuning category `3`; made active requests, bounded coverage and confirmation evidence explicit. |
| sslscan | Active TLS protocol/cipher and certificate survey. Removed the undocumented `--no-failed` argument, qualified cipher/Heartbleed conclusions and connection failures, and identified SNI/STARTTLS prerequisites. |

All four now use observed absolute executable paths and early completion evidence. Removed routine review-date footers and unsupported claims that sample transcripts were verified captures; retained useful examples as explicitly illustrative. Version/option sources, actual execution and limits are in the [validation record](validation.md#hermes-skill-contributions--2026-10-10). This batch does not establish Linux runtime behavior for the other packages or worker performance.


## Controlled-image environment updates — 2026-10-11

Reviewed the local additions to six existing entrypoints: **ffuf, impacket-secretsdump, masscan, nmap, openvpn and rustscan**, using schema v0.8 for the changed guidance. Confirmed installed invocations, removed duplicate Nmap environment notes, and moved this review date/test history into maintenance records. Existing GitHub changes, including ffuf's saved-result interpretation, were retained. No new packages were accepted and the catalogue is unchanged.

The accepted additions cover ffuf catch-all interpretation, scanner route/completion evidence, retained OpenVPN session lifecycle and missing RustScan prerequisites. Whole affected entrypoints and relevant scanner/VPN references were read to check placement and contradictions; this is not a full operational audit of every pre-existing procedure. Other packages were not reviewed for schema conformity. Blanket speed/compatibility claims and a blanket claim that all Impacket tools are installed were narrowed to observed facts. The submitted VPN scan benchmarks were not independently reproduced and remain in the local draft backup.

Two new draft packages (**imap-enumeration**, **roundcube**) and the multipart exploit-construction guidance were excluded from publication because they include exploitation, phishing or cross-account access procedures. Their original local content was preserved. The accepted change adds no such procedures. Validation and its execution limits are recorded in [the validation record](validation.md#controlled-image-environment-updates--2026-10-11).
