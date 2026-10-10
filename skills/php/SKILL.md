---
name: php
description: Use PHP CLI for a selected local web test, configuration checks and PostgreSQL connection diagnosis through the pgsql extension. Use for CLI/web SAPI differences, missing extensions, PHAR behavior, HTML output encoding misleading upload/image validation, Joomla template or Backdrop module process actions, or offline Laravel CBC cookie/session analysis.
---

# PHP CLI reproduction context

Read this entire SKILL.md before acting. Establish the selected binary/SAPI, then choose configuration/source inspection, PHAR/upload review, PostgreSQL diagnosis or output encoding. When psql is unavailable and the task requires PostgreSQL diagnosis, read [the PHP connection procedure](references/postgresql-connection.md) fully before its commands; it requires an existing libpq service and a reviewed local snippet. For HTML encoding or dynamic SQL construction, read [output and SQL context](references/output-and-sql-context.md) fully before its checks. For offline Laravel CBC cookie/session analysis, read [cookie decryption](references/laravel-cookie.md) fully first; it requires the actual cipher and authorized key/envelope files. For an authorized Joomla template edit/process test, read [template process boundaries](references/joomla-template-processes.md) fully first; it requires actual edit authority, original bytes and a verified trigger. For an authorized Backdrop module/archive upload and direct PHP endpoint test, read [Backdrop module execution](references/backdrop-module.md) fully first; it requires actual installation authority, the selected format and tracked artifact/trigger. For validated/coerced inputs later used in a shell command, read [validation and argument boundaries](references/validation-and-arguments.md) fully first; it covers pure CLI reproduction and an authorized nc-backed form test. For serving a selected disposable web test, read [local web server](references/local-web-server.md) fully first. Finish with the observed configuration, served response, exact transformation, verified database identity or observed template process effect/restoration; lint or a CLI result alone cannot establish web-runtime behavior.

Define `php_bin` as the intended executable, which may be a versioned binary rather than the default `php`:

~~~bash
"$php_bin" -v
"$php_bin" --ini
"$php_bin" -m
"$php_bin" -r 'echo PHP_VERSION, " ", PHP_SAPI, PHP_EOL;'
~~~

Record the binary, SAPI, loaded configuration and relevant extensions. CLI results do not establish the version/configuration used by Apache or FPM. An HTTP version header is a separate observation; testing local PHP 8.2 does not reproduce a service merely reporting 8.3.2. `-n` ignores ini files and may omit extensions, so use it only when that configuration difference is intentional.

For an existing reviewed source file, define `script` and lint it before any intended execution:

~~~bash
"$php_bin" -l "$script"
~~~

Lint checks syntax, not application behavior, runtime dependencies, reachable classes or security. Normal PHP startup/configuration still matters. To execute a small reviewed snippet, `-r` accepts PHP code without `<?php` tags; keep shell quoting intact and pass variable input as arguments rather than interpolating it into PHP source. Running a supplied script or calling `unserialize` is code execution, not merely inspection of an artifact.

When interpreting source, backticks invoke `shell_exec`, not `exec`; disabling `shell_exec` also disables the backtick operator. A blocked function explains that mechanism only, not whether the whole application is safe. `<?=` is the short echo form and is independent of `short_open_tag`; the shorter opening `<?` is configuration-dependent. Check the actual web SAPI's settings before attributing a failed reproduction to CLI settings. See [execution operators](https://www.php.net/manual/en/language.operators.execution.php) and [PHP tags](https://www.php.net/manual/en/language.basic-syntax.phptags.php).

A scheduled CLI launcher may include additional PHP files. Checking or hashing only the launcher does not establish the integrity of those dependencies. Trace `include`/`require`, configuration-driven prepend/append files, the working directory and effective include_path without executing the application. A bare `index.php` is resolved using PHP's include rules; it need not refer to the file a browser URL suggests. Check the resolved file and containing-directory permissions under the actual execution identity. `file_exists` only checks existence, and linting the launcher does not recursively validate the included code. See [PHP include semantics](https://www.php.net/manual/en/function.include.php).

`-d name=value` changes configuration for that invocation, subject to the directive's rules. For PHAR creation, `phar.readonly` controls whether PHP archives can be written; some changes are constrained by the startup ini. Reading an archive does not require a blanket machine-wide setting change. Keep any creation-specific override on the controlled CLI invocation and use a fresh output path.

For PHAR behavior, match the version and API actually called. PHP 8.0 stopped automatically unserializing PHAR metadata on ordinary archive loading; explicit metadata access is a different operation. A failed older demonstration therefore does not alone establish a patched application, harmless metadata or a missing gadget.

`getimagesize` can accept a non-image and return nonsensical dimensions. A `GIF89a` prefix plus reported dimensions is not proof of a valid decodable image or a pure image file. Use the intended image decoder and retain the original bytes. When wrappers or application transformations change a response, verify exact lengths and contents; do not invent missing bytes to make a parser accept it.


For upload-handler review, trace the original filename, client-supplied `$_FILES['file']['type']`, error status, content check and final destination as separate values. The MIME field is not PHP verification of the bytes. `move_uploaded_file` checks that its source came through PHP's HTTP POST upload mechanism; success does not establish a valid image. Ordinary CLI files do not become HTTP uploads merely by assigning `$_FILES`, so a failed CLI move is not a reproduction of the web handler.

Follow the exact variables used to build the stored name: `$extension` and `$ext` are different variables, and an omitted assignment leaves that step unresolved. A double extension alone does not explain the final filename or server execution. Check the complete handler and effective web-server mapping. An unconditional client message such as `Uploaded!` proves neither a successful move nor that a later URL addresses the uploaded file. See PHP's [upload fields](https://www.php.net/manual/en/features.file-upload.post-method.php) and [move semantics](https://www.php.net/manual/en/function.move-uploaded-file.php).
