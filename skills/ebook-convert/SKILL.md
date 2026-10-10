---
name: ebook-convert
description: Convert local e-books with calibre and diagnose format selection, omitted HTML resources and pipeline transformations. Use when a wrapper creates a directory unexpectedly or the output differs from its source.
---

# Convert with the actual format pair

Identify the installed calibre build and executable used by the job; a service can use a private copy instead of the one on PATH. Define `converter` as that executable's absolute path, `input` as the reviewed source file and `output` as a fresh absolute destination ending in the intended format, such as `.epub`:

~~~bash
"$converter" "$input" "$output" --help
~~~

The first two positional arguments select input and output. Format-specific options depend on both; general help alone may omit the relevant input plugin's controls. Keep an explicit output filename: a destination without an extension selects an OEB directory, while `.epub` alone requests a derived filename. Absolute paths also avoid leading-hyphen filename ambiguity.

Define `conversion_log` as a fresh private file, then run the reviewed conversion as an ordinary user:

~~~bash
umask 077
"$converter" "$input" "$output" >"$conversion_log" 2>&1
conversion_status=$?
~~~

Check status and diagnostics before accepting the output. Verify the expected content and structure using the intended reader; a created file or wrapper HTTP 200 does not establish a correct e-book. A wrapper timeout or HTTP error can leave output behind. Preserve that partial result and diagnose the failed stage before retrying into a new destination.

## Locate missing content

For an authorized diagnostic rerun, add `--debug-pipeline "$debug_dir"` with a new private directory. This still performs conversion and writes intermediate content; it is not a dry run. Inspect the earliest stage where the defect appears:

| Stage | Next decision |
|---|---|
| `input` | Missing text/resources here points to input parsing, encoding or resolution. |
| `parsed` / `structure` | Compare structural detection and transformations rather than changing the output format blindly. |
| `processed` | Correct content here but incorrect final output points to output-plugin behavior or the reader. |

HTML conversion can package referenced local resources. Current HTML input resolves paths and normally excludes resources outside the input document's directory tree. A warning about an outside-root resource calls for checking its intended location; relocate approved assets under the document root instead of routinely enabling `--allow-local-files-outside-root`. Historical builds can behave differently. Review links and the produced resource list before distributing a conversion of unfamiliar HTML; this operation is not passive text inspection.

For EPUB output, inspect the archive member list, package manifest and selected content files before extracting. Do not assume the body is always `index.html`, or that an unexpected member's suffix proves its content type. A historical converter's ability to read a local file does not establish shell execution or every current version's behavior.

Use the [format-pair command reference](https://manual.calibre-ebook.com/generated/en/ebook-convert.html), [pipeline guide](https://manual.calibre-ebook.com/conversion.html) and matching release's [HTML input code](https://github.com/kovidgoyal/calibre/blob/master/src/calibre/ebooks/conversion/plugins/html_input.py) to resolve plugin and resource differences.
