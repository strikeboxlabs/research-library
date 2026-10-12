---
name: a2enmod
description: Enable one selected Apache module with the Debian-style a2enmod helper and verify configuration activation. Use when module symlinks, dependencies, MPM choice or an unchanged running daemon make an enablement result ambiguous.
---

# Enable the selected Apache module

Read this entire SKILL.md before acting. Require the controlled Apache instance, installed Debian-style helper, selected available module and approval for its configuration and service effects. Review the module's configuration/dependencies and validate before activating. No conditional resources are required. Finish with helper status, valid configuration and the requested application result after managed activation; missing module or failed activation remains unresolved.

Define `module` as the exact selected installed module name, `apache_ctl` as that instance's trusted apache2ctl wrapper, and `service_bin`/`service_name` as its established managed service interface. Inspect installed help and the available module's load/configuration files. CGI module choice, for example, depends on the selected MPM; do not copy a historical module name without checking that instance.

Run under the existing authorized administrative context:

~~~bash
a2enmod "$module"
enable_status=$?
"$apache_ctl" configtest
config_status=$?
~~~

The helper creates enabled-module symlinks to the installed available configuration; it does not install the module or immediately load it into the running daemon. Associated `.conf` directives can affect the main server context. Already enabled is not an error. Read dependency/conflict diagnostics and check both statuses; a configuration failure can leave the new symlinks present, so resolve or restore the intended configuration before activation.

For the selected instance, inspect the configured module list with `"$apache_ctl" -M`. This parses the current configuration and is not a query of modules in an already running process. A successful configtest also does not prove a live application endpoint works. These parser commands load configured modules and require trusted configuration/binaries.

Once configuration is valid, use that service's supported approved activation action. If restart is the selected action, account for its interruption:

~~~bash
"$service_bin" "$service_name" restart
activation_status=$?
"$service_bin" "$service_name" status
~~~

Retain activation/status diagnostics and check the intended ordinary application response. A failed restart can leave Apache stopped; a running PID can still serve the wrong virtual host or handler. Module enablement does not itself establish CGI mapping, repository export policy or permission to publish content. Configure those separately only when they are the selected task. If restoration is required, disable only the module added for this change with the installed `a2dismod` and validate/activate again; avoid forced cascading disables of unrelated dependencies.

References: [Debian helper semantics](https://manpages.debian.org/bookworm/apache2/a2enmod.8.en.html), [Apache control/configuration checks](https://manpages.debian.org/bookworm/apache2/apache2ctl.8.en.html).
