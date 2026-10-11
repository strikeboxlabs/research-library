---
name: gluster
description: Inspect a selected GlusterFS cluster's volume names and metadata with the gluster CLI. Use for established storage administration, distinguishing control-plane visibility from client mount access.
---

# Inspect the selected cluster's volumes

Read this entire SKILL.md before acting. Identify the intended cluster node and established administrative connection context. Finish with command status, observed volume metadata and any access or coverage gap.

Check the installed `gluster --version` and help. Define `node` as the intended Gluster management node:

~~~bash
gluster --remote-host="$node" volume list
~~~

After a successful listing, define `volume` as one exact returned name:

~~~bash
gluster --remote-host="$node" volume info "$volume"
~~~

Preserve diagnostics and the selected node/name. A failed request is not an empty cluster; volume visibility does not prove client mount permission or file access. A volume's brick locations need not be reachable through the address used for the initial request.

For an already attempted client mount, inspect its actual client log. Name-resolution failure and missing/untrusted TLS credentials are separate prerequisites; resolve the indicated hostname or established certificate setup rather than disabling TLS. Volume creation, start/stop, option changes and rebalancing are separate mutations.

See the [upstream CLI manual](https://github.com/gluster/glusterfs/blob/devel/doc/gluster.8) for this installed generation's command grammar.
