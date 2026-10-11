# Validate numeric input before allocating work

Use this for source review or a fix to an owned handler whose request field controls iterations. Establish whether the parser supplies JSON numbers or form strings, the legitimate minimum, and a maximum based on the application's work budget. `isNaN(value)` coerces its argument; a false result does not establish a finite integer in range. `Number.isSafeInteger` checks a number without coercing strings and rejects non-integral or non-finite values.

For a JSON-number contract, this **illustrative validation** admits zero through an application-selected limit. Zero must be handled as an empty result if the application allows it:

~~~javascript
function validCount(value, limit) {
  return Number.isSafeInteger(limit) && limit >= 0 &&
    Number.isSafeInteger(value) && value >= 0 && value <= limit;
}
~~~

For form strings, validate the complete permitted decimal syntax and length before conversion, then apply the same range check. Decide explicitly whether signs, leading zeros and surrounding whitespace are valid. `parseInt` alone can accept a numeric prefix followed by unrelated text; converting an empty string with `Number` produces zero. Reject missing, array and object values rather than silently coercing them.

Validate once into a local constant and use a forward bounded loop with a local counter. An `async` function can still perform synchronous work that blocks the event loop; request concurrency, mutable shared counters, queue size and per-iteration cost need separate controls. An HTTP timeout does not necessarily cancel that work.

Evaluate the predicate locally against legitimate boundary values, one beyond each bound, fractional and non-finite values, wrong types and missing input. Do not send pathological work to a service to infer termination. Record the accepted input type/range and unresolved cost or cancellation behavior. See the [ECMAScript Number methods](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-number.issafeinteger) for coercion and integer semantics.
