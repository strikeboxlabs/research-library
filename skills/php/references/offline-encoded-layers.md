# Decode a selected literal without evaluating PHP

Start from the original acquired bytes and a known expression. A screenshot ending in an ellipsis is insufficient. Extract only the selected literal into `literal`, an absolute local data-file path; do not include PHP quotes, escapes or surrounding calls. Resolve string-literal escapes from the original syntax first, without running it. Record the file digest and exact expression separately.

For the specific nesting `gzuncompress(str_rot13(base64_decode(...)))`, work from the inner call outward: base64, ROT13, then zlib. `gzuncompress` expects the gzcompress/zlib representation; it is distinct from gzip decoding or raw gzinflate. Do not change the algorithm until a missing/truncated input is resolved.

Use the verified `php_bin` and confirm zlib is available with the selected `-n` configuration. Define `decoded` and `decode_errors` as fresh private output files. This bounded diagnostic accepts at most 256 KiB of encoded input and 1 MiB of decoded output:

~~~bash
(
  set -o noclobber
  "$php_bin" -n -r '
    $s = file_get_contents($argv[1], false, null, 0, 262145);
    if ($s === false || strlen($s) > 262144) { exit(2); }
    $b = base64_decode($s, true);
    if ($b === false || !function_exists("gzuncompress")) { exit(3); }
    $d = gzuncompress(str_rot13($b), 1048576);
    if ($d === false) { exit(4); }
    $written = fwrite(STDOUT, $d);
    if ($written === false || $written !== strlen($d)) { exit(5); }
  ' "$literal" >"$decoded" 2>"$decode_errors"
)
~~~

Check the process status and diagnostics before treating output as a complete layer. A failed run can leave an empty/partial output; preserve that fact rather than evaluating it to test validity. Strict base64 rejects non-alphabet corruption but is deliberately narrower than a source call using PHP's permissive default. Keep that difference explicit.

Inspect the decoded layer as inert bytes: follow input predicates, include targets and command/network sinks statically. Do not send it to a public decoder or invoke eval/include, unserialize or an embedded callback. Repeat only when a complete next literal and its transform order are independently established. Finish with input/output sizes, the exact layer mapping and unresolved calls; decoding is not proof the code executed or the tree is clean.

See [strict base64](https://www.php.net/manual/en/function.base64-decode.php), [ROT13](https://www.php.net/manual/en/function.str-rot13.php), [bounded zlib decoding](https://www.php.net/manual/en/function.gzuncompress.php) and [zlib versus gzip](https://www.php.net/manual/en/function.gzcompress.php).
