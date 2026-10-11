# Capture metadata for one known Elasticsearch index

Use the established, authorized Elasticsearch URL, trusted CA and authentication context. Choose an exact known index name; omitting it or supplying wildcards, comma-separated names or `_all` broadens selection. This procedure needs monitoring access and does not retrieve indexed records. Use the entrypoint's GET capture with `url` set to:

~~~text
https://<owned-endpoint>/_cat/indices/<exact-index>?h=health,status,index,docs.count&v=true
~~~

The placeholders are illustrative; use the service's actual scheme, host, port and exact index. Keep authentication in the established private configuration/header mechanism and retain status, headers and body from the same request. Check curl's exit status before interpreting the table. An HTTP error, filtered result or missing row does not establish that the index does not exist.

CAT is intended for human diagnostics. For automation, choose the relevant structured index/health/count API instead of treating this table as an application contract. `docs.count` comes from Lucene and includes hidden nested documents; it is not necessarily the number of application records. Use the count API when that distinction matters. `yellow` means all primary shards are assigned and at least one replica is unassigned; it does not mean all reads failed. A single row reports that index's observed state, not complete cluster health or a consistent snapshot across later requests.

Record the exact endpoint/index, status, returned fields and any permissions or coverage gaps. See the [CAT indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices) for the deployed version's parameters and required privileges.
