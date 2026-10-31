---
name: "s3scanner"
description: "Enumerate object-storage buckets for a domain or list, checking existence and public readability across AWS, GCP and other providers with s3scanner. Use to discover exposed bucket names behind an in-scope domain; existence is not authorization to read."
---

# s3scanner bucket enumeration

Installed invocation: `/usr/bin/s3scanner`, version `3.0.0` (Kali package s3scanner).

Read this entire SKILL.md before acting. Require an in-scope domain or explicit bucket-name list and an output file. Finish with the bucket states found (exists, public-readable, denied) and the provider coverage used.

~~~bash
/usr/bin/s3scanner --provider aws --scan --bucket-file "$names" -o "$out"
~~~

`--provider` selects the object store (`aws`, `gcp`, `digitalocean`, `linode`, `dreamhost`, or `custom` with a config file; default aws) and `--threads` bounds concurrency (default 4). Domain-mode derives candidate bucket names from the domain and its permutations — findings are name guesses that happened to exist, so record the derivation, not just the hits.

Public-readable means the listing or objects answered anonymous requests. Reading beyond what the engagement authorizes (private objects via guessed keys, writable buckets) stays outside this skill: a 200 on / is surface evidence, and a writable-bucket result is a finding to report, not an invitation to upload. Bucket absence in one provider is not absence everywhere.

References: [project documentation](https://github.com/sa7mon/S3Scanner).
