# Review the selected YAML consumer

Use the deployed/acquired source, selected interpreter/library provenance and the process's observed working directory. This is a source and diagnostic review; do not execute an acquired script or object-tagged YAML to discover its behavior.

Follow the complete call path: where the input name originates, directory changes, file opening, loader call/options and the later operations on its return value. A source excerpt ending in an ellipsis cannot prove that a function is called or that later type/version checks protect an earlier deserialization operation. Distinguish a filename, file bytes, parsed nodes and constructed Ruby objects.

## Resolve the input from the process context

An ordinary relative `File.read("dependencies.yml")` uses the process working directory, not the directory of the script named on the command line. A wrapper, service, explicit chdir or sudo directory policy can select that working directory. An absolute interpreter and script pathname do not make their relative data filenames absolute.

Define `relative_input` as the exact reviewed ordinary filename and `cwd` as the independently observed absolute working directory. In the trusted Ruby environment, a lexical path calculation is:

~~~bash
"$ruby_bin" -e 'puts File.expand_path(ARGV.fetch(0), ARGV.fetch(1))' "$relative_input" "$cwd"
~~~

This reports a candidate absolute pathname; it does not check existence, resolve symlinks, open the file or establish the identity/permissions of the process that consumed it. Retain those separately when relevant. A missing-file exception establishes that particular failed open, not a reason to place an arbitrary replacement input in a privileged process's working directory. Prefer correcting the approved application's explicit data-path contract.

## Select the loaded parser's actual semantics

Ruby's YAML interface normally uses Psych, but version and options matter. The Ruby2.7 documentation's Psych.load constructs Ruby objects and explicitly directs untrusted documents to safe_load. The Ruby3.1 documentation's Psych.load delegates to safe_load, allowing Symbol by default. Those documented versions are examples of changed semantics, not a universal conclusion based on an interpreter banner; match the actually loaded implementation and application options.

For an intended plain-data consumer, use its applicable safe_load contract with narrowly required permitted classes/symbols and alias policy. Do not enable object classes or unsafe loading merely to make an acquired tagged document parse. Safe loading still does not validate the application's expected mapping/types/version strings or impose every resource limit; review the schema and subsequent operations separately. A rejected class, alias or syntax is a different outcome from an empty document or a missing file.

Read exception frames in execution order. A later parser/application exception is not rollback evidence: earlier file, helper or object-construction effects may already have occurred. Report the operation and evidence supported by the source/trace, without claiming successful dependency validation or update from a printed value.

Finish with resolved-input assumptions, source locations, actual loader/version/options and any missing deployment/path evidence. Use [File.expand_path](https://docs.ruby-lang.org/en/3.1/File.html#method-c-expand_path), [older Psych.load and safe_load](https://docs.ruby-lang.org/en/2.7.0/Psych.html) and [newer Psych loader contracts](https://docs.ruby-lang.org/en/3.1/Psych.html) to resolve the selected version's behavior.
