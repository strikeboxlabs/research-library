# Test a signed-session filter oracle

Use this only for an authorized application after static inspection establishes that a client-controlled signed session object reaches a selected ORM relation filter. Require the exact cookie serialization/signing contract, a known signing key, the selected record identity, a bounded alphabet/length and a stable response marker. Read the signing implementation directly; do not import the application. A successful signature is only the transport prerequisite.

## Prove the response classes first

Build three private session values with the same selected identity: a known-positive predicate, a known-negative predicate and a malformed or impossible predicate. Send each request without redirects, with a timeout, and record status, Location, content type and the explicit success marker. A page saying no files and an ORM exception/500 are different classes. A login redirect, rate-limit response or fallback page is unknown. Do not define success as merely the absence of a negative string.

The selected identity must itself return the relation rows needed for the marker. Guessing a numeric administrator ID from convention can turn every predicate into a false response. Confirm it from acquired code/data or a positive control. The ORM translates structured filters according to its schema/provider; this is not raw SQL injection, and a selected field list does not prevent hidden fields from affecting the where clause.

## Recover one bounded prefix

The following adaptable logic assumes the caller supplies a `probe(prefix)` function returning the literal strings `match`, `miss` or `unknown`. It enforces exactly one matching character at each position and never treats an error as false. Keep checkpoints private because the recovered value can be credential material:

~~~python
def recover_prefix(probe, alphabet, length, checkpoint):
    prefix = checkpoint
    if not 0 <= len(prefix) <= length:
        raise ValueError("checkpoint exceeds selected length")
    while len(prefix) < length:
        matches = []
        for character in alphabet:
            outcome = probe(prefix + character)
            if outcome == "unknown":
                raise RuntimeError("ambiguous response; preserve evidence and stop")
            if outcome == "match":
                matches.append(character)
        if len(matches) != 1:
            raise RuntimeError(f"expected one match at offset {len(prefix)}, got {matches!r}")
        prefix += matches[0]
        checkpoint = prefix
    return prefix
~~~

Derive alphabet and length from the verified producer, schema or stored format. A 32-character lowercase hexadecimal alphabet is justified by a demonstrated raw MD5 hex producer, not by length alone. Use an exact-equality predicate for the final value and rerun both controls periodically. Stop on changed cookies, redirects, throttling, server errors, multiple/no matches or an exhausted request budget; preserve the offset and evidence rather than retrying blindly.

For a requests-based probe, create one `requests.Session`, set both the data and signature cookies exactly as observed, use a finite timeout, `allow_redirects=False`, and classify only the expected status/content marker. Cookie-domain/path mismatches can prevent transmission. Keep secrets out of URLs/logs and do not persist the final value unless the task requires it. Hash-format identification and authorized offline recovery are later, separate tasks; application credential recovery does not establish OS credential reuse.

Prisma documents `startsWith` as a string filter and relation `is` as a related-record filter. Verify the acquired generated schema/client version because current docs do not prove every historical build. See [Prisma Client filters](https://www.prisma.io/docs/orm/reference/prisma-client-reference#startswith), [Requests sessions](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) and the application's identified session-signing sources.
