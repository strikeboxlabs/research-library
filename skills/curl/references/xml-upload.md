# XML upload, external entities and server-side file evidence

Use for an authorized XML-processing test with an established upload field/schema and selected server file. First send an ordinary valid document with a unique text marker and observe which data node is returned. This separates upload routing, document parsing and reflected content. Keep cookies/CSRF requirements from the actual form; an upload extension or a Gunicorn banner does not identify the XML parser or its options.

The following **illustrative** document fits a form expecting `creds` with `Author`, `Subject` and `Content`. Adapt the schema to the real handler. Save it as a private `xml_file`, first using literal `owned-xml-marker` in Author as the normal control:

~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE creds [
  <!ENTITY chosen SYSTEM "file:///absolute/server/task/marker.txt">
]>
<creds>
  <Author>&chosen;</Author>
  <Subject>owned-xml-test</Subject>
  <Content>selected document</Content>
</creds>
~~~

For the external-entity case choose that file URI from an explicitly permitted existing marker or selected file; it refers to the **server parser's** filesystem/namespace, not curl's local disk. Match DOCTYPE to the root name and preserve the XML encoding. Supply the entity reference in the node the application actually returns. An entity definition alone does not demonstrate expansion.

Define `url` as the verified upload route, `file_field` as its actual multipart field and `headers`/`body` as new private capture paths. This assumes simple local filenames without curl form metacharacters:

~~~bash
umask 077
curl --silent --show-error --connect-timeout 5 --max-time 30 \
  --form "$file_field=@$xml_file;type=text/xml" \
  --dump-header "$headers" --output "$body" \
  --write-out 'status=%{http_code}\n' "$url"
~~~

Let curl construct the outer multipart boundary. `text/xml` labels this part; it is not the outer request Content-Type and does not turn malformed data into XML. Add only actually required ordinary form fields or authentication; do not invent a `data` field or reuse a GUI's Content-Length/boundary. Upload processing may store a file/post even if a later operation errors, so inspect the selected state before retrying.

| Result | Interpretation and next decision |
|---|---|
| Ordinary marker returned, selected file marker appears only in the entity case | Evidence of this server-side entity/file read. Record exact request and relevant response, with process-access limits. |
| Literal `&chosen;`, empty node or rejected DTD | Expansion might be disabled, the node unused or the handler different. Check the actual parser/configuration and control result before choosing another test. |
| Parse error for a selected file | The file may be missing, denied, invalid for the declared encoding or contain XML-significant bytes such as `<`/`&`. A parse error does not prove every file is unreadable; this method is not a general binary transfer. |
| HTTP 200 with an upload acknowledgement only | Confirms neither reflection nor file disclosure. Follow the application's actual selected result object. |
| Transport timeout or 500 | Request/outcome may be partial; preserve it and inspect state, not an automatic retry or success. |

After a confirmed read, an expressly selected application source/configuration file can reveal a route and its actual decoding/deserialization order. Read recovered Python as text; importing it executes code. A route name alone does not establish its body field, base64 alphabet, pickle serializer, authentication or deployed build. Use the observed handler contract to construct the next request; do not guess a source path merely from the application's name. A file read is separate from code execution, and the parser's file permissions still apply.

Primary guidance: [XXE file and upload behavior](https://portswigger.net/web-security/xxe), [XML document/DTD rules](https://www.w3.org/TR/REC-xml/), [curl multipart construction](https://curl.se/docs/manpage.html#--form).
