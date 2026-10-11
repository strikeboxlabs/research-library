---
name: create-next-app
description: Scaffold one owned Next.js project with a selected create-next-app version and deliberate router/language/package-manager choices. Use when a moving generator or reused preferences can produce a different structure than intended.
---

# Create the selected Next.js scaffold

Read this entire SKILL.md before acting. Require an owned parent, fresh project name, trusted exact generator version and permission for package downloads and generated files. All instructions are inline. Finish with generator version/options, status and actual project structure; scaffolding does not establish build or deployment success.

Define `parent` as the owned absolute directory, `generator_version` as the approved exact version and `project_name` as the intended fresh single directory name. Confirm Node/npm compatibility and the selected generator's own documented options before running:

~~~bash
cd -- "$parent" || exit
npx -- "create-next-app@$generator_version" "$project_name"
status=$?
~~~

Review npx's resolved-package prompt and answer the generator's configuration prompts deliberately. Record language, App versus Pages Router, source-directory placement and package manager; prompt sets/defaults vary by version. Reused preferences or automatic yes can silently select a different scaffold.

Inspect status, generated manifest, lockfile and source tree before acceptance. The generator can install dependencies and initialize Git; inspect partial files after failure instead of overwriting a conflicting project. A latest scaffolder followed by older dependencies is not a verified reconstruction of an older application. Changing dependencies does not supply its missing routes/configuration. Build the reviewed generated project separately when the task requires that artifact.

Reference: [create-next-app CLI](https://nextjs.org/docs/app/api-reference/cli/create-next-app); use the selected version's options rather than importing every current option into an older generator.
