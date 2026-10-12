---
name: ruby
description: Identify a selected Ruby/Psych environment, check source syntax or confirm an owned WinRM certificate session with the installed Ruby gem. Use for loader provenance, relative inputs, client key protection and TLS verification decisions.
---

# Establish the actual Ruby runtime and input contract

Read this entire SKILL.md before acting. Require the selected trusted Ruby environment and the selected task's inputs. For YAML-consuming code, read [YAML inputs and working directory](references/yaml-inputs.md) fully; for an owned WinRM endpoint with an already issued client certificate, read [certificate session](references/winrm-certificate-session.md) fully before its fixed identity check. Otherwise use the local runtime/syntax steps below. Finish with actual provenance and selected task evidence, or the failed stage and missing dependency.

Define `ruby_bin` as the actual executable selected by the application or permitted invocation. A shell's default Ruby can differ from an absolute interpreter or a Bundler-managed runtime:

~~~bash
"$ruby_bin" --version
"$ruby_bin" -rpsych -e 'puts RUBY_DESCRIPTION; puts "Psych=#{Psych::VERSION}"; p Psych.method(:load).source_location'
~~~

The second query loads the trusted installed Psych library and reports its version and load method's source location. It does not import the acquired application or deserialize its input. Loading a library still executes its initialization: establish the intended startup/load-path environment rather than running this inside an untrusted dependency tree. Preserve startup/load errors as gaps. A native or replaced method can have no Ruby source location; do not invent one.

Match this provenance to the actual source and deployment context. Another installed interpreter, gem search path, startup option or application wrapper can select different code. The interpreter's major/minor version does not uniquely establish the loaded Psych behavior. Retain full exception frames and input paths when available; an abbreviated stack cannot establish everything that occurred before failure.

For a selected bounded acquired Ruby file, define `source_file` as its absolute path and run `"$ruby_bin" -c -- "$source_file"` in the trusted startup environment. Retain status and diagnostics. Syntax OK means the interpreter parsed that input; it does not load the file's required gems, connect to its endpoint or validate its options. Do not run the application to resolve a missing dependency during source review.

See [Ruby command-line options](https://docs.ruby-lang.org/en/3.4/ruby/options_md.html), [Psych version and loader API](https://docs.ruby-lang.org/en/3.1/Psych.html) and [method source locations](https://docs.ruby-lang.org/en/3.1/Method.html#method-i-source_location).
