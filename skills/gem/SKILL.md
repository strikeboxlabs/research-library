---
name: gem
description: Inspect installed RubyGems versions or install one selected gem in the intended user environment. Use when dependency availability, installer failures or executable paths differ from the application's Ruby environment.
---

# Resolve local Ruby dependency inventory

Read this entire SKILL.md before acting. Require a trusted existing Ruby/RubyGems environment and the selected gem name; inspect local metadata before deciding whether the application's dependency requirement is met. For a requested installation, read [selected user installation](references/user-install.md) fully before changing that environment. Finish with environment, observed versions, requirement and any unresolved load/build issue.

Define `gem_bin` as the executable associated with the application's intended Ruby and `gem_name` as the exact distribution name from its reviewed dependency declaration. Confirm this installation's options:

~~~bash
"$gem_bin" --version
"$gem_bin" help list
"$gem_bin" list --local --exact "$gem_name"
~~~

`--local` selects local inventory; `--exact` avoids the ordinary regular-expression name match. An **illustrative** `httpx (1.2.5)` reports a registered installed version visible to this RubyGems environment. Empty successful output means no matching registered gem in that search context, not that every Ruby installation lacks it. A command/startup error leaves inventory unresolved.

Compare the listed version/platform with the actual Gemfile/lockfile or reviewed requirement. Multiple versions can coexist. Bundler's selected bundle, GEM_HOME/GEM_PATH and another Ruby executable can differ from this inventory; do not repair a missing require by blindly installing into the shell's default environment. A Ruby `require` name can differ from the gem distribution name.

Installation output listing dependencies and generated documentation establishes a reported installer result, not that the application loaded them or that a native extension works. Unpacked files can remain after a failed extension build without an installed specification. Inspect the original build/load diagnostic and intended interpreter before choosing a repair. The linked installation task changes the environment and can run build hooks; it is not an automatic inventory step. Starting a supplied Ruby script executes it.

See the [RubyGems list options and installation behavior](https://guides.rubygems.org/command-reference/) and [gem locations/load paths](https://guides.rubygems.org/rubygems-basics/).
