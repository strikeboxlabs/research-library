# Virtual hosts and request markers

For `vhost`, `base_url` selects the network endpoint and `domain` forms candidate Host names. Supply label candidates in `wordlist`; inspect a small run before assuming the file's entries are appended as intended. Obtain a stable body marker from a nonexistent Host, then define `miss_marker` to that observed marker:

~~~bash
rustbuster vhost -u "$base_url" -d "$domain" -w "$wordlist" \
  -x "$miss_marker" -t 5 -o "$results"
~~~

The ignored string can also appear on real pages. Confirm a candidate outside the filtered scan and compare status, redirect destination and content with the control. HTTPS SNI follows the TLS connection's name; changing the HTTP Host header alone does not necessarily reach the intended TLS virtual host. Use the correct endpoint/certificate setup before interpreting uniform failures.

For a custom GET parameter, set `fuzz_url` to the full authorized URL containing literal `FUZZ` in the chosen value:

~~~bash
rustbuster fuzz -u "$fuzz_url" -w "$wordlist" -t 5 -o "$results"
~~~

Choose one variable at a time. `-X` selects the method, `-H` adds headers and `-b` supplies the body in modes supporting them. Shell quoting, URL encoding and JSON escaping are different layers: arbitrary wordlist text is not automatically a valid JSON string. Check a candidate's resulting request before broadening the list.

The upstream CLI also exposes `--csrf-url` and `--csrf-regex` for token extraction and a `CSRFCSRF` marker. These do not by themselves establish that cookies, per-request token rotation or authenticated sessions match the application. If token extraction yields no match or the server returns an expiry response, repair the request state before treating failures as absent content. Consult that installed build's behavior for multiple wordlists/markers; do not assume another fuzzer's pitchfork or Cartesian semantics.

Use [the mode examples and options](https://github.com/phra/rustbuster#fuzz-usage) to resolve implementation differences.
