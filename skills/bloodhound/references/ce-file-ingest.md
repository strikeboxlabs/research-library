# Import an acquired collection into the selected CE instance

Require the approved, already running BloodHound CE endpoint, an account permitted to ingest there, and the reviewed ZIP/JSON collection. Establish receiving version and producer/schema compatibility first. A historical Legacy desktop launcher and direct Neo4j login are different workflows; do not infer the CE endpoint or credentials from those defaults.

Record the selected archive digest, actual filename, producer, collection time/methods and known failures. Collector counts describe emitted evidence, not accepted records. An output-prefix argument can differ from the generated ZIP name; select the file actually produced rather than constructing its name from that argument.

Sign in to the selected CE web interface. Open **Administration → Data Collection → File Ingest**, then **Upload File(s)** and select that acquired ZIP or JSON. Labels can vary with the receiving release. Uploading writes to that instance's graph; choose an isolated owned instance beforehand when attribution requires separation. Do not deploy or clear another database to work around an import error.

Retain the ingest job's completion, warnings/errors and available counts. An empty job table, file picker or upload receipt does not establish successful ingestion. Resolve a format error against the producer and receiving versions; preserve failed files and diagnostics instead of silently dropping them. Partial acceptance limits subsequent graph conclusions.

After ingestion completes, use **Explore** to find a fully qualified known object. Verify its domain, SID/type and selected relations against the collection. Apply the entrypoint's permission-edge interpretation: an imported `GenericWrite`, `AddMember` or `MemberOf` relation records captured configuration, not a performed change, current token or successful desktop login. A missing relation can reflect collection or ingestion gaps.

Finish with instance identity, selected archive provenance, ingest outcome and the requested redacted object/edge evidence. Closing the browser preserves the imported records; account for retention in the task result.

Reference: [SpecterOps CE quickstart: data ingestion and Explore](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart).
