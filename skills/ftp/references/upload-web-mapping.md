# Verify an authorised upload and its HTTP mapping

Use this only when writing a selected test file to the service is part of the task. You need the FTP host, known login, approved remote directory and evidence for its possible HTTP URL. A directory named `upload` does not establish a shared filesystem or URL mapping.

Prepare a uniquely named `.txt` file containing a non-sensitive marker in your local task directory. Check the intended remote name and use one that will not overwrite an existing object. Enter the normal FTP session from the local directory holding that file. At the **FTP prompt**, use actual names in this adaptable sequence:

~~~text
binary
pwd
cd approved-remote-directory
ls
put unique-marker.txt unique-marker.txt
bye
~~~

An FTP `230` indicates login. A preliminary `125`/`150` starts a data transfer; look for its final completion response, typically `226`. A denied `put` establishes a write limitation even when login or downloads work. A completed transfer establishes storage through this service, not publication at a guessed URL. Follow the entrypoint's passive/active data-path diagnosis if transfer stalls.

If the task also permits verifying the corresponding web resource, define `url` as that exact URL (including the correct virtual host), `headers` and `body` as fresh local output paths. A bounded HTTP capture using an available curl is:

~~~bash
curl --silent --show-error --max-time 15 --dump-header "$headers" \
  --output "$body" --write-out 'HTTP %{http_code}\n' "$url"
~~~

Check curl's exit status, HTTP status and the captured body. Compare the marker bytes with the original; a status 200 alone could be an error page or another virtual host. This command does not follow redirects; inspect their destination and scope before a separate request. A matching marker supports this specific FTP-to-HTTP mapping. It does not demonstrate execution of ASP/PHP or any other server-side code, even if the uploaded filename had such an extension.

Report the exact remote path, tested URL, transfer completion and content match/mismatch. Leave cleanup of this exact marker explicit according to the task's authorization; never expand it to a directory-wide delete.

Sources: [tnftp transfer commands](https://man.netbsd.org/ftp.1), [FTP reply meanings](https://www.rfc-editor.org/rfc/rfc959.html), [curl output options](https://curl.se/docs/manpage.html).
