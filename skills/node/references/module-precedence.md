# Establish the impact of a writable earlier module path

Use this for a controlled reproduction or an authorized assessment of CommonJS module substitution. Establish the actual requiring file, bare package name, process identity and launch environment using the entrypoint's non-loading resolver. A writable earlier `node_modules` ancestor can take precedence over a fallback in `NODE_PATH`; it cannot override a builtin or an earlier successful local match merely because it is writable.

For example, a script at an **illustrative** `/srv/app/jobs/check.cjs` requiring `logger` can select `/srv/app/node_modules/logger/index.js` before a global fallback. The search starts at the requiring file, not the operator's terminal. Trace package `exports`/`main`, real paths, flags and any earlier candidate before deciding which directory matters.

For an execution test, use an owned replica first or a selected target/job where module creation and the resulting job effect are authorized. Save the original state and choose an absent candidate directory; never overwrite the existing legitimate package just to demonstrate this behavior. Preserve the expected package's format and entry resolution. A minimal CommonJS canary entry can print a marker and terminate deliberately:

~~~javascript
console.error(JSON.stringify({
  probe: 'module-precedence', file: __filename,
  euid: typeof process.geteuid === 'function' ? process.geteuid() : null
}));
throw new Error('module-precedence canary reached');
~~~

This changes application behavior: it fails at module load. Use only where that controlled failure is intended; a compatible replacement for a continued job needs its actual export/event interface. A module exporting a constructor is different from a module exporting an object. A surrounding try/catch may not catch errors thrown before that try begins, including JSON.parse in a callback.

After placing the reviewed canary at the exact selected candidate entry, re-run the resolver to confirm the selected path. Execute only the intended reviewed launcher/job; define `node_bin` and `entry` for a simple direct launcher when that matches the deployment:

~~~bash
"$node_bin" "$entry"
~~~

A scheduled wrapper may set different shell/environment/identity conditions. Observe that job's own output or trusted process evidence; an operator's direct run proves only that invocation. The canary's `file` establishes the loaded entry and Unix `euid` reports effective UID for that process. Log ownership or a changing timestamp alone does not prove either. Keep marker time/job identity with the result.

CommonJS caches loaded modules by resolved filename. Changing a file need not change an already running process; a fresh authorized invocation and a cached long-lived process are different tests. Do not force an unrelated restart. Lack of a marker can mean the candidate wasn't selected, the job didn't run, a dependency failed earlier or output was captured elsewhere; use the resolution and job evidence to discriminate.

Remove only the files/directories created for this test, after confirming their exact owned paths, and restore any deliberately replaced content. Recheck resolution and the next intended job result. Report lookup risk, observed code execution/identity and restoration separately; the generic canary proves no shell or further privilege effect.

See [CommonJS lookup and caching](https://nodejs.org/api/modules.html), [package entry rules](https://nodejs.org/api/packages.html) and [effective UID](https://nodejs.org/api/process.html#processgeteuid).
