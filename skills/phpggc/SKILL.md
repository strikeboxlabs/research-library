---
name: phpggc
description: Select and generate PHP serialization gadget chains with PHPGGC for an authorized test. Use to match dependency versions and trigger vectors, preserve serialized bytes and diagnose why a generated object is not exercised by an application.
---

# Match a chain to the application

Read this entire file before acting. Read [serialization and validation](references/serialization-and-validation.md) before transporting or testing a generated chain. For a Laravel gadget carried in a selected Redis session, also read [session delivery and trigger](references/redis-session.md) fully first. Finish with the selected chain, compatibility evidence, exact artifact and observed test result; generating an object is not proof that a target is vulnerable.

Use the installed `phpggc` entrypoint or its verified PHP/script invocation. Find chains matching the actual dependency, then inspect the selected chain:

~~~bash
phpggc -l
phpggc -i Monolog/RCE1
~~~

The chain's library/version range, effect and trigger vector are separate prerequisites. Resolve the deployed dependency version and available classes/autoloader, the deserialization entrypoint, allowed classes and subsequent object use. An application framework label is not enough. `__destruct`, `__toString` and other vectors trigger at different times; an object that deserializes successfully may never reach the required method.

For an authorized fixture compatible with the example chain, define `payload_file` as a fresh private path. The following generates serialized data for a harmless marker command; it does not test the application:

~~~bash
umask 077
phpggc Monolog/RCE1 system 'printf PHPGGC_FIXTURE' > "$payload_file"
~~~

Choose parameter syntax from `-i` for the actual chain. Command, PHP-code and function-call chains take different arguments. A generated file may contain NUL bytes; keep it as bytes. Do not put it through shell command substitution or manually replace a class/string name without recalculating serialization lengths.

When the application expects an array/container around the object, PHPGGC's `--wrapper` can supply that structure. It runs the supplied PHP wrapper during generation, so use a reviewed local wrapper and the documented hooks. Wrapping is different from transport encoding and from choosing a new gadget chain.

Use [the upstream guide](https://github.com/ambionics/phpggc) and the installed chain information to resolve version/vector differences.
