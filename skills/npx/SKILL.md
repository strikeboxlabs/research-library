---
name: npx
description: Run a selected trusted npm package generator at an exact version in an owned workspace. Use when local versus fetched packages, argument placement or moving scaffolder versions affect the created project.
---

# Run the selected generator

Read this entire SKILL.md before acting. Require a trusted exact package/version, reviewed generator arguments and an owned output location with permission for its effects. All instructions are inline. Finish with the resolved package, status and actual generated project; generator success alone does not establish a later build.

Check `node --version`, `npm --version` and `npx --version`. This task targets npx shipped with npm 7 or later. Define `parent` as the selected owned directory, `package_spec` as the exact approved package/version and `generator_args` as a Bash array of its reviewed arguments, including the intended fresh project name where required:

~~~bash
cd -- "$parent" || exit
npx -- "$package_spec" "${generator_args[@]}"
status=$?
~~~

Missing packages may be fetched into npm's cache after an installation prompt. Review the resolved package before accepting; retaining the prompt is not a security sandbox. Existing exact local dependencies can satisfy the request. An unversioned name or `latest` can select a different generator later.

Arguments after the package go to the generator; npx options belong before it. An ambiguous package executable requires its documented explicit package/binary selection. Preserve errors and inspect the actual output before retrying into the same directory. Record generator version/options separately from the dependencies it created: changing dependencies afterwards does not retroactively change the scaffold's design.

Reference: [npx manual](https://docs.npmjs.com/cli/v11/commands/npx/).
