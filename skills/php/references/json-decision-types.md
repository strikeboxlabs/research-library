# Boolean decisions and JSON envelopes

For an acquired handler, trace the predicate's return type, its caller's condition and the final response serialization without executing the application. A PHP Boolean false, a JSON field containing false and a PHP string containing a JSON document are different values.

`json_encode(['message' => false])` normally returns a non-empty string. Testing that string as a Boolean yields true even though its JSON field is false. PHP treats the empty string and the string `"0"` as false; a string containing `false` or a JSON object is truthy. Conversely, a false return from json_encode indicates an encoding failure, not a successful negative decision.

With a trusted selected `php_bin`, this pure local diagnostic requires JSON support and intentionally ignores ini files:

~~~bash
"$php_bin" -n -r '$decision=false; $envelope=json_encode(["message"=>$decision]); var_dump($decision, $envelope, (bool)$envelope);'
~~~

Illustrative interpretation: Boolean false, a string containing `{"message":false}`, then Boolean true. Retain the actual interpreter, output and status; this does not reproduce the deployed web handler, database or session.

Keep internal predicates Boolean and let the response/controller boundary serialize their result. Require the intended positive decision explicitly rather than treating any returned envelope as authorization. Do not blindly decode arbitrary strings to repair a caller: establish the function's contract, failure handling and all callers first. Input type validation remains separate; JSON number 1 and Boolean true are not interchangeable under strict comparison.

Follow control flow beyond a negative decision. `header(...)` does not stop execution; `return header(...)` returns from that function, while the calling router may continue. A subsequent unreachable exit statement supplies no additional protection. Finish with the typed predicate/caller/response map and any missing code or deployment facts. See [Boolean conversion](https://www.php.net/manual/en/language.types.boolean.php) and [JSON encoding results](https://www.php.net/manual/en/function.json-encode.php).
