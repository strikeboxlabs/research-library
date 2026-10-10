# Match a Laravel session deserialization path

Establish the deployed dependency version/classes, Redis session driver/database/prefix, selected session ID, storage serialization/encryption and the subsequent request that reads that key. A `composer.json` constraint is not an exact deployed version; use the lock/vendor/runtime evidence. An unserialize offset error is evidence of malformed data reaching a parser, not proof that a selected chain will trigger.

Inspect the installed chain's information first. For a matching authorized fixture with Laravel/RCE10's function-call parameters, define `payload_file` as a fresh private path:

~~~bash
phpggc -i Laravel/RCE10
umask 077
phpggc Laravel/RCE10 system id > "$payload_file"
~~~

The generation command creates bytes; it does not call `id` on the target. The upstream chain uses a `__toString` vector, so deserialization alone need not trigger it. Verify the actual application path exercises that object use. The broad chain catalogue version label is a lead, not proof that every later release or configured application is compatible.

For the permitted session test, place those exact bytes only in the selected disposable fixture session key using the confirmed storage format and protocol client/encoder. A Redis SET has separate command, key and value arguments; whitespace in serialized data must remain inside the value. Do not split the payload on spaces, count Unicode characters as byte lengths or use `$(cat payload)` for arbitrary serialized bytes. Shell command substitution loses trailing newlines and cannot preserve NULs. JSON/HTTP carriage adds its own encoding constraints; a valid PHP artifact does not establish delivery.

Keep the original fixture session state/TTL for the intended restoration or use a wholly disposable session. Issue the scoped application request that reads it and correlate an identity/marker result with the selected artifact. A transport 400/URL error may occur after processing; inspect observed effect before repeating a write. A working `id` result establishes the application process identity for that invocation, not a general unrestricted shell or host root. An error, no marker or an untriggered object requires checking byte delivery, class loading and vector separately. Restore/delete only the selected fixture state as agreed; do not clear a shared database. See [Laravel/RCE10 implementation](https://github.com/ambionics/phpggc/blob/master/gadgetchains/Laravel/RCE/10/chain.php) and [Redis SET semantics](https://redis.io/docs/latest/commands/set/).
