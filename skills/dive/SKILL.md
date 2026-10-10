---
name: dive
description: Inspect Docker image layers from a local archive and locate earlier versions of removed files. Use when the final filesystem hides build-time data or layer filters and efficiency results obscure the evidence.
---

# Inspect image history from an archive

Define `archive` as an existing absolute path to a Docker image archive. Check `dive --version` and `dive --help` for that build's archive and output support. Use the explicit archive source to inspect the acquired file without importing it into a daemon or running its workload:

~~~bash
dive "docker-archive://$archive"
~~~

A bare image name normally selects the Docker engine instead. A container filesystem export is not a substitute for an image archive containing historical layers. Newer archive layouts and compression may need a newer parser; preserve parse errors instead of adding `--ignore-errors` and claiming complete coverage.

## Locate a change in the terminal UI

Use a terminal-capable session. In the layer pane, arrows select a layer; `Ctrl+L` selects current-layer changes and `Ctrl+A` aggregated changes. `Tab` switches to the file pane. There, `Ctrl+U` toggles unmodified entries, `Ctrl+R` removed entries and `Ctrl+M` modified entries. These hide/show categories; they do not alter the image. Use the displayed key hints if configuration differs, and clear text/category filters before concluding a path is absent.

**Illustrative case:** `app/db.sqlite3` is removed in layer 8. Record that layer and path, then find the most recent earlier layer containing its bytes. Layer 7 need not contain it: layers are changesets, not complete filesystem snapshots. Retain separate versions when a later layer modifies the same path.

## Work without an interactive terminal

Where the installed help supports `--json`, define a fresh `report` path in an existing directory:

~~~bash
dive --json "$report" "docker-archive://$archive"
~~~

Inspect the exported schema: current output includes ordered layer metadata and file lists, not recovered file contents. Retain parsing diagnostics and map layer identifiers to the archive manifest. `CI=true` instead selects an efficiency-rule evaluation; a failing efficiency threshold is not necessarily an unreadable archive, and passing it is not a secret scan. Do not assume JSON export also evaluates CI rules.

## Recover selected bytes

List the outer archive and inspect its manifest to establish the selected image and layer order. Do not order layer directories alphabetically or assume every history entry creates a layer. Define `layer_member` as the exact listed member containing the desired layer, `layer_tar` as a fresh working file, `member` as the exact regular-file path inside that layer, and `recovered` as a fresh output:

~~~bash
umask 077
tar -tf "$archive"
tar -xOf "$archive" "$layer_member" > "$layer_tar" &&
tar -tvf "$layer_tar"
# After confirming the intended member's name, type, uniqueness and size:
tar -xOf "$layer_tar" "$member" > "$recovered"
~~~

Check every command's status before consuming its output. Keep each layer separate; extracting all layers into one directory is not correct filesystem reconstruction. A `.wh.name` marker hides a lower-layer path, and `.wh..wh..opq` hides lower children of a directory. Such markers contain no deleted file bytes. Earlier bytes remain recoverable only if they actually exist in the supplied layers; data created and removed before a layer was committed may be absent entirely.

Preserve archive identity, manifest selection, layer order, member path and recovered-file digest. A recovered database or configuration is a historical snapshot, not proof of current account access. See [Dive's controls](https://github.com/wagoodman/dive) and the [OCI layer rules](https://github.com/opencontainers/image-spec/blob/main/layer.md) for interpretation differences.
