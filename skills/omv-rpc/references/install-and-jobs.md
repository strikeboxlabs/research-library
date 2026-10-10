# Selected package installation and background output

Use this only for a selected authorized installation on a backend matching these contracts. Define `rpc_bin` as the verified CLI, `remote_deb` as the complete reviewed .deb's absolute path **on the backend machine**, and `receipt`, `rpc_error`, `job_result` and `job_error` as fresh private local files. Confirm the backend can read that archive and compare its transferred size/digest. A client-local path or a completed scp alone is insufficient.

Inspect the package's control scripts, member paths/modes, provenance and intended effects before installing. In upstream 6.x, Apt.install accepts a `packages` string array and delegates to apt-get; a full local .deb path can be such a member when that backend/apt version accepts it. Shell-quoting a filename does not make its package hooks harmless. Package names from repositories and local archives have different provenance/dependency considerations.

Construct JSON with a serializer rather than interpolating a path into JSON text:

~~~bash
umask 077
params=$(python3 -c 'import json,sys; print(json.dumps({"packages":[sys.argv[1]]}))' "$remote_deb") || exit
"$rpc_bin" -u admin Apt install "$params" >"$receipt" 2>"$rpc_error"
status=$?
~~~

Check `status` and the error stream before continuing. The successful stdout is a JSON string naming a background status file, **not installation completion**. Keep it as a job receipt, not a shell command or the path of the installed package. The backend can resolve dependencies, change held/downgraded packages and remove packages according to its implementation; inspect the installed method's options before choosing this operation as a supposedly narrow file install.

## Collect this job's output

The 6.x Exec.getOutput parameters require `filename` and a nonnegative `pos`; optional `length` has a minimum of 1024 bytes. For the first read:

~~~bash
job_params=$(python3 -c 'import json,sys; f=json.load(open(sys.argv[1])); assert isinstance(f,str); print(json.dumps({"filename":f,"pos":0,"length":8192}))' "$receipt") || exit
"$rpc_bin" -u admin Exec getOutput "$job_params" >"$job_result" 2>"$job_error"
status=$?
~~~

Check status/error, then parse the JSON object. Keep `output` attached to that `filename`, and use returned `pos` for the next bounded read; do not reuse zero and mistake repeated text for new progress. Define `previous_result` as the last successful response and fresh output paths for the next read:

~~~bash
job_params=$(python3 -c 'import json,sys; r=json.load(open(sys.argv[1])); print(json.dumps({"filename":r["filename"],"pos":r["pos"],"length":8192}))' "$previous_result") || exit
"$rpc_bin" -u admin Exec getOutput "$job_params" >"$job_result" 2>"$job_error"
~~~

Continue under the task's observation budget with a sensible delay until `running` is false **and** `pendingOutput` is false. The latter distinguishes unread output from a finished process. Retain each reply before another read. Backend exceptions can report installation failure even after a receipt was accepted; do not interpret an exception as an empty successful output. A still-running job at the budget is incomplete, and a stopped job may already have made changes.

The 6.x implementation removes background status state when getOutput observes a finished process with no pending output. Exec.isRunning also removes it when finished; polling that method first can discard the later getOutput opportunity. Prefer getOutput throughout when logs matter. A subsequent missing receipt can reflect consumed/expired state, not proof the operation never ran. Do not invoke Exec.stop or kill a backend process as automatic log recovery; stopping package configuration has its own consequences.

## Establish the resulting capability

Inspect the selected package's installed/configuration state and intended effect through the task's existing access. A controlled postinst marker plus its `id` output in this exact job can show hook execution under the installer's identity. Output declaring a package unpacked does not establish that configuration finished or that every hook succeeded. If examining a privilege change, verify real/effective identity and the actual capability rather than inferring success from an archive name or a mode bit.

This local RPC trust model can give a service account access to privileged installation without that account itself being UID 0. Distinguish the current OS session, supplied admin RPC context, backend authority, package trust and final observed effect. Do not require a shell-injection flaw when caller-chosen package hooks already cross the boundary. Conversely, read-method success alone does not establish this install permission.

References: 6.x [Apt implementation](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/share/openmediavault/engined/rpc/apt.inc), [Apt parameters](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/share/openmediavault/datamodels/rpc.apt.json), [Exec behavior](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/share/openmediavault/engined/rpc/exec.inc) and [Exec parameters](https://github.com/openmediavault/openmediavault/blob/6.x/deb/openmediavault/usr/share/openmediavault/datamodels/rpc.exec.json).
