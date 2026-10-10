# Capture a selected static document

For a static or load-complete document, save this small driver as a task-local `capture.js`. It uses the installed renderer rather than reimplementing rendering. Define `url` and `output_pdf` before invocation; choose a new output path so stale output cannot masquerade as success.

~~~javascript
var system = require('system');
var page = require('webpage').create();
if (system.args.length !== 3) {
    console.error('usage: capture.js URL OUTPUT');
    phantom.exit(2);
} else {
    page.viewportSize = { width: 1280, height: 900 };
    page.paperSize = { format: 'A4', orientation: 'portrait', margin: '10mm' };
    var timer = setTimeout(function () {
        console.error('page-load timeout');
        phantom.exit(3);
    }, 30000);
    page.open(system.args[1], function (status) {
        clearTimeout(timer);
        if (status !== 'success') {
            console.error('page-open failed: ' + status);
            phantom.exit(1);
            return;
        }
        page.render(system.args[2]);
        phantom.exit(0);
    });
}
~~~

~~~bash
phantomjs capture.js "$url" "$output_pdf"
~~~

The timeout is a driver choice, not a PhantomJS default. PDF output uses `paperSize`; image output uses the appropriate filename extension and viewport/clip behavior. Check that an artifact was produced, that it parses as the requested type and that its pages contain the expected marker/content. The driver exit alone does not perform those checks.

For a dynamic page, `page.open` completion is often too early. Replace immediate rendering with a bounded check of a known page-ready condition, such as a specific DOM element or application state. Define both the condition and timeout from the application. Avoid treating an arbitrary sleep as evidence all requests finished. If the condition never appears, inspect script/resource errors and engine compatibility before retrying.

When diagnosing a document-generation service, compare the supplied input, observed fetches and resulting artifact. A callback hit proves a resource request; it does not prove injected JavaScript executed. An expected marker in the PDF is stronger rendering evidence. Keep local-file access or script-execution tests separately scoped and recorded instead of inferring them from a User-Agent header.

See the [page API](https://phantomjs.org/api/webpage/method/open.html) and [PDF paper sizing](https://phantomjs.org/api/webpage/property/paper-size.html). These instructions do not assume the renderer is equivalent to a current Chrome installation.
