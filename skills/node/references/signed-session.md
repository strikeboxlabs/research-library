# Reproduce a signed client-side session

Use this for an acquired cookie-session application whose serialization, key and signing implementation have been identified, or an owned reproduction of that contract. Read the selected source without importing it. Require a trusted Node runtime, private key bytes and a captured known-valid cookie pair before treating a generated pair as compatible. No cookie-session or application import is required for this built-in crypto helper.

## Identify the exact signed bytes

cookie-session stores session JSON on the client; signing protects integrity, not secrecy or automatic replay prevention. Its name can be configured. A Base64-encoded JSON object with a separate .sig cookie is not automatically a JWT. Decoding one Base64 field can expose a user object without exposing a JWT header or signature segment.

In the reviewed cookie-session 2.0.0 / Cookies / default Keygrip contract, the value is ordinary Base64 of UTF-8 JSON; Cookies signs the literal `name=value` string. The signature is HMAC-SHA1 encoded as Base64 with + mapped to -, / mapped to _ and padding removed. The data value retains its own Base64 alphabet/padding. Sign the encoded value, not decoded JSON, the cookie attributes or the value with its name omitted. Re-serializing a captured object can change property order, spaces or Unicode representation, so calibrate against the exact captured value first.

Custom Keygrip instances can select another algorithm/encoding. Multiple configured keys sign with the first and verify with the key list; a captured old signature can match a rotated verification key. A mismatch does not establish that every key is invalid or that the application accepts unsigned sessions. Semver ranges in package.json establish declared requirements, not the actual installed dependency versions.

## Calibrate, then generate the selected pair

Define `key_file` as private exact key bytes (no automatically appended newline), `cookie_name` as the observed name, `value_file` as the exact captured encoded value in a one-line UTF-8 file, and `signature_file` as its captured signature in the same format. `node_bin` is the trusted Node executable. This offline probe reports only compatibility:

~~~bash
"$node_bin" --input-type=commonjs - "$key_file" "$cookie_name" "$value_file" "$signature_file" <<'JS'
const fs = require('node:fs');
const crypto = require('node:crypto');
const [keyFile, name, valueFile, signatureFile] = process.argv.slice(2);
const oneLine = path => {
  const value = fs.readFileSync(path, 'utf8').replace(/\r?\n$/, '');
  if (/[\r\n;]/.test(value)) throw new Error('Not a single cookie field');
  return value;
};
if (!/^[A-Za-z0-9_-]+$/.test(name)) throw new Error('Unexpected cookie name');
const value = oneLine(valueFile);
const sig = crypto.createHmac('sha1', fs.readFileSync(keyFile))
  .update(name + '=' + value, 'utf8').digest('base64')
  .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
if (signatureFile) {
  const captured = Buffer.from(oneLine(signatureFile), 'ascii');
  const generated = Buffer.from(sig, 'ascii');
  console.log(JSON.stringify({matchesCaptured: captured.length === generated.length
    && crypto.timingSafeEqual(captured, generated)}));
} else {
  console.log(name + '=' + value + '; ' + name + '.sig=' + sig);
}
JS
~~~

After a matching control, prepare the intended JSON in a private file. Serialize that selected object with JSON.stringify and encode its UTF-8 bytes with Buffer.toString('base64'), retaining padding. Run the same helper with that new value_file and omit signature_file to produce the selected Cookie header value; redirect it to a fresh private file rather than routine logs. Do not hand-edit a value without recomputing its signature. A correctly signed object still must satisfy the application's expected schema, lifetime and authorization checks.

If the application uses the entire user object as a database relation filter, signing authority can become filter authority: id plus a password startsWith predicate may affect which related rows appear even if the selected output columns exclude password. This is an ORM input/trust boundary; a raw SQL API elsewhere with a fixed literal query is not evidence of raw SQL injection at this route. Establish the actual handler, selected identity, positive/negative response controls and allowed fields before a request. Cookie acceptance, data-predicate inference and OS credential reuse are separate outcomes.

References: [cookie-session contract](https://expressjs.com/en/resources/middleware/cookie-session.html), [2.0.0 serialization](https://github.com/expressjs/cookie-session/blob/v2.0.0/index.js), [Cookies signature input](https://github.com/pillarjs/cookies/blob/0.8.0/index.js), [Keygrip algorithm/encoding](https://github.com/crypto-utils/keygrip/blob/master/index.js), [Node HMAC](https://nodejs.org/api/crypto.html#cryptocreatehmacalgorithm-key-options).
