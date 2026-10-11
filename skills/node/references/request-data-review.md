# Review request parsing and verification order

Use an acquired working copy and trusted Node environment. Require the selected route, middleware order and installed/locked dependency versions; an error stack's path is a lead until matched to the deployed file. Inspect missing router/model files separately rather than treating the top-level server file as the whole application.

Follow each request field through content-type parsing, representation/type checks, database access and the response. URL-encoded and JSON parsers can produce different values. A valid JSON body can still contain a wrong field type; parsing success is not semantic validation. An `extended: false` URL-encoded setting does not establish how a separate JSON route handles nested objects. A rejected request explains that attempt rather than every input representation.

Follow the caller after a validation helper returns. Express `res.json` sends a response; it does not stop JavaScript execution or automatically return from the enclosing route. A helper with no explicit return yields undefined, rather than an authentication boolean. Repeated sends can fail after headers were sent while intervening file/database operations have already been reached. Establish the actual return/throw/branch and error middleware before calling a displayed rejection an enforced boundary. See [Express response behavior](https://expressjs.com/en/4x/api/response/).

For layered byte decoding, record each intermediate representation and final consumer. Base64 to UTF-8 text to hex bytes differs from decoding Base64 directly into the signed bytes; an inner hex renderer's newline can survive the outer encoding. Node's hex decoder can return a truncated prefix at a non-hex character or dangling digit, so success alone is not full-input validation. A byte-buffer substring test operates after its actual decoding, not on the original header text. Inspect the accepted grammar and exact byte count without generating a forged token. Sequential createHash updates hash concatenated inputs; a secret-prefixed hash is distinct from createHmac. Remediation must define a standard MAC and canonical bytes consistently at generation and verification. References: [Buffer encodings](https://nodejs.org/api/buffer.html#buffers-and-character-encodings), [HMAC](https://nodejs.org/api/crypto.html#class-hmac).

For cookies, distinguish transport decoding, plain JSON parsing and a library which reconstructs executable JavaScript. Never call an acquired deserializer merely to inspect its input. Trace the actual installed package statically; its name or a source comment does not establish behavior/version. Identify operations which occur before a later signature/authorization comparison. A check after unsafe reconstruction cannot protect against effects which already occurred. A field named `sign` also does not identify an HMAC, server-held session or standard cookie-signing contract; inspect the actual algorithm, bytes and verification order without generating a forged session.

For syntax checking of the selected source only, define `node_bin` as the trusted executable and `source` as the existing working-copy JavaScript path. Use an inspected startup environment without unreviewed preload/loader hooks:

~~~bash
"$node_bin" --check "$source"
~~~

Preserve its status and syntax diagnostic. This does not import dependencies, test requests, establish application behavior or show the source matched the deployed service. Missing packages do not require installation just to read code; retain the version/implementation gap. Code execution, network markers and a changed cookie are separate tests with their own authority/evidence, not prerequisites for this review.

Finish with the selected file/dependency context, input representations, reachable consuming operations and the placement of validation/verification. Keep application identity, database records and OS process identity separate. See [Node syntax checking](https://nodejs.org/api/cli.html#-c---check) and the deployed framework/parser documentation when a behavior depends on its version.
