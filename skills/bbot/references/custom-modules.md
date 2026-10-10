# Custom modules, lifecycle and authority

Use the installed BBOT version and a reviewed preset/module directory. A custom module is Python code loaded by the BBOT process; the module's flags do not create a security sandbox. A trusted module can implement the task's selected local action or emit events for existing collectors. Keep substantial task logic in the selected module, rather than replacing BBOT's event dispatch.

## Load one known module

Choose an absolute owned directory and save `identityprobe.py` there. This illustrative module logs the process identity during setup and each supplied DNS event without launching a shell or writing a privileged file:

~~~python
import os
from bbot.modules.base import BaseModule

class identityprobe(BaseModule):
    watched_events = ["DNS_NAME"]
    produced_events = []
    flags = ["passive", "safe"]
    meta = {"description": "Report process identity and selected DNS events"}

    async def setup(self):
        self.info(f"identityprobe setup euid={os.geteuid()}")
        return True

    async def handle_event(self, event):
        self.info(f"identityprobe event={event.data}")
~~~

The module class name must match the filename, ignoring case. `def MyModule(BaseModule)` defines a function, not a subclass. Include both event lists even when no events are produced. `setup` occurs once; `handle_event` receives matching events. A setup marker establishes setup execution; an event marker additionally establishes dispatch. Choose watched/produced event types for the real task rather than leaving this diagnostic module unchanged as a collector.

Create a preset with the following structure, replacing `/absolute/path/to/reviewed-modules` with the actual chosen directory. This is a placeholder, not a claimed installation path:

~~~yaml
modules:
  - identityprobe
module_dirs:
  - /absolute/path/to/reviewed-modules
~~~

Define `preset_file` as its absolute filename, `target` as a scoped DNS name and fresh `scan_name`/`out_dir`. The directory must contain the matching module file and be readable by the executing identity:

~~~bash
bbot -p "$preset_file" -t "$target" --no-deps -n "$scan_name" -o "$out_dir"
~~~

A typo between the saved preset filename and `-p` selects a different or missing file. Diagnose preset lookup, module directory, filename/class, syntax, dependency and setup errors separately. `--force` cannot turn an invalid function definition into a valid module. If no event marker appears, check whether the target generated the watched event and whether the module loaded; a scan-start banner alone proves neither.

Current upstream preloading reads module metadata through an AST and skips a file lacking the expected class metadata. Actual loading then executes the module file before locating the matching class. Therefore top-level Python effects can precede a later load failure **if the file reaches loading**; a skipped malformed file cannot be assumed to have executed. Keep work inside lifecycle methods when ordering/evidence matters. Do not infer which stage ran solely from an artifact displayed in a walkthrough.

`--dry-run` stops before the scan loop but current CLI preparation occurs first. Module imports/setup, dependencies and output preparation can precede that stop. It is not a sandbox or a safe way to inspect untrusted Python/presets. For untrusted files, read the selected YAML and Python as text; do not import them to discover their behavior.

## Validate a permitted privileged task

An exact BBOT executable in sudoers can still load a caller-selected preset and `module_dirs` when its argument grant permits them. The resulting Python runs with that process's effective identity. `secure_path` fixes executable search, not an explicitly selected Python directory; `NOPASSWD` removes the matching authentication prompt, not the argument restrictions.

Inspect `sudo -l`/`sudo -ll`, the permitted RunAs identity, arguments and the deployed loader. When the task authorizes an execution check, use only the reviewed module above (or the task's equally controlled marker), a scoped target and an output directory writable by that identity. Define `bbot_bin` as the exact permitted executable and `runas` as the permitted target identity:

~~~bash
sudo -n -u "$runas" "$bbot_bin" -p "$preset_file" -t "$target" --no-deps -n "$scan_name" -o "$out_dir"
~~~

An illustrative `identityprobe setup euid=0` proves that module setup ran as root in that invocation. A different UID proves only that identity. A denial or missing marker leaves execution unconfirmed. Preserve the exact policy, inputs and marker; inspect those specific restrictions before retrying, instead of adding `--force` or assuming a path-only grant covers every operation. Other task actions can then run inside the reviewed module under that established identity when authorized; a nonzero later scan status does not undo an earlier observed action.

For adaptation use the [module authoring API](https://www.blacklanternsecurity.com/bbot/Stable/dev/module_howto/) and installed-version source. Current [loader](https://github.com/blacklanternsecurity/bbot/blob/stable/bbot/core/modules.py) and [CLI preparation order](https://github.com/blacklanternsecurity/bbot/blob/stable/bbot/cli.py) distinguish preloading, importing, setup and scan execution.
