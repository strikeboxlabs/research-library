---
name: node
description: Use Node.js for CommonJS resolution, selected module precedence, a bounded Socket.IO exchange, request/cookie source review, signed client-session analysis or numeric input validation. Use for dependency differences, parser and session trust boundaries and bounded application work.
---

# CommonJS lookup and application contracts

Read this entire SKILL.md before acting; reuse complete current context. Establish the trusted Node runtime and inspected launch environment, resolve from the actual requiring file, and retain the selected path or concrete error. This predicts lookup under those conditions; it does not prove the running application loaded or executed that file. When the task requires an execution/identity demonstration, read [module precedence and a controlled canary](references/module-precedence.md) fully before changing or running the selected job.

For an application using Socket.IO events, read [a selected event with an existing client](references/socketio-event.md) fully before that procedure; it requires an installed compatible socket.io-client and the observed subscription/session contract. Keep this branch unloaded for ordinary resolution.

For an acquired cookie-session/Keygrip application or owned signed-cookie reproduction, read [signed session bytes and trust](references/signed-session.md) fully before calibrating or generating a pair. It requires the identified serialization/signing contract and exact private key bytes; finish with a matching control or the concrete mismatch.

For acquired request/cookie processing code, read [parser and verification order](references/request-data-review.md) fully before source interpretation or syntax checks. It requires the actual route, middleware and dependency context; finish with the supported dataflow and unresolved implementation gaps.

For a loop or queued job controlled by request data, read [numeric input and bounded work](references/numeric-input.md) fully before evaluating or changing the handler. It requires the input format and intended bounds; finish with local validation results and any remaining concurrency or runtime uncertainty.

For CommonJS lookup, inspect the launcher and its shell/service environment first. A login-shell wrapper may set `NODE_PATH` differently from an interactive terminal. `NODE_OPTIONS`, preload flags and custom loader hooks can execute code at startup: use a trusted diagnostic environment rather than replaying an unreviewed launcher. If clearing those settings, record the difference from the real service.

Define `node_bin` as the trusted executable, `entry` as the absolute path of the file containing the relevant `require`, and `specifier` as its literal package/path argument. Do not substitute the application's top-level entry for a dependency's own requiring file. This helper uses standard CommonJS resolution without importing the selected application/package:

~~~bash
"$node_bin" --version
"$node_bin" --input-type=commonjs - "$entry" "$specifier" <<'JS'
const { createRequire } = require('node:module');
const [entry, specifier] = process.argv.slice(2);
const fromEntry = createRequire(entry);
console.log(JSON.stringify({search: fromEntry.resolve.paths(specifier)}));
try {
  console.log(JSON.stringify({resolved: fromEntry.resolve(specifier)}));
} catch (error) {
  console.error(JSON.stringify({code: error.code, message: error.message}));
  process.exitCode = 1;
}
JS
~~~

For a bare package, ordinary lookup walks `node_modules` from the requiring file's directory through its ancestors before fallback locations such as `NODE_PATH`. Changing the terminal's directory does not relocate an absolute `createRequire` base. On Linux, `NODE_PATH` is colon-separated. Relative specifiers such as `./helper` instead resolve from the requiring file; core modules such as `fs` can return a builtin identifier and `search: null`.

If two candidate copies exist, the returned filename identifies the selected copy for this probe. An **illustrative** `/srv/app/node_modules/logger/index.js` is a result to inspect, not a target-image path assumption. Check that file's package metadata and directory permissions; a writable earlier directory is a lookup risk, not evidence of code execution. Log-file ownership or periodic timestamps alone do not establish the writer's effective identity.

`MODULE_NOT_FOUND` leaves a missing dependency/path to resolve. Other errors, including package export restrictions, are not equivalent. Preserve `package.json`, symlink layout, runtime version, startup flags and environment when comparing with the service. Node normally resolves symlinks to real paths; preserve-symlink flags and loader hooks can change behavior. A copied directory tree can therefore answer a different question.

This procedure covers `require`, not ESM `import`; ESM does not use `NODE_PATH` for module lookup. Resolution inspection needs no installation or replacement module. Use the conditional canary procedure only for an intended execution test with its scope and recovery established.

References: [CommonJS resolution](https://nodejs.org/api/modules.html), [createRequire](https://nodejs.org/api/module.html#modulecreaterequirefilename), [startup flags](https://nodejs.org/api/cli.html), [ESM differences](https://nodejs.org/api/esm.html#no-node_path).
