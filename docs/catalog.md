# Skill catalogue for selective loading

[`catalog.json`](../catalog.json) is optional selection metadata for schedulers such as Board. It lists every physical skill once while leaving the flat, independently installable packages unchanged. A copied skill does not need the catalogue or repository helpers. The canonical name and discovery description remain in its `SKILL.md`.

## Schema version 1

```json
{
  "schema_version": 1,
  "library_id": "research-library",
  "skills": [
    {
      "id": "file",
      "path": "skills/file",
      "tags": ["execution:linux", "task:offline-analysis"],
      "requires": []
    }
  ]
}
```

This abbreviated example shows the shape, not the full catalogue. `id` must equal the package folder and frontmatter name; `path` is exactly `skills/<id>` relative to this checkout. Consumers identify a package across libraries using `library_id` plus `id`, and detect duplicate Pi names before exposing a combined selection. Paths must remain inside their package and library. Do not rename or copy packages to create category views.

Tags are overlapping facets, not exclusive folders:

| Facet | Meaning |
|---|---|
| `task:` | A supported task, such as `source-review`, `static-analysis`, `finding-triage`, `config-diagnostics`, `offline-analysis`, `data-inspection`, `archive-inspection`, `runtime-inspection`, `build-diagnostics`, `document-inspection`, `service-discovery`, `share-enumeration`, `ad-enumeration`, `ad-attack`, `credential-recovery`, `remote-execution`, `remote-access`, `authentication-testing`, `offline-cracking`, `web-enumeration`, `web-app-testing`, `exploit-execution`, `traffic-capture`, `asset-discovery`, `recon-pipeline`, `cloud-security`, `container-security`, `steganography`, `symbolic-execution`, or `windows-inspection`. The engagement task values are used by the reviewed security batch; schedulers should define profiles on explicit values rather than assuming a closed list. |
| `execution:` | The environment for the documented procedure: `execution:linux` for Linux-executed guidance, `execution:windows` where the skill's own procedure requires an established Windows execution context, `execution:cross` for verified cross-platform procedures. This classifies where the documented commands run, not the inspected target. Every entry carries exactly one execution tag. |
| `target:` | A known target technology, such as `rails`. Absence means unspecified, not unsupported. |
| `language:` | An explicitly supported language, such as `python`, `go`, `ruby`, `c`, `cpp`, `php`, `javascript`, `java`, or `csharp`. |
| `artifact:` | Relevant input/output kind, such as `source`, `binary`, `core`, `config`, `archive`, `json`, `document`, or `scan-report`. |

`requires` lists command names, never paths, for executables verified present on this controlled image (426 entries; for example `impacket-GetNPUsers`, `lsb_release`, `certipy-ad`, `qemu-system-x86_64`). An empty list means unspecified readiness — including tools absent from this image and Windows procedures whose binaries are intentionally not declared — not verified absence. Schedulers can report missing declared executables per selection.

`classification:unreviewed` marks entries whose routing classification has not been reviewed. Such entries retain `execution:linux` and make no `task:` claims; a reviewed entry must claim at least one `task:` value. This marker concerns catalogue classification only: its absence is not a claim of complete schema migration, runtime testing or worker effectiveness. The current classification reviews 110 entrypoints, including web-injection/API-discovery additions (dalfox, arjun, tplmap, kiterunner), a steganography group (zsteg plus reclassified steghide) and symbolic execution (angr in a dedicated venv, unicorn); including an 8-skill bug-bounty recon chain (subfinder, amass, httpx on httpx-toolkit, nuclei, katana, hakrawler, waybackurls, gau) and a cloud/container security set (pacu, scoutsuite on scout, s3scanner plus reclassified aws, az, terraform, consul, vault; peirates, kube-hunter, deepce, cdk plus reclassified kubectl, docker, docker-compose, dive, etcdctl, kubeletctl, docker-registry-grabber): the original 34 for source, runtime/build, configuration, data, archive, document and offline-analysis tasks, a 37-entry security engagement batch (recon, SMB/LDAP enumeration, AD attack, credential work, web and exploitation tooling, traffic capture), and 3 Windows-context procedures (`credentialmanager`, `powershell`, `sharp-gpoabuse`) tagged `execution:windows` from their own package text. Their conditional procedures were not revalidated as part of this metadata pass. The dated validation record identifies the reviewed sets. The remaining 472 packages remain explicitly unreviewed for classification.

Board checks declared executable names through the daemon account's PATH; the declared names above were verified present under that account (doctor reports no missing declared executables). Declaring a command does not grant permissions or enforce an execution boundary, and an undeclared prerequisite remains the skill's own responsibility to state.

## Board and Pi

This integration targets Debian-derived Linux hosts. `execution:linux` describes the documented execution environment; it does not establish tool installation or compatibility with other distributions.

Install the full checkout where the local Board daemon's worker account can read it. Add the absolute path to its `catalog.json` file to Board's `skills.catalogs` list, then select a small profile by task and technology. Board resolves matching catalogue records to complete skill directories; Pi receives only the selected directories through repeatable `--skill` arguments. Keeping `--no-skills` disables unrelated automatic discovery while explicit paths remain available in Pi 1.3. A root catalogue does not itself change Pi discovery.

Keep profiles and routing decisions in Board. Combine a small common selection with task/language additions; use separate facts for the worker's OS and the target technology. Missing classification or a missing tool is a recorded coverage gap, not permission to silently claim complete coverage. A profile may be selected explicitly when the initial task is ambiguous. Board's per-attempt manifest records profile IDs, catalogue/package hashes, source/snapshot paths and estimated metadata cost; retain Git revisions separately when needed. A later task can use a different selection without altering packages.

Skill metadata exposure, reading an entrypoint, following its conditional references, and a correct worker outcome are separate observations. The catalogue does not establish a fixed safe skill count or improved efficiency. Compare useful outcomes, omitted prerequisites, actual loading, irrelevant reads, time and usage on matched tasks before tuning a budget.

## Maintain and check

Add a record when adding a physical package. Review the actual supported task before replacing `classification:unreviewed` with factual facets; avoid inferring capabilities from the tool name alone. Keep prerequisites unknown until supported. Catalogue classification need not rewrite the skill body or replace its source/validation record.

```bash
python3 -B scripts/check_catalog.py
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
```

The standard-library checker rejects malformed/duplicate JSON keys, unknown schema fields, duplicate IDs/tags/requirements, noncanonical or escaping paths, name mismatches, unsupported facets, and missing/unknown packages. The repository checker includes it when a catalogue is present. No catalogue is required for an isolated skill copy. These checks establish catalogue consistency and packaging, not installed capabilities or successful scans.
