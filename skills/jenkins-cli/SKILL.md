---
name: jenkins-cli
description: Use the Jenkins Java CLI to verify controller identity and permissions and read an existing build log. Use when selecting transport, separating client authentication from command arguments or interpreting historical file-disclosure transcripts.
---

# Establish the controller and read an existing build

Use a trusted controller's `JENKINS_URL/jnlpJars/jenkins-cli.jar` with a compatible Java runtime. A downloaded JAR is executable code; its filename alone does not establish its origin. Keep the controller's context path in `jenkins_url`, such as `https://ci.lab.example/jenkins/`.

Define `java_bin` and `cli_jar` as the selected executable and trusted JAR paths. Define `auth_file` as an existing private file containing the authorized `username:API_token`, without displaying its contents:

~~~bash
jenkins=( "$java_bin" -jar "$cli_jar" -s "$jenkins_url" -webSocket -auth "@$auth_file" )
"${jenkins[@]}" who-am-i
"${jenkins[@]}" help
~~~

Place global client options before the command name. Check that `who-am-i` identifies the expected account; successful authentication does not grant every command permission. The controller supplies available commands, and plugins can add others. Check the selected command's help and required permissions before using it.

For a known existing job and build, define `job` as its exact Jenkins name, `build_number` as the observed numeric build number and `tail_lines` as a positive output limit:

~~~bash
"${jenkins[@]}" help console
"${jenkins[@]}" console "$job" "$build_number" -n "$tail_lines"
~~~

This reads that build's log without starting a build. Verify its identity and relevant stages before interpreting success or failure; a truncated tail may omit the cause. Increase the range deliberately or read the complete log when needed. A missing build or permission denial does not prove the job never ran. Keep captured logs private when they contain credentials or other sensitive values. Use an explicit build number: an omitted selector can resolve to a different run than intended. `-f` follows a running log and can keep the session open.

## Recover from connection and interpretation failures

WebSocket mode requires client and controller support; it is available from Jenkins 2.217 and is the default from 2.391. If a reverse proxy blocks its upgrade, verify proxy routing or deliberately select the supported `-http` transport instead. A transport failure does not establish invalid credentials. Keep HTTPS certificate verification enabled; investigate the trust chain/name instead of routinely disabling verification. Jenkins' SSH CLI service is separate from the host's ordinary SSH login service.

For historical CVE-2024-23897 evidence, distinguish the client's legitimate `-auth @file` (reads a local authentication file) from the vulnerable controller-side expansion of command arguments beginning with `@`. Fixes were released in 2.442, LTS 2.426.3 and LTS 2.440.1; check the actual build and configuration against the advisory.

Error messages containing file fragments are not necessarily an intact file transfer. In Jenkins 2.441, `connect-node` treats expanded lines as node names, deduplicates them through a set and can attempt actual node connections. Its errors can lose order and duplicate lines; it is unsuitable as a read-only file-copy procedure. Do not reconstruct complete XML, hashes or binary keys from a partial diagnostic transcript by guessing missing bytes.

Use the [CLI reference](https://www.jenkins.io/doc/book/managing/cli/) for transports and permissions, the [console implementation](https://github.com/jenkinsci/jenkins/blob/master/core/src/main/java/hudson/cli/ConsoleCommand.java) for selector behavior, and the [security advisory](https://www.jenkins.io/security/advisory/2024-01-24/) for affected versions and disclosure limits.
