# Query a selected registry without installing packages

Require the intended registry URL, approved metadata scope, installed npm version and known authentication context. Loopback refers to this process's network namespace; an observed registry on a remote host is not the workstation's localhost. Inspect selected project/user/global configuration and registry-scoped authentication privately before sending requests. Do not print complete npmrc files into routine logs.

Define `registry` as the approved URL, `term` as one narrow search term and `report` as a fresh private JSON path. After checking local `npm help search`:

~~~bash
umask 077
npm search --json --searchlimit=10 --registry="$registry" -- "$term" > "$report"
status=$?
~~~

Keep status/diagnostics, actual registry and returned name/version/description/maintainer associations. This queries registry metadata rather than local installed dependencies. Search is limited and can be filtered, cached or unsupported by the registry; legacy search may ignore searchlimit. Empty results do not prove global package absence. A matching description is a candidate, not proof of application use, trusted authorship or installed code. Resolve the actual project manifest/lock/tree separately. See [search options](https://docs.npmjs.com/cli/v11/commands/npm-search/).

Do not install a package merely to inspect search results. Installation can modify the project and execute lifecycle code; requiring its main module executes that module too. For a legitimate installation use the entrypoint's build reference and exact reviewed identity. A bare version/name query or successful install does not validate a secret-like value found in package source.

# Diagnose an owned private-registry login

`Web login not supported` concerns the registry/client authentication strategy, not necessarily a wrong password. Verify the installed client's supported auth modes and the registry's configuration. Newer clients can default to web authentication while retaining legacy prompts; do not infer that all Verdaccio versions require the same strategy or that web login always means OAuth.

For a permitted existing account on a registry supporting legacy authentication, define `auth_config` as a fresh absolute file in a private owned directory; this login will save credentials there. Keep intended existing project configuration separate. Use the intended registry URL, trusted transport and prompt:

~~~bash
umask 077
npm login --registry="$registry" --userconfig="$auth_config" --auth-type=legacy
status=$?
npm whoami --registry="$registry" --userconfig="$auth_config"
~~~

Inspect the login result before the identity query. `login` authenticates an existing account; `adduser` can create one and is a separate requested change. Saved registry credentials are sensitive and may enable publishing; an identity response alone does not prove package read/write permission. Retain only the account/registry outcome, secure or remove the temporary credentials under the task's lifecycle policy, and never copy tokens between unrelated hosts. See [login](https://docs.npmjs.com/cli/v11/commands/npm-login/).

Effective registry selection can involve command-line arguments, environment, project/user/global/built-in npmrc and scope-specific registries. `$HOME/.npmrc` is only one input, and `userconfig` can override that location. An elevated job need not use the caller's HOME; inspect its actual environment and configuration instead of assuming a distribution's historical sudo behavior. Acquired registry configuration is not permission to redirect a privileged installer. Preserve original settings and registry-scoped authentication; see [npmrc precedence and credential scope](https://docs.npmjs.com/cli/v11/configuring-npm/npmrc/).
