---
name: xml-pp
description: Format bounded, trusted XML with the XML::Twig xml_pp CLI while preserving original bytes and detecting partial parser output. Use for whitespace/encoding differences and separating formatting from schema or security validation.
---

# Format XML without losing the original evidence

This is Perl XML::Twig's `xml_pp`. Check `xml_pp -h` and the installed package version; similarly named formatters may use different parsers. Use a bounded, trusted local input. Define `input` as its absolute filename and `formatted`/`errors` as new, distinct output paths:

~~~bash
if xml_pp -l -s indented -- "$input" >"$formatted" 2>"$errors"; then
    printf '%s\n' 'Formatting completed; inspect the result against the original.'
else
    printf '%s\n' 'Parsing failed; preserve diagnostics and do not accept the output.' >&2
fi
~~~

`-l` loads the document before printing, using more memory and avoiding the documented streaming mixed-content whitespace defect. Default streaming mode can already have emitted a prefix when parsing fails; a nonempty output file is not a successful parse. Success establishes parsing/serialization under this installation, not schema validity or the truth of fields such as `test-connection-db=OK`.

Keep original bytes for hashes, signatures and exact comparisons. Pretty printing changes layout; `-p 'pre code'` preserves whitespace within selected tags, while `-e utf8` deliberately converts output encoding and updates its declaration. `-i` replaces input files; use separate output for inspection. Never redirect output onto the same input path, because the shell truncates it before parsing.

Formatting is active XML parsing. The reviewed upstream CLI does not expose XML::Twig's `no_xxe` constructor option. A dependency method named `safe_parsefile` catches parse errors; it does not mean external entities are blocked. If input may contain untrusted DTD/entity references, stop and choose an explicitly configured parser in a constrained environment rather than running this command with sensitive file access. Pretty-printer naming or the absence of an entity-expansion switch is not a security guarantee.

For malformed/truncated input, retain the original and parser error location; verify the producing command's transport/status before editing bytes to make the XML parse. Capture HTTP response bodies to files before formatting instead of piping an unchecked response straight into a parser.

See the [xml_pp options and mixed-content caveat](https://metacpan.org/dist/XML-Twig/view/tools/xml_pp/xml_pp), [CLI implementation](https://github.com/mirod/xmltwig/blob/master/tools/xml_pp/xml_pp), and [XML::Twig parser options](https://metacpan.org/pod/XML::Twig) for differences between formatting and entity handling.
