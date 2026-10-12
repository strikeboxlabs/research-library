# Install one approved global CLI

Require trusted Node/npm, the intended existing global prefix, trusted registry/package identity, a reviewed exact version and permission for installation/lifecycle effects. Define `package_spec` as that exact name@version and `package_name` as its unversioned name:

~~~bash
node --version
npm --version
npm prefix --global
npm ls --global --depth=0 -- "$package_name"
npm install --global -- "$package_spec"
status=$?
npm ls --global --depth=0 -- "$package_name"
~~~

Inspect engine requirements, existing package state and prefix permissions before installation. Global mode changes this prefix's package tree and CLI links; it can run lifecycle code. Do not add sudo or change the prefix as a silent repair for denied access. A historical unscoped package name does not establish equivalence to a newer scoped replacement.

Require successful transaction diagnostics and the intended installed version, then resolve the requested CLI and verify its own help/version against that installation. Package installation alone does not prove its command is on PATH, that an old wrapper was replaced or that the CLI's intended task works. Preserve missing-link, engine and lifecycle failures separately. This is not project dependency installation and does not establish a project lockfile.

See [npm global installation](https://docs.npmjs.com/cli/v11/commands/npm-install/).
