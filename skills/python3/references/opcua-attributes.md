# Read one OPC UA Variable's attributes

Use a trusted Python environment with `asyncua` installed and one known Variable NodeId on an owned isolated diagnostic server. Establish the endpoint and namespace mapping from that server's configuration; an index such as `ns=2` is not portable between servers. The example assumes the fixture intentionally permits an anonymous session. A production endpoint requires its provisioned identity and security configuration, not a downgrade to satisfy this example.

Define `python_bin`, `endpoint` and `node_id` from that fixture. This performs a bounded metadata read without browsing recursively or writing values:

~~~bash
"$python_bin" -I - "$endpoint" "$node_id" <<'PY'
import asyncio
import sys
from asyncua import Client, ua

async def inspect():
    async with Client(sys.argv[1], timeout=4) as client:
        node = client.get_node(sys.argv[2])
        print("node", node.nodeid, "name", await node.read_browse_name())
        if await node.read_node_class() != ua.NodeClass.Variable:
            raise ValueError("selected node is not a Variable")
        for attribute in (ua.AttributeIds.AccessLevel, ua.AttributeIds.UserAccessLevel):
            value = await node.read_attribute(attribute)
            print(attribute.name, value.StatusCode, value.Value.Value)

asyncio.run(asyncio.wait_for(inspect(), timeout=15))
PY
~~~

`read_attribute` checks the returned status by default. Preserve the exception/diagnostic when a read fails; do not replace a failed UserAccessLevel read with AccessLevel and label it user authorization. The former is user-specific; the latter describes general variable capability. Bit 0 indicates current-value reading and bit 1 indicates current-value writing. These are advertised attributes, not an observed write result or permission to change a process. Application logic, transient state and additional controls still matter.

An identically named node in another namespace is a different object. Record full NodeId, qualified browse name, session identity/security and time with the result. No mutation is needed to report an inconsistent diagram, advertised access or missing user-specific evidence. For operational equipment, use its approved diagnostic route and owner-defined read scope; never infer control authority from successful connection or metadata.

Finish with the two attribute observations or the exact failed prerequisite, without silently turning unknown access into allowed access. See [asyncua Node API](https://opcua-asyncio.readthedocs.io/en/latest/api/asyncua.common.html#asyncua.common.node.Node.read_attribute) and [OPC UA Variable attributes](https://reference.opcfoundation.org/specs/OPC-10000-3/5.6.2).
