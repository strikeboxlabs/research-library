---
name: qrencode
description: Generate a QR image from selected local data with libqrencode qrencode. Use when exact input bytes, output format, scan margins or symbol capacity affect a generated code.
---

# Generate the selected QR artifact

Read this entire SKILL.md before acting. Require installed qrencode, the reviewed data file and a fresh output path in a private working directory; no conditional resources are required. Generate the image, check status and inspect it. Finish with the input/output identities and any decode comparison; unavailable decoding remains an explicit verification gap.

Define `data` as the absolute input file, `output` as a new absolute PNG path and `diagnostics` as a fresh private log. Inspect installed version/help, including PNG support:

~~~bash
qrencode --version
qrencode --help
umask 077
qrencode -8 -r "$data" -t PNG -l M -s 6 -m 4 -o "$output" 2> "$diagnostics"
status=$?
~~~

`-8` encodes the supplied bytes rather than applying case/Kanji transformations; `-r` avoids placing data in argv. Preserve significant newlines and encoding. Command-line strings have shell and NUL constraints; a QR image is neither encryption nor validation of its contents.

Here M selects error correction, six pixels per module and four modules of margin. More error correction reduces capacity. Keep the quiet margin and avoid interpolated resizing; DPI changes metadata rather than encoded content. Let symbol version adjust unless the consumer requires a particular version. `--strict-version` rejects excess data instead of enlarging the requested symbol. A capacity or missing-PNG-support error requires different recovery; preserve diagnostics rather than truncating the input.

Inspect the actual PNG and, when an appropriate decoder is available, compare its decoded symbol/data with the intended input. Do not treat a successful write or a URL-looking payload as evidence of a fetch or consumer acceptance. Structured append produces multiple numbered images and requires consumer support, outside this single-symbol procedure.

See the upstream [CLI manual](https://github.com/fukuchi/libqrencode/blob/master/qrencode.1.in) and [input/output implementation](https://github.com/fukuchi/libqrencode/blob/master/qrenc.c) for format/build differences.
