# Seventh CTF writeup batch

Reviewed 2026-10-09. All three supplied Hack The Box writeups were processed: **51 physical PDF pages** were text-extracted and read, with **26 selected pages** rendered and visually inspected. This batch adds **seven independent tool skills** and enriches **seven existing skills**, bringing the catalogue to **94**.

Each new package contains one `SKILL.md`. Curl gains one conditional HTTP-proxy reference. ILSpyCmd is an explicitly researched Linux CLI alternative to the dnSpy workflow in Bagel. Workers need selected skill folders only; this report is maintenance evidence. Originals and intermediate material remain in ignored `ingest/` and `work/pdf-ingest-batch7/`.

## Coverage of all three documents

Page numbers are one-based physical PDF pages, including covers. Repeated commands were reviewed without adding duplicate instructions.

| Document | Pages | Accepted guidance |
|---|---:|---|
| `Backfire.pdf` | 13 | Controlled local .NET execution rather than online compilation of token material (9–10); sudo command capabilities (12–13); iptables backend/table/order and mutation semantics, save-file effects and restore boundaries (12–13). WebSocket and listener evidence was also reviewed; corrections appear below. |
| `Bagel.pdf` | 26 | Bounded Wfuzz response filters and PID coverage (7–8); PE/.NET classification (8); Linux CLI decompilation, property access and reconstructed-source limits (9–20); server-side text normalization (16, 21–22); SDK/runtime selection, project/build execution and sudo interpretation (23–26). |
| `Bamboo.pdf` | 12 | Go module/build behavior and scanner-source review (2–3); native HTTP proxy forwarding versus CONNECT (3–6); scoped LinPEAS selection and interpretation (7–8); application-trigger/process correlation and exact writable-script evidence (9–12); Bash real/effective-ID behavior (12). |

New skills: `dotnet`, `file`, `go`, `ilspycmd`, `iptables`, `iptables-save`, `linpeas`.

Enriched skills: `bash`, `curl`, `jq`, `proxychains`, `pspy`, `sudo`, `wfuzz`.

## Corrections and useful distinctions

- **Firewall operations:** Backfire's comment-bearing `iptables -A` changes live policy; its subsequent `iptables-save -f` writes a file under the program's privileges. This is a consequential capability of the sudo grant, not ordinary persistence or a demonstrated version-specific iptables vulnerability. Saving, restoring and installing boot-time persistence are different operations. Backend, address family and namespace bound visibility. A default-table listing is not the complete firewall; rule ordering and other hooks affect acceptance. The new skills capture those distinctions without reproducing the authorized-keys overwrite.
- **WebSocket framing:** Backfire's `404` establishes an HTTP response in that test, not a successful upgrade. A valid opening handshake needs the expected `101` and acceptance headers. Its fixed zero mask is not a standards-compliant client masking strategy: `0xfe` sets the mask bit and selects a 16-bit length, rather than describing an unmasked server frame. RFC 6455 requires fresh unpredictable client masks and minimal length encoding. The helper also does not support arbitrary larger payloads or a complete frame lifecycle. No general WebSocket client was inferred from this custom transport.
- **Listener and access changes:** Backfire's displayed `0.0.0.0:7096` is a wildcard listener, not loopback-only merely because the initial external scan omitted it. Remote reachability and service identity need separate evidence. Its `>` redirection into `authorized_keys` replaces the existing contents. Bamboo also shows an overwrite, and generating a key on the remote host is not necessary to authorize an already held client public key. These persistent access changes were not added as session-repair defaults. Existing SSH, socket and key-identity skills already cover the reusable distinctions.
- **Managed binaries:** Bagel's `file` label reflects the PE container and managed metadata. It does not establish Windows-only execution or a mandatory 32-bit runtime; the writeup itself runs the .NET application on Linux. A DLL is not automatically a native library or runnable application. ILSpyCmd supports the inspection task on Linux, with tool-runtime requirements distinct from the inspected assembly's framework. Reconstructed C# and a generated project are not the original source tree or proof of a successful rebuild.
- **Code-review evidence:** the shown object-typed `RemoveOrder` is an auto-property, not an absence of implementation. Trace setters during deserialization and getters during response serialization. A response property reading `Unauthorized` is not proof that authorization was enforced. The Json.NET root-type note concerns serialization and does not establish a requirement to supply a root type for the demonstrated nested-property deserialization. A binder/type policy and actual reachable property behavior matter. Nullable metadata is not a blanket statement that null is accepted at runtime. The generic controller/service/repository summary is not demonstrated by the shown event-handler code.
- **Text reconstruction:** JSON escapes are representation, not automatically corruption. Decode the correct field rather than replacing every literal backslash-n. Bagel's application already reads lines and joins them, so decoding cannot recover original line endings or a missing final newline. Validate the recovered key/configuration with its intended parser, preserving the original response. A format-specific terminator repair is different from claiming byte-identical recovery.
- **Build versus execution:** Bagel's `dotnet run` can restore dependencies, execute build logic and launch the project. Granting privileged execution of that runtime/build entrypoint is not a narrow permission to inspect DLLs. The SDK, selected target framework and installed runtime are separate facts; `global.json`, parent build files and package assets influence behavior. A temporary directory is not inherently safe or guaranteed to be cleared on reboot. Backfire's suggestion to use an online compiler is unsuitable for private signing material; local reviewed fixtures cover the useful tool task.
- **Go and the linked scanner:** the prose's `go.mod tidy` is a typo; the shown `go mod tidy` is correct but can modify dependency manifests. The linked scanner is a small source-configured program, not a CLI with safe discovery flags. It hardcodes proxy-side loopback, scans 1–65535 with 100 workers, and classifies by absence of one Squid error phrase. Its dial timeout is not a total request/body timeout; it follows redirects by default, can omit response-body cleanup on one branch and appends to a shared result slice without synchronization. It cannot support the writeup's general open-port conclusion without independent verification. No scan or source repair was performed.
- **Proxy paths:** ProxyChains' HTTP mode uses CONNECT. Curl's ordinary HTTP proxy mode uses forwarding, so success with one mode does not imply the other is allowed. `NO_PROXY` may bypass an explicit curl proxy unless deliberately overridden. Proxy errors, CONNECT success and origin responses are distinct. A destination loopback address is interpreted in the proxy's context. Keep destination and redirect scope explicit.
- **Enumeration and actual privilege:** current LinPEAS flags can enable authentication attempts, network discovery and online inventory submission. The reviewed `-a` implementation enables more than passive collection, and its README/help descriptions differ in detail. Scoped selection and observed evidence are preferable to treating highlights as findings. Bamboo's privileged invocation uses an absolute script path; the demonstrated issue is writable-script execution, not proven PATH hijacking. File-content write and directory replacement rights differ. Correlate an application action with process observations rather than treating all concurrent processes as caused by the action. Bash `-p` preserves an existing effective identity; it does not grant root from nothing. Bamboo's final output retains the original real UID while showing effective UID 0.

Primary manuals/source are linked inside each accepted package. Additional review sources: [RFC 6455 handshake and masking](https://www.rfc-editor.org/rfc/rfc6455.html), [Json.NET type handling](https://www.newtonsoft.com/json/help/html/T_Newtonsoft_Json_TypeNameHandling.htm), [Microsoft deserialization rule](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2326), [PaperCut's historical fixes](https://www.papercut.com/kb/Main/PO-1216-and-PO-1219/), [the shown PaperCut PoC](https://github.com/horizon3ai/CVE-2023-27350/blob/main/CVE-2023-27350.py).

## Reviewed material not turned into skills

| Material | Decision and remaining work |
|---|---|
| Backfire's Havoc SSRF/compile-injection chain and HardHat operator creation | Reviewed the custom transport, token and state-change evidence. These are application-specific exploit/C2 workflows, not enough for a general Linux utility skill. Hardcoded credentials, account creation, callback payloads and persistent SSH access were not copied into portable examples. Existing JWT/HTTP/SSH skills cover the generic decisions. |
| Bagel's custom deserialization payload and reverse-shell project | Retained static inspection, serialization and build-context lessons. A reusable application test needs its own fixture, type policy, known before-state and intended effects. Writing `orders.txt` is a mutation even when described as a test. Credential reuse and broad PID probing were not made automatic fallbacks. |
| Bamboo's PaperCut exploit and replacement of a privileged script | The historical affected/fixed build ranges matter; a banner saying only “22” is insufficient. PaperCut documents fixes including 22.0.9. The shown PoC changes scripting settings and then assigns cleanup values; that is not proof of restoration to the original state. Modifying a vendor script or making Bash setuid is persistent system modification. No generic payload or automatic cleanup procedure was inferred. |
| Bamboo's `squidscan` gist | Source reviewed for build and interpretation lessons. Deferred as a standalone skill because its unbounded default scope, response heuristic and implementation defects need a corrected controlled fixture first. Native curl guidance covers selected HTTP verification. |
| Repeated Nmap, curl transfer, procfs reads, jq, SSH forwarding, key inspection, script PTYs and ordinary shell commands | Existing coverage was retained. Only demonstrated guidance gaps produced edits. Native GUI actions and application-specific administration remain source context. |

All three PDFs are processed. Deferred material is a coverage decision, not unread input. The earlier uncommitted batch and unrelated assessment methodology were preserved.

## Source fingerprints

SHA-256 identifies the exact originals even after the ignored inbox is replaced.

| File | SHA-256 |
|---|---|
| Backfire.pdf | `927e43e5ac0e77e8413cc19c6974bcd0cd4ab7de801a2632f39c9244494986f7` |
| Bagel.pdf | `7787298d83b645ebc720dcd7f94d991c7489fd8b1f67195b3620b2a43b6ef25d` |
| Bamboo.pdf | `1e8e424aec725112f1a773dcab03aed8ea6075bf62f549e224ac63e757994c3a` |

The Netfilter Git source endpoint returned an anti-bot page; command guidance was verified against the upstream manuals mirrored by man7 instead. An outdated LinPEAS source path returned 404; the repository tree identified its current flag implementation. These retrieval issues did not leave accepted command semantics dependent on unavailable material.

See the [validation record](validation.md) for executed checks and the [Linux adaptation guide](../GETTING_STARTED.md#2-adapt-to-this-machine) for installed-help and fixture validation on the intended host.
