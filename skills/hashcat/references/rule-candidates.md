# Generate a pattern-based candidate file

Use when acquired evidence supports a password seed/pattern and a bounded rule-derived candidate set is useful for an offline verifier or a separately authorized online consumer. This is a candidate-generation task; `--stdout` does not compare a hash or establish a password.

Define `seed_file` as an existing private newline-delimited file containing the exact reviewed seed bytes, `rules` as the existing verified rule-file path, and `candidates`/`generation_log` as fresh private outputs. Select the intended rules rather than assuming a filename such as best64 means a fixed number of candidates or has a universal installed path:

~~~bash
umask 077
hashcat -a 0 --stdout -r "$rules" "$seed_file" > "$candidates" 2> "$generation_log"
status=$?
~~~

Require successful status and inspect stderr before handing off the file. A partial output left by failure is not the full selected space. Seed-file input avoids interactive shell history expansion of exclamation marks, dollar/backtick reparsing and accidental `echo` options. Preserve intended encoding, whitespace and line boundaries; embedded newlines are record separators in this workflow.

Rule operations can change case, reverse text, append/prepend characters or reject candidates. An unchanged identity rule preserves the original only when it is actually present. Repeated rules/seeds can emit duplicates; rejected candidates and consumer length/encoding limits mean generated-line count and actually tested count differ. Inspect the installed rule syntax and the chosen rule file. Do not claim every possible variation of a phrase was generated.

For a known local bcrypt record, hand the resulting file to the chosen offline checker with the complete record, matching format and case-specific pot/session. Hashcat mode 3200 or a supported John bcrypt format is an input choice made from the record's producer/representation, not from the seed. Interpret parser acceptance, recovery and exhaustion using that checker. No record is required to generate the candidates themselves.

If duplicate removal is useful, write a separate result rather than replacing evidence. A byte-oriented sort/unique pass changes candidate priority; retain the original order if the consumer's attempt budget makes priority matter. Count/review the final file before a live authentication task. Do not enable another consumer's rewrites implicitly: that can broaden the space and increase attempts after the shortlist was selected.

An **illustrative** seed `TeamPhrase!` with rules for identity, lowercasing and a `1` suffix could produce `TeamPhrase!`, `teamphrase!` and `TeamPhrase!1`. These are invented examples, not a transcript, recovered secret, exhaustive list or promised best64 output. A domain clue justifies testing a hypothesis; it does not prove the same password is used by an application and an OS account.

Finish with the selected seed/rule inputs, generation status, resulting file and intended consumer/budget. Keep candidates and recovered secrets private. See [Hashcat's rule syntax](https://hashcat.net/wiki/doku.php?id=rule_based_attack) and [CLI options](https://github.com/hashcat/hashcat/blob/master/docs/hashcat-help.md) for `--stdout` and `-r`.
