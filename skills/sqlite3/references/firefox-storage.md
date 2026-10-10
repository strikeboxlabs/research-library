# Firefox profile evidence and extension BLOBs

Define `database` as the absolute path to a coherent working copy of the selected profile's database, preserving its captured WAL/SHM sidecars. Do not start Firefox against the evidence profile: it can migrate databases, update state and contact services. Inspect the schema before using the following queries; Firefox versions and extension storage differ.

## Distinguish stored pages from visits

`places.sqlite` includes bookmark/history information, not every kind of profile data. `moz_places` contains page records, while `moz_historyvisits` supplies visit records. A page title alone does not prove an extension was installed, a setting was enabled or a password/PIN had a particular form.

For the verified `moz_places(id,url,title)` and `moz_historyvisits(id,place_id,visit_date)` schema:

~~~bash
sqlite3 -init /dev/null -readonly -batch -bail -header -csv "$database" 'SELECT p.id, p.url, p.title, v.id AS visit_id, v.visit_date FROM moz_places AS p JOIN moz_historyvisits AS v ON v.place_id=p.id ORDER BY v.visit_date DESC, v.id DESC LIMIT 30;'
~~~

Keep the raw `visit_date` and verify its units against the producing Firefox version before conversion. A join can return several visits to the same page; it deliberately excludes page rows without a retained visit. Empty history can reflect deletion, acquisition limits or a different profile. Do not label all `moz_places` rows as visits to compensate.

## Inspect binary extension records before choosing a decoder

For an IndexedDB database whose actual schema includes `object_data(object_store_id,key,data)`:

~~~bash
sqlite3 -init /dev/null -readonly -batch -bail -header -csv "$database" 'SELECT object_store_id, hex(key) AS key_hex, typeof(data) AS storage_type, length(data) AS stored_bytes, hex(substr(data,1,16)) AS prefix_hex FROM object_data ORDER BY object_store_id,key LIMIT 20;'
~~~

Preserve the object-store ID and key with any selected field. SQLite can inspect and export BLOB bytes; it does not automatically interpret the application's serialization. Mozilla's implementation includes Snappy-compressed structured-clone data and out-of-line files. Decompression, where appropriate for that record/version, is not JSON parsing or vault decryption. Inspect the record's storage form and companion files before choosing a compatible decoder. A `strings`/hex hit is a locator, not a verified field association or complete extraction.

For a password-manager extension, a browser-history search about a short PIN is only a hypothesis. Recovery depends on the actual client format, persisted unlock material and account KDF settings. Do not substitute a current default for captured metadata or call “no match” proof of a longer PIN. This reference supports database triage; it does not recover vaults or generate authentication codes.

References: [Firefox profile contents](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data), [Places schema](https://github.com/mozilla-firefox/firefox/blob/main/toolkit/components/places/nsPlacesTables.h), [IndexedDB storage implementation](https://github.com/mozilla-firefox/firefox/blob/main/dom/indexedDB/ActorsParent.cpp), [SQLite CLI](https://sqlite.org/cli.html).
