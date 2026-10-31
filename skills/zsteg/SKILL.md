---
name: "zsteg"
description: "Detect hidden data in PNG and BMP images with zsteg through LSB plane, channel and extra-data analysis. Use for CTF-style image steganography where steghide (JPEG/WAV) cannot apply."
---

# zsteg image steganography

Installed invocation: `/usr/local/bin/zsteg`, version `0.2.14` (Ruby gem).

Read this entire SKILL.md before acting. Require the acquired image file and a record of checks run. Finish with extracted candidates or a bounded negative statement covering the planes checked.

~~~bash
/usr/local/bin/zsteg -a "$image"
~~~

`-a` runs all detection methods — LSB planes across channels, bit orders and extra-byte analysis. Without it, the default run covers a smaller subset; for CTF images `-a` is the baseline. `--lsb`, `--bits`, `--channel` and `--order` reproduce a specific plane when a candidate needs targeted re-extraction.

Interpret hits with compression-noise awareness: photographic PNGs routinely show low-order-plane 'text' patterns that are noise, so a zsteg string hit is a candidate, not a finding — extracted data should decode to something coherent (valid archive, readable text) before it counts. Absence of candidates after `-a` bounds PNG/BMP plane analysis only; other carriers (JPEG, WAV, containers) need other tools (steghide, binwalk).

References: [project documentation](https://github.com/zed-0xff/zsteg).
