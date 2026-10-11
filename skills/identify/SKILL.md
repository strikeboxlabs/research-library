---
name: identify
description: Inspect one owned raster image's format, geometry, frames and metadata with ImageMagick identify. Use when a profile, signature or successful header read is being mistaken for complete file validation.
---

# Inspect the selected image

Read this entire SKILL.md before acting. Require a trusted installed ImageMagick decoder, one owned regular raster input and the intended processing environment. No conditional resources are required. Finish with command status, relevant geometry/properties and decoding limits.

For ImageMagick 6, define `input` as an absolute file path:

~~~bash
identify -version
identify "$input"
summary_status=$?
identify -verbose "$input"
detail_status=$?
~~~

For ImageMagick 7, use `magick identify` in each image command and `magick -version` for the build. Establish which binary actually runs; the workstation's identify build can differ from an application's magick. Querying even a binary's version executes it, so do not run an acquired executable merely to identify it.

Keep stderr and both statuses. Summary rows identify format, dimensions, page geometry and frame number; multiple rows can represent a multi-frame image. Verbose output adds properties, profiles and pixel statistics. Missing profiles do not prove the file lacks all metadata. A successful quick identification can rely on metadata rather than decode every pixel; use the intended full decoder and inspect/render the result when pixel validity matters. Raw raster input needs known depth, dimensions and format rather than a guessed extension.

The displayed image signature derives from pixel components, not every file byte or metadata field. Use a whole-file digest separately when byte identity matters. `Tainted: False` is an ImageMagick state label, not a safety verdict. A profile property is observed metadata, not proof that every referenced path was opened or that a service uses the same decoder/policy.

Identification parses input and can engage coders/delegates. Use the selected restricted processing environment for untrusted artifacts, and retain policy/unsupported-format errors as capability gaps. Do not relax coder policy globally to make an inspection succeed.

References: [ImageMagick 6 identify](https://legacy.imagemagick.org/script/identify.php/) and [ImageMagick 7 identify](https://imagemagick.org/identify/).
