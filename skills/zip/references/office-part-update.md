# Update one reviewed Office package part

Require an owned, already readable Office ZIP package, a preserved original, an independent working copy and a reviewed staging directory containing the selected replacement part. ZIP packaging does not decrypt an encrypted Office file. Worksheet protection controls editing and differs from file encryption; hidden-column metadata is another separate property.

Select the exact root-relative member from the package's relationships. For SpreadsheetML, the displayed sheet name maps through `xl/workbook.xml` and its relationship file to a worksheet part; `sheet2.xml` is not inherently the second sheet visible to a user. Preserve namespaces, relationships and content types when making an XML-aware edit. A single-line regular expression does not generally parse XML.

Define `working` as the absolute working archive outside staging, `staging` as the reviewed package root and `member` as its exact relative path. Inspect the original member list first, then add/update only that member:

~~~bash
(
  cd -- "$staging" || exit
  zip "$working" "$member"
)
status=$?
~~~

Require zero status and inspect diagnostics. `zip -f` freshens only existing members whose staged files have newer modification times; it does not add new members. Normal add/update can also retain stale members or skip unchanged timestamps. Do not assume a broad `zip -fr ... *` proves the selected replacement reached the package.

Test the working archive with `unzip -t`, inspect the member list, then compare `unzip -p "$working" "$member"` bytes with the reviewed staged file. Store extraction in a fresh private comparison file and require both extraction success and equality; a CRC test alone cannot prove which XML revision was packaged. If a timestamp skip leaves old content, create a fresh package from the complete reviewed root and verify all required parts rather than publishing the stale copy.

Open the result in the intended document consumer and check the requested change and unaffected content. Repacking can invalidate signatures and requires consumer validation; keep the original available if the consumer rejects the package. See the [Info-ZIP manual](https://manpages.debian.org/bookworm/zip/zip.1.en.html), Microsoft's [SpreadsheetML structure](https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/structure-of-a-spreadsheetml-document) and [Excel protection distinctions](https://support.microsoft.com/en-us/excel/protection-and-security-in-excel).
