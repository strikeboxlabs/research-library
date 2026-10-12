# Install the selected gem for the intended user

Require the existing trusted Ruby/RubyGems installation, an approved exact gem name/version and repository, and authorization to install its dependencies/build hooks in this user environment. Resolve the intended Ruby first. If the application uses a reviewed Bundler lockfile, follow that bundle's installation workflow; a standalone gem install does not reproduce its dependency selection.

Define `gem_bin` as RubyGems for that Ruby, `gem_name` as the selected distribution name and `gem_version` as its approved version. Inspect the install options, active source configuration and user destination:

~~~bash
"$gem_bin" help install
"$gem_bin" sources --list
"$gem_bin" environment user_gemhome
"$gem_bin" list --local --exact "$gem_name"
~~~

Resolve unexpected sources or an incompatible Ruby/platform before installation. Do not add an unverified mirror or bypass TLS/dependency checks to repair a download/build failure. For the requested user installation:

~~~bash
"$gem_bin" install "$gem_name" --version "$gem_version" --user-install --no-document
"$gem_bin" list --local --exact "$gem_name"
~~~

`--user-install` selects the user's gem repository instead of GEM_HOME; it does not modify every Ruby installation. `--no-document` skips generated documentation, not dependency installation or native-extension builds. The version constraint pins the selected gem, while dependency versions still follow resolution unless a separate locked workflow controls them.

Keep final status and the actual installed specification/platform. A failure can leave cached/unpacked/build files, so preserve its diagnostic and inspect inventory before repeating. A registered version does not prove the application's require or native extension loads.

If the gem provides a CLI, inspect the reported executable directory and any PATH warning. Select its verified installed wrapper for a harmless version/help check; do not invent a versioned user path or immediately connect a remote client. Finish with Ruby environment, selected gem/dependencies, installation status and that local load/startup result or the remaining prerequisite. Do not remove shared dependencies merely to clean a failed attempt.

Reference: [RubyGems install, environment and source commands](https://guides.rubygems.org/command-reference/).
