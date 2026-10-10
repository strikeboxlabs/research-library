# Reproduce encoding at the actual output context

Trace the submitted field through storage to the exact template expression. A filename used in `src` and a display name used in `alt` are different flows. Encoding on an admin listing does not establish encoding on a separate detail page; an input blacklist does not replace encoding at the output context.

For a harmless local check, define `php_bin` as the selected PHP CLI and `text` as the sample string to encode. Pass it as data to the selected PHP CLI:

~~~bash
"$php_bin" -r 'echo htmlspecialchars($argv[1], ENT_QUOTES | ENT_SUBSTITUTE, "UTF-8"), PHP_EOL;' -- "$text"
~~~

**Illustrative:** `A"B&C` becomes `A&quot;B&amp;C`. This checks encoding for ordinary HTML text or a quoted attribute using that character set, not JavaScript, a URL scheme or browser execution. Make flags explicit: PHP 8.1 changed the default from ENT_COMPAT to ENT_QUOTES plus ENT_SUBSTITUTE. Invalid UTF-8 replacement is a transformation, not byte-preserving evidence. Consult [htmlspecialchars](https://www.php.net/manual/en/function.htmlspecialchars.php) when versions or output differ.

For adjacent SQL review, follow each value to its own execution call. A bound DELETE does not protect an earlier INSERT built by concatenation. Conversely, merely calling `prepare()` does not protect text already interpolated into the SQL; placeholders must carry the data. Inspect the actual driver, API and reachable statement before inferring stacked statements or filesystem writes. These static findings do not require running the web application from the CLI.

In a dynamic UPDATE builder, review array keys separately from values. `PDO::quote($value)` quotes a string literal; it does not protect `$key` concatenated as a column or assignment fragment. An allowlist must restrict fields to those the caller may change, even when their names are valid SQL identifiers. Bind values after choosing fixed, permitted identifiers: [PDO placeholders](https://www.php.net/manual/en/pdo.prepare.php) cannot stand for a column name or arbitrary SQL syntax. A parameterized WHERE clause does not protect an already interpolated SET clause.
