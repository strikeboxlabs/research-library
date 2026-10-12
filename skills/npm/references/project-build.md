# Install dependencies, build and start the owned project

Require an existing owned project, reviewed manifest/scripts, trusted registry/package identities and permission for installation and build effects. Check Node/npm versions and project compatibility.

For an existing reviewed manifest and compatible lockfile, `npm ci` installs the whole locked project, removes its existing node_modules and refuses manifest/lock disagreement without rewriting the lock. Preserve required tree-shaping configuration. Use `npm install` without a package argument only when resolving the existing manifest and its possible lock changes is intended; inspect those changes. Frontend and server directories can be separate package roots with separate installations. See [clean install](https://docs.npmjs.com/cli/v11/commands/npm-ci/).

For a selected dependency addition, define `project` as its absolute directory and `package_spec` as one exact approved `name@version` or `@scope/name@version`, rather than a moving tag:

~~~bash
node --version
npm --version
cd -- "$project" || exit
npm install --save-exact -- "$package_spec"
status=$?
~~~

Preserve diagnostics and inspect status before building. Installation changes dependencies and potentially package.json/package-lock.json; review those changes. `--save-exact` records an exact direct dependency, but does not establish equality of the entire transitive tree with another installation. Retain the resulting lockfile. Installation can run package lifecycle code; reducing scripts changes the installed result and is not proof of a successful normal build. A peer/engine conflict calls for reviewing the selected versions, not blindly forcing installation.

For the selected project's actual reviewed `build` script, including any prebuild/postbuild hooks:

~~~bash
npm run build
status=$?
~~~

Scripts execute from the package root and use its local binary PATH. `build` is a manifest-defined command, not an npm guarantee of a particular output folder. Missing script, dependency failure and compilation failure are distinct. Inspect status, complete diagnostics and the intended fresh artifact; an old output directory can survive failure. A successful build proves this project built in this environment, not that a scaffold reproduces another application's routes, source or deployment. Record generator options, direct/transitive versions and relevant configuration when comparison matters.

For the reviewed server root, `npm start` executes its start lifecycle; without a start script npm's fallback is node server.js, not the manifest's main entry. A long-running server needs its actual readiness evidence and deliberate shutdown. A worker banner followed by getaddrinfo ENOTFOUND identifies a name-resolution failure, not an absent Redis service. Keep runtime network context and dependency names explicit. Browser connection failure may instead come from a bundled URL: change the intended source configuration and rebuild before testing the served frontend. See [start](https://docs.npmjs.com/cli/v11/commands/npm-start/).

Primary references: [npm install](https://docs.npmjs.com/cli/v11/commands/npm-install/), [npm run](https://docs.npmjs.com/cli/v11/commands/npm-run/).
