# Forms, assets and browser opener boundaries

Use Flask when the owned exercise needs a response-producing POST route rather than static file serving. Establish the interpreter, form action/method, field names and intended receiver origin first. A development receiver is not the original application's authentication service.

For a minimal owned `receiver.py`, the following accepts a public test marker without collecting credentials:

~~~python
from flask import Flask, request

app = Flask(__name__)

@app.route('/probe', methods=['GET', 'POST'])
def probe():
    if request.method == 'POST':
        values = request.form.getlist('marker')
        if len(values) != 1 or not values[0] or len(values[0]) > 80:
            return 'one bounded marker required\n', 400
        app.logger.warning('FORM marker=%r', values[0])
        return 'marker received\n', 200
    return ('<!doctype html><form action="/probe" method="post">'
            '<input name="marker"><button>Submit</button></form>'), 200
~~~

Use the entrypoint's interpreter/CLI to serve it, then test the same intended route. For an owned loopback receiver:

~~~bash
curl --silent --show-error --max-time 5 --data-urlencode 'marker=owned-test' \
  --dump-header "$headers" --output "$body" http://127.0.0.1:8080/probe
~~~

`headers` and `body` are fresh private files. Pair status/body with the receiver's `FORM` event. A missing field, JSON body, duplicate field or wrong method needs request/route correction, not a changed target password. For an expressly authorized credential-form exercise, adapt the exact observed form action and field names, use designated test accounts and private collection, and keep receipt separate from successful authentication. Do not make printing all real passwords a default receiver behavior. HTML `id` and displayed labels do not determine the POST names. The receiver's own route does not validate the original site's CSRF token.

With `render_template`, put owned templates in that application's `templates/` directory. Relative CSS/script/image URLs resolve using the page's document/base URL, so relocating a downloaded login page changes their destinations and often its appearance. Inspect `action`, any `base` element, inline handlers and asset requests. Deliberately use owned local assets or an authorized explicit asset origin; fetching remote JavaScript executes that origin's supplied code in the containing page. Do not assume `wget -O` also cloned dependencies or authenticated state.

## Selected opener-navigation exercise

A controlled page opened by another page may receive `window.opener`. In current browsers, ordinary `_blank` links generally imply noopener; explicit `rel=opener`, older implementations, `window.open` options and Cross-Origin-Opener-Policy change the result. Missing `rel=noopener` in markup alone is not current vulnerability proof. `nofollow` is a link relationship for crawlers, not the opener isolation control.

For a task explicitly testing navigation of an owned original tab, serve a controlled page containing this **illustrative** marker procedure, replacing the destination with the owned test origin:

~~~html
<script>
if (window.opener) {
  window.opener.location.replace('https://owned-receiver.example/probe?case=opener');
}
</script>
~~~

Reproduce the actual link-opening mechanism and browser/version. Record whether opener exists, whether navigation is permitted and whether the original tab visibly moves to the marker. A cross-origin opener allows limited operations including navigation; it does not allow reading the original document/cookies. A request for this page proves retrieval only; a request for the marker plus browser observation supports the navigation result. A server-side URL fetcher does not necessarily have an opener. An iframe's `parent` is a separate surface with sandbox/navigation restrictions; it is not an automatic replacement for a null opener.

JavaScript executed on the hosted page reads that page's origin cookies. An empty `document.cookie` there does not show that another application's cookies are protected by its framework, nor that same-origin XSS occurred. HttpOnly independently blocks script access to the applicable cookie, while the browser may still send it to its origin. Opener abuse from a page you control requires no same-origin XSS in the original site. If the selected exercise includes a simulated login, correlate the original tab's destination, designated test submission and receiver result; a visually matching page or source IP alone is not proof of account takeover.

See [opener behavior](https://developer.mozilla.org/en-US/docs/Web/API/Window/opener), [Flask request data](https://flask.palletsprojects.com/en/stable/quickstart/#accessing-request-data) and [template rendering](https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates).
