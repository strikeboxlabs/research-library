---
name: wrapwrap
description: Generate PHP filter chains that wrap resource contents with a prefix and suffix. Use for authorized parser fixtures where an existing wrapper generator can satisfy a JSON/XML envelope without hand-building filter chains.
---

# Generate the wrapper for the consuming parser

Read this entire file before acting. Read [byte and parser validation](references/byte-and-parser-validation.md) before using the resulting chain. Finish with the generated chain and the consumer's observed decoded/parser result; chain generation is not resource retrieval.

Use the verified installed invocation, represented here by `wrapwrap.py`. Its positional inputs are resource, prefix, suffix and requested size. The resource is interpreted where PHP consumes the chain, which can differ from the machine generating it.

For a controlled fixture containing short printable marker text, define `resource` as the marker's path in that PHP environment. Run in a fresh work directory because the reviewed tool writes `chain.txt`:

~~~bash
wrapwrap.py "$resource" '<root><name>' '</name></root>' 128
~~~

The shell quotes preserve the delimiters as arguments. This example aims to give an XML parser a `root/name` element containing resource data. Select prefix/suffix based on the actual consumer, not just whether an XML or JSON parser is mentioned in a writeup. Generation chooses filter operations; it does not prove the required PHP/iconv filters exist in the consumer.

The requested size can be rounded by the implementation, and generated chains can be very large. Inspect the reported size and resulting `chain.txt`, then account for request-line/body limits, proxy limits and PHP memory usage. Do not interpret a shorter-than-requested result as necessarily the full source resource. A generated URL that fits a local file may still exceed the application's transport limits.

For a JSON consumer, a prefix such as `{"message":"` and suffix `"}` supplies an envelope only if the inserted bytes are valid in that position. It is not a general JSON escaping operation. Read the reference before interpreting encoded newlines, quotes or binary data.

See [upstream usage](https://github.com/ambionics/wrapwrap) and the authors' [filter-chain explanation](https://www.ambionics.io/blog/wrapwrap-php-filters-suffix).
