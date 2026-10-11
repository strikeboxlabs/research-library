---
name: magick
description: Identify the trusted ImageMagick 7 build and its available configuration, formats and delegate capabilities. Use when an application's bundled binary differs from a workstation decoder or a version banner is insufficient evidence.
---

# Identify the selected ImageMagick 7 runtime

Read this entire SKILL.md before acting. Require a trusted installed ImageMagick 7 executable; define `magick_bin` as that selected invocation. No conditional resources are required. Finish with observed build/options and the remaining service-context or decoding gaps.

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

Reference: [ImageMagick magick options and subcommands](https://imagemagick.org/magick/).
