---
name: phantomjs
description: Render a selected page to PDF or an image with the PhantomJS CLI and diagnose legacy headless-browser results. Use when the installed renderer is PhantomJS and modern-browser assumptions or load-versus-render timing cause misleading output.
---

# Render through the installed headless engine

Read this entire file before acting. For rendering, read [capture and interpretation](references/capture.md) fully. Finish with the selected input, render artifact and actual completeness checks; a resource request or successful page open does not prove a complete PDF.

Check `phantomjs --version` and `phantomjs --help`. PhantomJS runs a supplied JavaScript program using its own runtime/WebKit; it is not Node.js and does not use Node modules. A server response mentioning PhantomJS is a lead to verify, not proof that the local CLI matches that server.

Use it when the task specifically needs this installed rendering engine. A modern page can fail because of unsupported JavaScript/CSS, missing fonts, TLS differences or asynchronous loading. Repeatedly increasing a delay will not repair unsupported language features.

Rendering a URL executes page content and may fetch additional URLs; local file input can also reference network resources. Keep the actual document and resource origins within the requested task. A browser-style local-file read, rendered text and OS command execution are distinct outcomes.

See [screen capture](https://phantomjs.org/screen-capture.html) and [page opening](https://phantomjs.org/api/webpage/method/open.html).
