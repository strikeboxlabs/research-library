---
name: grafana2hashcat
description: Convert compatible offline Grafana password and salt records with iamaldi's grafana2hashcat.py. Use when iteration counts, salt encoding or mixed stdout would corrupt Hashcat input.
---

# Grafana record conversion

This skill concerns **iamaldi/grafana2hashcat**; similarly named converters can have different input formats and defaults. Define `converter` as the reviewed script path and inspect `python3 "$converter" -h`. Use selected records from a consistent database acquisition, retaining a separate account-to-record mapping.

The reviewed converter hardcodes PBKDF2-HMAC-SHA256 with **10,000 iterations**. Establish that algorithm and cost from the source application's version/configuration before using it. A Grafana filename or a SQLite writer-version label does not establish password parameters. Do not silently relabel records from another cost or algorithm.

Define `input_records` as a UTF-8 text file with one `hex_digest,literal_salt` record per line: exactly two fields, no header, no account name, no blank lines and no CSV quoting. The script splits on commas rather than parsing general CSV. Preserve the literal salt; do not trim meaningful spaces or hex-decode it. The digest is hex-decoded to bytes, then base64-encoded; base64 of the hexadecimal text is a different value.

Define `hashes` as a fresh private output:

~~~bash
umask 077
python3 -X utf8 "$converter" "$input_records" -o "$hashes"
~~~

Use `-o`: stdout also contains banners and suggested commands, so redirecting all stdout produces contaminated input. The output file is overwritten if it exists. Check process status, output record count and one-line `sha256:10000:base64_salt:base64_digest` structure; malformed input can abort conversion. Independently decode a sample's two base64 fields and compare them to the source bytes.

For example, this synthetic input uses the known fixture password `secret` and salt `pepper`; it is not a recovered account credential:

~~~text
3ad31dc57a7452c442f259cfff7aa61f2a6cea88ee634724ae146e221ae4e01c56c8bcbb3552310acd2fd746a396d2f99bf8,pepper
~~~

Its converted record is:

~~~text
sha256:10000:cGVwcGVy:OtMdxXp0UsRC8lnP/3qmHyps6ojuY0ckrhRuIhrk4BxWyLy7NVIxCs0v10ajltL5m/g=
~~~

Decoded `cGVwcGVy` must be the six bytes `pepper`; the digest field must decode to the 50 bytes represented by the input's 100 hex characters. If it decodes to ASCII hex instead, the conversion used the wrong representation. This fixture demonstrates conversion only. For an actual record, confirm its parameters and compare decoded bytes to its own source fields.

If a header such as `password_hash,salt` causes a hex-decoding error, fix the export to contain data rows only. A missing second field is malformed input, not a wrong password. Check for stale/absent output after any failure; do not feed a previous file to Hashcat as if the new conversion succeeded.

Compatible output belongs to Hashcat mode `10900`. Its dictionary is a positional argument; the converter's printed `--wordlist` is not the documented way to supply it. Define `wordlist`, private `pot`, unique `session` and `seconds` before a bounded offline check:

~~~bash
hashcat -m 10900 -a 0 "$hashes" "$wordlist" --potfile-path "$pot" --session "$session" --runtime "$seconds"
~~~

Successful conversion is a representation change, not password recovery or proof that the parameters were correct. Report source/account mapping, verified parameters and conversion count without publishing credential records.

Use the [converter implementation](https://github.com/iamaldi/grafana2hashcat/blob/main/grafana2hashcat.py) to check a local revision's assumptions and [Hashcat syntax](https://hashcat.net/wiki/doku.php?id=hashcat) for the installed cracking interface.
