---
name: ruby
description: Identify a selected Ruby/Psych environment and review YAML input resolution without running acquired application scripts. Use when interpreter banners, relative filenames or version-dependent loader behavior produce misleading conclusions.
---

# Establish the actual Ruby runtime and input contract

Read this entire SKILL.md before acting. Require the selected trusted Ruby environment and acquired source/error evidence. Use the runtime query below only in that trusted environment; for YAML-consuming code, read [YAML inputs and working directory](references/yaml-inputs.md) fully before interpreting its path or loading behavior. Finish with observed runtime/library provenance, source-to-input mapping and remaining gaps; a version banner alone is insufficient.

Define `ruby_bin` as the actual executable selected by the application or permitted invocation. A shell's default Ruby can differ from an absolute interpreter or a Bundler-managed runtime:

~~~bash
"$ruby_bin" --version
"$ruby_bin" -rpsych -e 'puts RUBY_DESCRIPTION; puts "Psych=#{Psych::VERSION}"; p Psych.method(:load).source_location'
~~~

The second query loads the trusted installed Psych library and reports its version and load method's source location. It does not import the acquired application or deserialize its input. Loading a library still executes its initialization: establish the intended startup/load-path environment rather than running this inside an untrusted dependency tree. Preserve startup/load errors as gaps. A native or replaced method can have no Ruby source location; do not invent one.

Match this provenance to the actual source and deployment context. Another installed interpreter, gem search path, startup option or application wrapper can select different code. The interpreter's major/minor version does not uniquely establish the loaded Psych behavior. Retain full exception frames and input paths when available; an abbreviated stack cannot establish everything that occurred before failure.

See [Ruby command-line options](https://docs.ruby-lang.org/en/3.4/ruby/options_md.html), [Psych version and loader API](https://docs.ruby-lang.org/en/3.1/Psych.html) and [method source locations](https://docs.ruby-lang.org/en/3.1/Method.html#method-i-source_location).
