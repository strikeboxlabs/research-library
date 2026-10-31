---
name: "rea"
description: "Reverse-engineer applications and native binaries with REA's agent-facing CLI: JavaScript/Electron analysis without a provider and native analysis through the installed Ghidra. Use when a task needs evidence-backed explanations of how a feature works without source code."
---

# REA reverse engineering

Installed invocation: `/usr/local/bin/rea`, version `6.7.0` (npm package rea-agents; Node 24.21.0 runs it in practice, though upstream documents a 24.22.1 floor). Reference checkout of the project lives at /opt/rea; the runtime is the npm package, not the checkout.

Read this entire SKILL.md before acting. Require the acquired target (app directory, ASAR or binary) and authorization to examine it — REA's own position is lawful research on software you own or are authorized to analyze. Finish with REA's findings plus their evidence and stated limitations, not just conclusions.

JavaScript/Electron analysis needs no provider and runs as a single command producing JSONL progress then results:

~~~bash
/usr/local/bin/rea analyze-javascript-application /absolute/path/to/app --json
~~~

Native binary analysis needs a provider; this image has Ghidra (`/usr/bin/ghidra`, 12.1.4) — configure it as the native provider per REA's CLI guide before native commands (`rea --help` lists them). Analysis runs locally; results carry the evidence (functions, references, pseudocode traces) behind each claim, and the agent's job is to read that evidence, not trust the summary.

Two operational notes. Analyses are long-running on real apps (a 6,177-file analysis took minutes of phase progress): launch them as background jobs writing to a file, and never block a pipeline waiting on one. And npm's default blocks frida's install scripts, so runtime-instrumentation features need `npm install -g --allow-scripts=frida rea-agents` once before use — static analysis is unaffected.

MCP registration is for interactive agents with per-agent config, and Hermes on this image is registered at staging time (stdio server `/usr/local/bin/rea mcp`, validated with `rea mcp doctor`; a Hermes restart loads it). Pi itself supports MCP, but Board's worker launcher does not register per-worker MCP servers, so workers use the CLI form above. The worker investigation loop that CLI supports end to end: launch an analysis as a background job on the acquired target, read the JSON results file for modules/boundaries/evidence, then run targeted follow-up analyses on what the evidence names — a full investigation is a series of one-shot commands, not a persistent session.

References: [project documentation](https://github.com/morluto/rea), [CLI guide](https://github.com/morluto/rea/blob/main/docs/cli.md).
