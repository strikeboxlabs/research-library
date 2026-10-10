---
name: bee
description: Select a Backdrop CMS installation, inspect its CLI status and run bootstrapped PHP with Bee. Use when site/root selection, PHP runtime differences or a sudo grant changes evaluation and command authority.
---

# Bee for the selected Backdrop site

Read this entire SKILL.md before acting; reuse complete current context. Select the actual Bee executable, Backdrop root and site before bootstrapping it. For PHP evaluation or a privileged Bee grant, read [evaluation and process authority](references/evaluation.md) fully before its procedure. Finish with the selected site/runtime and observed result, including child identity and artifact state when relevant; a sudo listing or successful bootstrap alone is insufficient.

Use the existing Bee CLI rather than recreating its Backdrop bootstrap. Define `bee_bin` as the selected installed invocation and `backdrop_root` as the verified installation directory, not the Bee source directory:

~~~bash
"$bee_bin" version
"$bee_bin" help status
"$bee_bin" --root="$backdrop_root" status
~~~

`--root` selects the CMS installation. Without it, Bee searches from the current directory. For multisite, add the actual `--site=site_name_or_url` value defined by that installation; it is distinct from the filesystem root and from `--base-url` used for generated links. Use a known site instead of allowing the current directory to choose one accidentally.

Status can identify the CMS/Bee versions, site/settings paths, database configuration and CLI PHP context. It bootstraps application code and can read the database; it is not a passive parser for an untrusted downloaded tree. An incomplete bootstrap/database warning limits the reported result. `status --show-password` deliberately reveals database credentials; omit it unless that value is the requested private evidence. Status does not establish the web SAPI's configuration.

For a selected task already requiring PHP evaluation, `help eval` explains the installed command and aliases. The reference retains its actual execution procedure, output/error interpretation and sudo effects. Other administration commands are available through installed help, but their effects are not implied by this package's narrow scope.

See [Bee usage](https://github.com/backdrop-contrib/bee/wiki/Usage) for root/site selection and [upstream requirements](https://github.com/backdrop-contrib/bee#requirements) when runtime/bootstrap behavior differs.
