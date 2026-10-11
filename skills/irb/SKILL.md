---
name: irb
description: Evaluate reviewed local Ruby expressions in IRB and inspect their actual return values. Use to verify a validator's string boundaries without loading an application or confusing a zero match offset with failure.
---

# Check a reviewed Ruby expression locally

Read this entire SKILL.md before acting. Require a trusted installed IRB/Ruby environment and small reviewed nonsecret expressions; retain exact inputs and returned values. No conditional resources are required. This is local expression evaluation, not an application-console or remote-injection task.

From a trusted working directory, inspect `irb --version` and `irb --help`, then start without the IRB configuration file:

~~~bash
irb -f
~~~

`-f` suppresses IRB's configuration initialization, not Ruby's entire startup/environment or arbitrary code execution. Do not supply an acquired initialization script, `require` an unreviewed library or launch a Rails console just to inspect a literal expression. IRB executes entered Ruby code with the current process's authority.

For an owned validator intended to accept only a complete ASCII-letter string, enter these reviewed expressions at the prompt:

~~~ruby
/\A[a-zA-Z]+\z/.match?("Alpha")
/\A[a-zA-Z]+\z/.match?("Alpha\n")
exit
~~~

The **illustrative expected** return values are `true` then `false`; record the actual observations on this runtime. `\A` and `\z` bound the complete string. Ruby's `^` and `$` instead bound a line; `\Z` allows a final newline. Choose the boundary and alphabet the actual validator requires, including deliberate Unicode/encoding rules.

`=~` returns a match offset or `nil`; an offset of zero is truthy in Ruby, not a failed boolean test. `match?` returns a boolean and needs a supporting Ruby version. A displayed exception leaves the test incomplete; keep the exact input and diagnose syntax/encoding/version rather than silently changing it. IRB can truncate a long displayed value, so a console excerpt need not be complete data.

Finish with the expression, runtime, expected versus observed values and exit from the owned session. A local result establishes Ruby semantics for that input; it does not identify a deployed application's regex, validation order, template engine or execution outcome.

References: [IRB startup and options](https://ruby.github.io/irb/), [IRB help](https://raw.githubusercontent.com/ruby/irb/master/lib/irb/lc/help-message), [Ruby regexp anchors and returns](https://docs.ruby-lang.org/en/master/Regexp.html).
