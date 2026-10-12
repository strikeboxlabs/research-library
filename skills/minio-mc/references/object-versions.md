# Retrieve one selected owned object version

Require the selected trusted MinIO `mc_bin`, private `config_dir`, provisioned `alias`, approved `bucket` and exact known nonsecret `object_key`. Set `object_ref` to `alias/bucket/object_key`. Metadata/list access and version-specific read access can differ.

~~~bash
"$mc_bin" --config-dir="$config_dir" version info "$alias/$bucket"
"$mc_bin" --config-dir="$config_dir" ls --versions "$object_ref"
~~~

Check each status and preserve the exact key, complete version ID, operation/type, size and timestamp with timezone. Enabled versioning does not prove this object has older versions. A prefix listing can include other keys: select the exact intended object. A delete marker is distinct from retrievable content. The displayed v1/v2 labels are presentation order; select the complete version ID rather than infer an ID or date from those labels. A missing/denied history cannot be repaired by enabling versioning now.

Define `version_id` as the observed intended content version and `download_file` as a fresh absolute local filename in a private owned directory. Inspect and copy that same version:

~~~bash
umask 077
"$mc_bin" --config-dir="$config_dir" stat --version-id "$version_id" "$object_ref"
"$mc_bin" --config-dir="$config_dir" cp --version-id "$version_id" "$object_ref" "$download_file"
~~~

Check inspection status before copying and retain the copy's final result. Omitting the version ID selects the current object; copying both versions to the same filename destroys that distinction. Preserve separate files and list/extract archives in separate new directories before comparing. A progress line or complete byte count is transfer evidence, not publisher authenticity or proof of the archive's members. Compare acquired size and a complete independently supplied digest when available; do not assume an S3 ETag is always the file's MD5. Keep partial downloads explicit.

Finish with endpoint/alias, bucket/key, full version ID, selected metadata, local path and verification limits. These commands read existing storage and write only the local copy; they do not restore, remove or change remote versions.

References: [version-info implementation](https://github.com/minio/mc/blob/master/cmd/version-info.go), [version listings](https://docs.min.io/aistor/reference/cli/mc-ls/), [stat](https://docs.min.io/aistor/reference/cli/mc-stat/), and [version-specific copy](https://docs.min.io/aistor/reference/cli/mc-cp/).
