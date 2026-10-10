# Validate the wrapper and consumer separately

Use a local authorized marker resource before applying the chain to a consequential resource. Keep the marker's original bytes and inspect the exact output of the matching PHP filter pipeline before passing it through the application's parser. This separates missing filters from malformed JSON/XML and from the application's field selection.

For an already generated chain in `chain_file` and an output path `wrapped_file`, this optional fixture evaluates it in the local PHP runtime. It reads the resource named by the chain; review that resource and the chain first:

~~~bash
php -r '$chain=rtrim(file_get_contents($argv[1]), "\r\n"); $out=file_get_contents($chain); if ($out===false) {exit(1);} if (file_put_contents($argv[2],$out)===false) {exit(2);}' \
  "$chain_file" "$wrapped_file"
~~~

Do not execute this fixture when the chain names an unapproved resource. Retain warnings as well as the exit status. Then test the actual XML/JSON parse and field access with the same PHP/library behavior as the application. A successful stream read can still produce an invalid document, and a successful parse can still select the wrong field.

The upstream examples show transformed line breaks such as `=0A`; a displayed result is not automatically a byte-for-byte copy of the resource. Compare a known marker containing newline/quote/non-ASCII cases to determine the transformation relevant to the task. Do not decode arbitrary `=XX` text blindly when it could be literal input. For binary recovery, establish a reversible encoding in the source/consumer path and compare exact bytes; an XML text display alone is insufficient.

When size increases stop producing output, distinguish truncation by the requested bound, request size rejection, missing iconv conversions, PHP memory limits and parser rejection. Increase one bound only when that observation justifies it. The generator's success message proves a chain was written, not that a remote environment has compatible filters or permissions.

Preserve the generator input, chain and fixture result together. Do not substitute a historical writeup's byte count or prefix for the actual consumer contract. See [the authors' technical explanation](https://www.ambionics.io/blog/wrapwrap-php-filters-suffix) and [PHP filter wrapper](https://www.php.net/manual/en/wrappers.php.php).
