---
name: facter
description: Query selected local system facts with Puppet Facter and diagnose missing, cached or overridden values. Use when OS or hardware inventory depends on Facter configuration and fact providers.
---

# Query the intended fact provider

Read this entire SKILL.md before acting. Identify the installed Facter version, trusted configuration and requested fact names before querying. Complete with the returned values, errors and provider/cache limits; a missing fact is not proof that the corresponding system feature is absent.

Facter can load Ruby custom facts and executable external facts. Treat its configured search paths and providers as executable inputs. For ordinary local inventory, use the normal user identity and disable those providers when only built-in facts are needed. Review the selected configuration before loading it; querying one name does not make arbitrary provider code passive.

~~~bash
facter --version
facter --help
facter --no-custom-facts --no-external-facts --json os.name os.release.major processors.isa
~~~

These options are documented for modern Facter; establish installed support before using them. Dot notation selects a nested field. Keep stdout and diagnostics distinct and check status before interpreting the result. An OS family or release value describes this execution environment; it is not package patch evidence or proof of the surrounding host's identity.

If a requested value is absent or differs from another inventory source, inspect the effective `facter.conf`, fact name and provider. Configuration can block fact groups or cache their values. When a fresh resolution is required, the documented `--no-cache` option disables loading and refreshing the fact cache for that invocation. It does not repair an unsupported or blocked fact. Preserve the original observation before changing query conditions. Legacy flat names may remain queryable even when absent from the default all-facts display.

For a custom-fact problem, inspect the deployed Ruby files and their search paths, including configuration and environment, before running them. External facts can be static data or executable programs and have a separate provider control. An environment variable rejected by sudo establishes that specific environment restriction; it does not establish that all configuration or command-line provider paths are constrained. Resolve that as a configuration/permission review, without loading an untrusted fact to demonstrate its authority.

Use the [Facter CLI reference](https://help.puppet.com/osp/8.11/Content/PuppetCore/Markdown/cli.htm) for option differences, [configuration reference](https://help.puppet.com/core/current/content/puppetcore/configuring_facter.htm) for blocking/caching, and [external facts](https://help.puppet.com/core/current/content/puppetcore/external_facts.htm) for provider behavior.
