---
name: pd4cmd
description: Convert reviewed HTML to PDF with PD4ML's Pd4Cmd Java CLI on Linux. Use to resolve legacy entrypoint mismatches, layout width versus paper size, external-resource access and incomplete or stale generated PDFs.
---

# Identify the installed wrapper before copying a command

Define `jar` as an absolute path to an existing trusted PD4ML distribution. An application-supplied JAR is executable code, including when invoked for usage information. Inspect its provenance/build first. Current distributions expose `com.pd4ml.tools.Pd4Cmd` as the JAR's main class; older applications may invoke a separately packaged `Pd4Cmd` class with `-cp`. A class-not-found error requires checking packaging and entrypoint, not changing the HTML or guessing flags. Use the installed build's usage; version families have different interfaces.

# Convert one reviewed input and verify this run's output

For the current Pd4Cmd interface, define `input_url` as the correctly encoded absolute `file:` URL of reviewed HTML, `html_width` as the intended layout viewport width in pixels, and `output_pdf` as a fresh path in the private output directory:

~~~bash
java -Djava.awt.headless=true -Xmx512m -jar "$jar" "$input_url" "$html_width" A4 -out "$output_pdf"
~~~

JVM options precede `-jar`. `html_width` controls the HTML layout viewport; A4 selects paper size. Changing one need not fix clipping caused by the other. `-out` directs the PDF to a file; without it the current CLI streams output to stdout. Preserve diagnostics separately and check the exit status, current-run file size and PDF readability. Render the relevant pages to check missing fonts/images, clipping and pagination. An old `result.pdf` left by a failed wrapper is not evidence that the latest input converted.

HTML conversion may load styles, images and embedded resources. The `pd4ml:attachment` element can embed another file in the PDF; a visible paperclip and extracted attachment are separate evidence from ordinary page text. Resolve resource URLs in the converter's execution context. A web wrapper's converter may have different filesystem and network access from the person submitting HTML. Keep resource access within the intended conversion inputs; neither headless mode nor a Java heap cap isolates that access. `-nohyperlinks` affects PDF link annotations and is not an external-resource access control.

If diagnosing a wrapper, trace the actual input chosen and output path. A loop that assigns a filename repeatedly but calls the converter once afterward converts only the final selected file. Zero matching rows, concurrent requests or random-name collisions can leave missing or stale output. Establish that input/output association before changing the converter or claiming a successful data read.

See the vendor's [current CLI reference](https://pd4ml.com/docs/pd4cmd-command-line-reference.html) and [resource/attachment examples](https://pd4ml.com/docs/usage-examples.html) when matching the installed build. Treat a legacy demo-JAR command as evidence about that deployment, not a universal launch syntax.
