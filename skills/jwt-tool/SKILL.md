---
name: jwt-tool
description: Inspect and modify controlled JWT fixtures with ticarpi jwt_tool. Use when claim types, signing algorithms, key-file bytes or confusing decoded claims with verified identity causes mistakes.
---

# Inspect the token before selecting a mode

Use ticarpi's `jwt_tool.py`, not an unrelated package with a similar name. Check its help and version banner. Define `jwt_script` as the reviewed script's absolute path and `token` as the original compact JWT without its Bearer prefix:

~~~bash
python3 "$jwt_script" "$token"
~~~

This decodes locally when no target/request options are supplied. The first invocation may initialize configuration/keys and exit with status 1; inspect that setup message and rerun rather than diagnosing a token failure. The three segments are base64url-encoded header, payload and signature bytes; decoding does not verify the signature or establish that the service accepts the claims. Preserve the original string. Tokens appear in process arguments and this tool can retain them in local logs under `~/.jwt_tool`; use private fixture material and inspect its configuration before working with sensitive captures.

Read `alg`, claim types and timestamps, then establish the service's actual allowed algorithm and key source independently. A field named `API_KEY` is not necessarily the signing secret; BackendTwo established the connection through the application's settings. A changed account record also does not rewrite an already issued token. Obtain a fresh authorized login token when testing updated account state.

For an authorized **local HS256 fixture**, define `key_file` as a private text file containing the exact known HMAC secret, with no accidental trailing newline:

~~~bash
python3 "$jwt_script" "$token" -T -S hs256 -kf "$key_file"
~~~

Change only the intended claim in the interactive menu and inspect the resulting JSON type. The reviewed implementation reads the entire key file for signing. A hex-looking secret remains literal text unless the application explicitly decodes it. `-T` without signing can leave the original signature attached to changed contents; printing a token does not make it valid. Verify the resulting signature and applicable issuer/audience/time requirements using the intended verifier.

Do not infer HS verification from `-V`: its reviewed path concerns asymmetric signatures/JWKS. `-t` or `-r` adds HTTP delivery, and scan modes can generate many requests; they are separate from this local procedure. Expiration, algorithm rejection, signature failure and application authorization failure need separate diagnoses. Do not extend timestamps or broaden claims just to hide an unexplained rejection.

## Separate a JWT from the application's session

If a page loads but an action still returns insufficient privileges, inspect that action's actual authorization inputs before changing the token again. A handler may require both a JWT claim and server-side session identity. A valid local signature does not create the second state. In PHP, a session cookie identifies data loaded by the configured session handler; a guessed identifier alone does not populate an authenticated session.

Keep the exact nested claim structure: an illustrative `data.username` is not a top-level `username`. Compare each required identity with the captured request and reviewed handler. A response other than 302 is not proof of authentication: errors and denial pages can use 200 or 500, and a redirect does not establish that server-side execution stopped. Require operation-specific evidence. See [PHP session loading](https://www.php.net/manual/en/function.session-start.php), [redirect behavior](https://www.php.net/manual/en/function.header.php) and the [JWT data model](https://www.rfc-editor.org/rfc/rfc7519.html).

Browser `localStorage` is application-managed storage, not a cookie jar or an HTTP header. Identify how client code reads the stored object and attaches the token to requests before reproducing the API call. A changed local username or a newly visible page does not establish server-side identity. Keep the UI object's fields separate from claims inside the compact token; the latter may also be renamed by a framework's claim mappings. For example, a .NET `ClaimTypes.Name` can appear as `unique_name` on the wire under the applicable mapping. Inspect the actual token and validator configuration rather than guessing a claim name from a model property. See [localStorage behavior](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) and [IdentityModel's claim mapping](https://github.com/AzureAD/azure-activedirectory-identitymodel-extensions-for-dotnet/blob/dev/src/Microsoft.IdentityModel.JsonWebTokens/ClaimTypeMapping.cs).
