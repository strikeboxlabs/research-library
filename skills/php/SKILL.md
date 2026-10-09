---
name: php
description: Inspect PHP CLI configuration and run controlled local checks. Use when CLI versus web SAPI, PHAR metadata behavior or image-header inspection causes a misleading reproduction.
---

# PHP CLI reproduction context

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

`-d name=value` changes configuration for that invocation, subject to the directive's rules. For PHAR creation, `phar.readonly` controls whether PHP archives can be written; some changes are constrained by the startup ini. Reading an archive does not require a blanket machine-wide setting change. Keep any creation-specific override on the controlled CLI invocation and use a fresh output path.

For PHAR behavior, match the version and API actually called. PHP 8.0 stopped automatically unserializing PHAR metadata on ordinary archive loading; explicit metadata access is a different operation. A failed older demonstration therefore does not alone establish a patched application, harmless metadata or a missing gadget.

`getimagesize` can accept a non-image and return nonsensical dimensions. A `GIF89a` prefix plus reported dimensions is not proof of a valid decodable image or a pure image file. Use the intended image decoder and retain the original bytes. When wrappers or application transformations change a response, verify exact lengths and contents; do not invent missing bytes to make a parser accept it.

Documentation reviewed 2026-10-09; Linux execution untested. Case: BigBang pp. 4–8. Sources: [CLI options](https://www.php.net/manual/en/features.commandline.options.php), [PHAR configuration](https://www.php.net/manual/en/phar.configuration.php), [PHP 8 changes](https://www.php.net/manual/en/migration80.incompatible.php), [getimagesize limitations](https://www.php.net/manual/en/function.getimagesize.php).
