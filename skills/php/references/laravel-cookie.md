# Decrypt a selected Laravel CBC cookie without executing its contents

Establish the actual cipher, known authorized APP_KEY bytes, cookie name/encoding and framework/runtime configuration. This procedure is limited to an AES-256-CBC envelope with a base64-prefixed 32-byte key. GCM/tag handling and older/different cookie middleware need their own matching implementation. URL-decode a captured cookie value once when the actual transport encoded it; JSON/base64 layers are separate. Do not paste secrets into command arguments or logs.

Use a reviewed local PHP snippet, `php_bin` from SKILL.md, an existing private `key_file` containing the exact `base64:...` APP_KEY and `cookie_file` containing the exact transport-decoded cookie, without added line endings. Define `plaintext` as a fresh private output path. This reads data files, authenticates the CBC envelope and writes raw plaintext; it never calls `unserialize` or boots the application:

~~~bash
umask 077
"$php_bin" -r '
function bad($message) { fwrite(STDERR, $message."\n"); exit(1); }
if ($argc !== 3) bad("expected key and cookie files");
$keyText = file_get_contents($argv[1]);
$cookieText = file_get_contents($argv[2]);
if ($keyText === false || $cookieText === false) bad("input read failed");
if (strncmp($keyText, "base64:", 7) !== 0) bad("unsupported key encoding");
$key = base64_decode(substr($keyText, 7), true);
if ($key === false || strlen($key) !== 32) bad("invalid AES-256 key");
$json = base64_decode($cookieText, true);
if ($json === false) bad("invalid envelope encoding");
$p = json_decode($json, true);
if (!is_array($p)) bad("invalid envelope JSON");
foreach (["iv", "value", "mac"] as $f) {
    if (!isset($p[$f]) || !is_string($p[$f])) bad("missing envelope field");
}
if (isset($p["tag"]) && $p["tag"] !== "") bad("unsupported CBC tag");
$iv = base64_decode($p["iv"], true);
if ($iv === false || strlen($iv) !== 16) bad("invalid IV");
$mac = hash_hmac("sha256", $p["iv"].$p["value"], $key);
if (!hash_equals($mac, $p["mac"])) bad("MAC mismatch");
$plain = openssl_decrypt($p["value"], "aes-256-cbc", $key, 0, $iv);
if ($plain === false) bad("decryption failed");
fwrite(STDOUT, $plain);
' "$key_file" "$cookie_file" > "$plaintext"
~~~

Check PHP status before inspecting the output; a failure can leave an empty/partial destination and is not a decoded cookie. PHP's `openssl_decrypt` with options zero expects base64 ciphertext; do not decode `value` again without changing the option. Key bytes are used directly, not derived from a password. Keep plaintext as bytes and inspect it without evaluating/deserializing it.

Laravel 9 cookie middleware can prefix plaintext with a name-bound HMAC and `|`; that prefix is not the Redis session key. Verify the actual CookieValuePrefix/middleware and serialization setting before isolating an identifier. An authenticated envelope proves compatibility with that supplied key/cipher, not current account identity or session state. To map a session, trace the configured driver, database, key prefix and ID; server-side session storage can differ from cookie storage. A raw CBC decrypt that ignores the envelope MAC is weaker evidence and may accept tampered data. See [Laravel encryption](https://github.com/laravel/framework/blob/9.x/src/Illuminate/Encryption/Encrypter.php), [cookie prefix](https://github.com/laravel/framework/blob/9.x/src/Illuminate/Cookie/CookieValuePrefix.php) and [OpenSSL decryption](https://www.php.net/manual/en/function.openssl-decrypt.php).
