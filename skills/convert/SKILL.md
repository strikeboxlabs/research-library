---
name: convert
description: Crop an owned raster image or generate a small marked PDF with ImageMagick 6 convert. Use when offsets, canvas metadata, resolution, fonts or a PDF coder policy error make the result unreliable.
---

# ImageMagick 6 image operations

Read this entire SKILL.md before acting. Require ImageMagick 6 convert and fresh output paths. For an owned raster crop, read [crop geometry](references/crop.md) fully before acting. For the marked PDF below, also require an available font and enabled PDF writing. Finish with command status and decoded output/geometry; missing coder/font support remains a prerequisite gap.

Confirm `convert -version` identifies ImageMagick; a same-named filesystem utility is a different program. ImageMagick 7 uses `magick`, so establish its invocation separately. Use `convert -list policy` to inspect relevant coder restrictions.

## Generate an owned marked PDF

Use `convert -list font` to select an available font. Define `font` as that font name and `pdf_out` as a fresh absolute .pdf path outside application data.

For an approximately A4 page at an explicit 72 pixels per inch:

~~~bash
test ! -e "$pdf_out" && test ! -L "$pdf_out" &&
  convert -size 595x842 -units PixelsPerInch -density 72 xc:white \
    -font "$font" -pointsize 18 -fill black -gravity center \
    -annotate 0 'Owned document marker' "$pdf_out"
status=$?
~~~

The canvas size is pixels; density determines its physical interpretation in PDF. This produces a raster page with centered text, not a searchable vector-text document. Merely choosing 595x842 pixels does not guarantee a particular page size under inherited resolution. Explicit font selection avoids relying on an unavailable default.

Check status/stderr, then parse the PDF with the task's existing PDF reader and render its page to confirm the intended marker and dimensions. A file left by a failed command can be incomplete, and existence alone is insufficient. Choose a fresh path for a retry.

An operation-not-allowed-by-security-policy error is distinct from an unreadable font or missing delegate. Inspect the effective policy and intended PDF-writing permission; do not enable arbitrary input/delegates or read/write access globally to make a fixture succeed. Use an already approved PDF writer when this capability is unavailable. Policy edits and tool installation are separate changes, not part of this creation task.

Resolve implementation differences through the [ImageMagick 6 convert reference](https://legacy.imagemagick.org/script/convert.php/) and [density/options documentation](https://legacy.imagemagick.org/script/command-line-options.php/#density).
