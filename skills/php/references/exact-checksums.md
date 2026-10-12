# Reproduce a selected legacy checksum transformation

Use for an offline comparison of a reviewed application's checksum expression and known public input. Establish the exact sanitized values, concatenation order, separators, encoding and output representation. Require the intended trusted CLI binary; this test does not execute the web application or demonstrate its filesystem permissions.

Define `first`, `last` and `email` as the already selected input strings. This evaluates only their concatenation and checksum:

~~~bash
"$php_bin" -r 'echo md5($argv[1].$argv[2].$argv[3]), PHP_EOL;' -- "$first" "$last" "$email"
~~~

Check status and compare only the 32-character hexadecimal digest. The final printed newline is not part of the string being hashed. PHP md5(..., true) instead returns 16 raw bytes; hex text and raw digest are different comparison stages. For GNU md5sum comparison, hash the same input bytes, for example `printf '%s%s%s' "$first" "$last" "$email" | md5sum --binary`; the output's filename/mode fields are not digest bytes.

Repeated identical bytes give the same result, rather than a fresh random directory name. Concatenation without separators also loses field boundaries: different field triples can produce the same concatenated input without requiring a cryptographic collision. Verify the application's transformations before assuming raw form fields match. FILTER_SANITIZE_STRING is deprecated since PHP8.1 and transforms strings; it does not establish general input validation or filename/path containment.

Read quote semantics before naming the input: in `md5('$file_hash' . time())`, the single-quoted first operand is the literal text `$file_hash`, not the value of that variable. Assigning a preceding `uniqid()` result therefore does not put that value into this expression. The time component still changes its selected input; a digest-shaped name is not evidence of unpredictable input. Record the actual expression and branch without guessing live upload names or probing their existence. A `getimagesize` check guarded by a submitted field also applies only when that field is present; inspect the actual request producer before claiming every upload took that branch. An extension check is separate from image decoding and successful storage.

For a trusted interactive diagnostic, `"$php_bin" -a` requires readline support for the actual interactive shell. Complete each selected PHP expression with its terminator and do not add PHP opening tags at the shell prompt. On PHP8.1+, absence of readline makes -a fail; older interactive mode consumed a whole script via stdin instead. Interactive history can retain entered code/input, so keep private values out of a reusable diagnostic session. The one-shot argv procedure above avoids an interactive history dependency.

A matching checksum establishes the selected transformation only. For upload-handler review, inspect the actual move result and destination separately. mkdir permissions are ignored on Windows, while Linux's mode is filtered by umask; ownership, effective ACLs and any links/reparse points require their platform's own evidence. A checksum-named path or an upload-success alert does not prove that the intended bytes were stored or served.

See [PHP MD5 representation](https://www.php.net/manual/en/function.md5.php), [interactive shell](https://www.php.net/manual/en/features.commandline.interactive.php), [sanitization filters](https://www.php.net/manual/en/filter.constants.sanitization.php) and [mkdir platform semantics](https://www.php.net/manual/en/function.mkdir.php).
