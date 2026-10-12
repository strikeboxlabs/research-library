---
name: magick
description: Inspect a selected image with ImageMagick 7 and identify its trusted build, policy, formats and delegate capabilities. Use when image metadata, decoding or a bundled binary differs from a workstation result.
---

# Inspect the selected ImageMagick 7 runtime and image

Read this entire SKILL.md before acting. Require a trusted installed ImageMagick 7 executable; define `magick_bin` as that selected invocation. Select runtime inventory or one reviewed ordinary-image inspection below. Use an owned trusted working directory and known configuration/loader environment for either task. No conditional resources are required. Finish with observed build/options or image properties, status and the remaining service-context or decoding gaps.

~~~bash
"$magick_bin" -version
version_status=$?
"$magick_bin" -list configure
configure_status=$?
"$magick_bin" -list format
format_status=$?
"$magick_bin" -list policy
policy_status=$?
~~~

Record the relevant version, quantum depth, HDRI/features and delegates with each status/diagnostic. Format rows indicate this build's declared read/write support; they do not establish that the task's input decodes or that every required external delegate is available. Effective policy can restrict an otherwise supported coder. An error or missing list is an incomplete inventory, not proof the feature is absent everywhere.

These commands execute the selected binary. For an executable recovered with source files, retain its provenance and inspect it statically first; a harmless-looking version option is still code execution. A source tree containing that binary does not establish that the web service currently invokes it. Match the application's actual binary, environment and policy before attributing behavior or an advisory; distribution patch state can differ from an upstream version string.

ImageMagick 7 uses `magick` for image processing and `magick identify` for inspection. ImageMagick 6's separate `convert`/`identify` programs can be different builds. Do not silently apply one build's options or results to another. Installation and policy changes are separate actions from this inventory.

## Inspect one reviewed ordinary image

Require the exact existing image, permitted resource budget and this binary's identify help/policy. Define `image` as its selected absolute path and `report`/`errors` as fresh outputs in an owned directory:

~~~bash
"$magick_bin" identify +ping "$image" >"$report" 2>"$errors"
status=$?
~~~

`+ping` asks for pixel as well as metadata characteristics; ordinary ping behavior can obtain properties without reading all pixels. Inspect status and diagnostics along with format, dimensions, frame identity and colorspace. A reported geometry is a decoder observation, not proof of the filename's extension, origin or pixel content's authenticity. Multi-frame files can produce several records. A partially reported image plus an error remains incomplete; inspect the selected input or supported format rather than silently loosening policy.

Run directly on the selected file instead of replaying a scheduled script that first empties its shared log. That reset discards prior results; newline-delimited find/xargs input can also split filenames. A changed log timestamp alone does not identify its writer, schedule or execution identity. Keep image inspection in the ordinary process context; no privileged launch or loader-library substitution is needed to obtain these properties.

References: [ImageMagick magick options and subcommands](https://imagemagick.org/magick/) and [identify properties and ping distinction](https://imagemagick.org/identify/).
