# HTTP virtual-host candidates and version differences

Use when varying the HTTP Host selects different applications on a known endpoint. Required inputs are the correct scheme/connection route, authorized hostname scope, a short candidate list and several negative controls. This is HTTP discovery; it does not establish that the names exist in DNS or that HTTPS SNI/certificate routing will behave identically.

Check `gobuster version` and `gobuster vhost --help`. Establish whether entries are bare labels or complete hostnames. For a release supporting `--append-domain`, define `url` with the intended domain, `labels` with bare candidate labels and `report` as a fresh path:

~~~bash
gobuster vhost -u "$url" -w "$labels" --append-domain -t 4 --delay 250ms -o "$report"
~~~

The current switch appends the selected domain; an IP-based URL needs the supported `--domain` value. A wordlist of complete hostnames ordinarily omits `--append-domain`. Older releases have differed in automatic appending: do not copy a historical command until one controlled request confirms the actual Host sent. Avoid both bare labels sent unintentionally and duplicated domain suffixes.

Compare a known/default host, multiple nonexistent labels and an interesting candidate with the same route/session. Preserve first-response status, Location, body length and distinguishing content. Following redirects with the supported `-r` option can collapse candidates into the same default/login page or change the host/credential context; a final 200 alone is not a discovered application. Length/status filters are response controls, not completeness guarantees; dynamic reflected hostnames can change lengths even for identical fallback pages.

Re-request a candidate directly with the intended Host. For HTTPS, verify SNI and certificate identity as well as HTTP Host; a manual Host override against an IP URL does not set the URL's TLS identity. A supported curl `--resolve` request with the hostname in the URL can check that combined route without changing system DNS. Keep HTTP-proxy behavior in view: current Gobuster warns that plain HTTP vhost mode through a proxy can route by the candidate Host rather than the selected target.

When the virtual host is confirmed, select its exact scheme/base path for subsequent `dir` work. A filtered directory listing is not proof of no readable files: a 403 parent or a 301 directory may still lead to selected children, and excluding 200 removes all successful responses of that status. Do not expand a candidate list just to compensate for an unverified routing/filter assumption.

Finish with confirmed candidate differences, actual hostname construction, route, controls and completed scope. An interrupted or entirely filtered scan supports only that bounded observation.

References: [Gobuster modes/releases](https://github.com/OJ/gobuster), [vhost options](https://github.com/OJ/gobuster/blob/master/cli/vhost/vhost.go).
