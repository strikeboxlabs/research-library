---
name: mogrify
description: Convert a selected batch of owned raster images with ImageMagick Mogrify while controlling output paths, overwrites and per-file failures.
---

# Batch image conversion

Read this entire SKILL.md before acting. Require a trusted installed ImageMagick invocation, selected ordinary raster inputs and a fresh writable output directory. Run as the ordinary user. Finish with input/output correspondence, command status and a visual check of the requested conversion; report missing coders or failed files rather than calling a partial batch complete.

Choose the invocation actually installed: `mogrify_cmd=(magick mogrify)` for the ImageMagick 7 interface, or `mogrify_cmd=(mogrify)` when that executable is supplied. Do not infer its absolute location from a different machine.

~~~bash
"${mogrify_cmd[@]}" -version
~~~

Mogrify normally changes original files. `-format png` changes the output suffix, but a same-format input can still name an existing file. Use `-path` to separate outputs. Inspect selected filenames first: two inputs with the same basename and different extensions can both map to one PNG name. Split or rename owned working copies before conversion when names collide. Require ordinary single-frame inputs for this simple batch; multi-frame files need an explicit frame/output naming plan.

Define `outdir` as an absolute path to a new directory under the owned workspace, and `inputs` as a Bash array of selected absolute input paths. The directory creation deliberately fails if that path already exists:

~~~bash
if mkdir -m 700 -- "$outdir"; then
    for image in "${inputs[@]}"; do
        if "${mogrify_cmd[@]}" -path "$outdir" -format png "$image"; then
            printf 'converted: %s\n' "$image"
        else
            printf 'conversion failed: %s\n' "$image" >&2
            break
        fi
    done
fi
~~~

Keep stderr and inspect each expected output before accepting it. A successful earlier file remains after a later failure; neither loop completion nor directory existence proves complete coverage. Verify dimensions, format and appearance against the requested result. A suffix is not evidence of the decoded format. Broad `*.*` input can include unrelated files, and a process-name kill can affect another conversion; use explicit selected files and track the owned process when cancellation is needed.

See [Mogrify usage and overwrite behavior](https://imagemagick.org/mogrify/) and [output path options](https://imagemagick.org/command-line-options/#path) for implementation differences.
