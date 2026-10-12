# Captured HTTP request and response

Use an existing authorized capture and installed Wireshark GUI. Open that file without starting live capture; display filter `http` selects dissected HTTP traffic. Select the actual request frame and retain its time, endpoints, method, Host, URI and conversation. A User-Agent is an asserted client label, not proof a particular executable ran.

Choose **Analyze → Follow → HTTP Stream**, or the packet-list context menu's matching Follow action. A missing/disabled action means the selected frame was not recognized as that protocol. If using TCP Stream instead, retain its index and distinguish the HTTP exchanges inside that connection. HTTP/2 also requires the correct substream. Follow changes the display filter; Back restores the prior filter.

Separate the request from its corresponding response, including status, headers and body. Select client-to-server or server-to-client data when helpful; default conversation view includes both. Theme colors alone do not identify direction. A GET request proves a request, not a successful or complete download.

For byte-preserving TCP export, choose Raw and Save As to a fresh private file. The saved binary omits display-added line separators; ASCII display replaces nonprintable bytes with dots. A server stream can include HTTP headers and multiple responses: it is not automatically the requested file. Preserve framing, encoding and missing-segment limitations before comparing extracted body bytes with another artifact. Review recovered source as data; capture contents do not establish that it was compiled, loaded or executed.

Finish with request/response frame or stream identity, observed status/body and completeness limits. See the [Follow Stream guide](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html) for installed-version controls.
