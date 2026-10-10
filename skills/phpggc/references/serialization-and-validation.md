# Preserve structure and test the actual trigger

PHP serialized string lengths count bytes. Protected/private property names can contain NUL bytes. JSON, URL/form encoding and base64 are transport layers, not interchangeable serialization formats. Keep the original binary artifact, then apply only the encoding the receiving application actually reverses. PHPGGC supports base64 (`-b`) and URL (`-u`) output encodings; inspect installed help when combining transformations. Avoid double encoding by a later HTTP client.

Use a disposable fixture with the matching PHP/dependency versions and a harmless marker effect. Exercise the same deserialization and subsequent method/cleanup sequence as the application, not merely a standalone `unserialize` call. Record which stage completed: input decode, class resolution, object construction, trigger invocation and marker effect. This isolates common failures:

| Result | Likely next investigation |
|---|---|
| Offset/length error | Compare exact bytes after transport with the original artifact. |
| Incomplete class or disallowed class | Check autoloading, dependency version and `allowed_classes`. |
| Object exists but no effect | Confirm the chain's trigger vector and later object use/lifetime. |
| Exception before cleanup | Check destructor timing and whether the application aborts before the expected trigger. |
| Marker works only in a standalone test | Compare application wrapping, signed/encrypted input, call path and runtime restrictions. |

`--fast-destruct` changes the object structure/timing for destructor vectors; it is not a universal fix for an incompatible class or different trigger. PHPGGC's payload-testing facilities can actually execute the selected effect. Do not mistake those for metadata inspection or run a test against a real application merely because generation is local.

PHAR output is another artifact type with its own metadata-deserialization trigger and PHP-version behavior. The existence of a file operation on `phar://` does not universally imply metadata deserialization on every supported PHP version. Establish the exact parser/call path before selecting that mode. Authentication/signatures around serialized input are additional constraints; a correct gadget chain does not bypass them automatically.

See [PHPGGC vectors, wrappers and encodings](https://github.com/ambionics/phpggc) and [PHP unserialize](https://www.php.net/manual/en/function.unserialize.php).
