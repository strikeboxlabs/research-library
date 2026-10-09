# Source packet

Tool: {{executable/name}}
Skill name: {{normally the executable name; lowercase letters/digits/hyphens}}
Tier and reason: {{A / B / C; observed knowledge gap or provisional triage}}
Useful tasks: {{one to three concrete questions an agent should answer}}
Target environment: {{Linux distro/tool version if known; privileges; local/container/remote; otherwise unknown}}
Research mode: {{supplied-only OR browse-primary-sources}}
Execution: {{not authorised OR exact isolated fixture and permitted operations}}

For B, one correction and its supporting semantics may be enough; a full investigation transcript is optional. For C, record why the tool is deferred and what would justify new guidance; create no runtime package.

## S1

Title and author/owner:
URL or supplied artifact ID:
Publication/version/commit, if known:
Relevant section, line range, or transcript timestamps:
Material: {{paste the relevant content, attach the file, or permit the model to retrieve the URL}}

## Additional sources

Repeat the S1 structure as S2, S3, etc. Include a practical walkthrough and evidence of interpretation or troubleshooting when available. Do not manufacture a failure example to complete the packet.

## Captures and observed failures, when available

- Capture location and exact tool/environment version or image ID:
- Captured command, exit status and whether it completed:
- Applicable manual section for options absent from help:
- Agent failure: {{request, observation and the behaviour the skill should improve}}

Do not label help captures as successful workflow tests. Keep raw output in `work/`; move durable citations and claim summaries into the tracked provenance companion before accepting the skill.
