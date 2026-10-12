# Build a trusted spec with the intended resources

Require the complete reviewed `.spec`, application sources/hooks and the permitted ordinary build context. PyInstaller executes a spec as Python code; it is not a declarative list to hand to a privileged build service. Review imported helpers and path construction as well as the visible `Analysis` call.

Define `spec_file` as its absolute path and fresh owned `build_directory` and `output_directory` outside the input tree:

~~~bash
pyinstaller --workpath "$build_directory" --distpath "$output_directory" "$spec_file"
status=$?
~~~

When building a spec, most application options are already encoded there; adding script-mode options such as `--onefile` does not redesign that spec. The documented remaining overrides include work/dist paths, clean, log level, noconfirm and UPX directory. Avoid clean/overwrite options unless the selected artifacts actually need them.

For a reviewed public application resource, the spec's `datas` tuples select a source and destination relative to the bundle. This **illustrative** fragment includes the project's own public image:

~~~python
datas=[('assets/logo.png', 'assets')]
~~~

Resolve relative sources in the spec's documented location context and inspect exactly which files a glob adds. A packaged data file remains recoverable data; bundling does not encrypt it or grant permission to include it. Keep secrets and unrelated host files out of the bundle.

For command-line `--add-data`, consult installed help: current documentation uses `SOURCE:DEST`, while older examples can use platform-specific separators. After building, inspect the resulting resource layout and perform the application's actual resource-loading check in its intended environment. Separate spec generation, successful build and successful application launch.

References: [spec execution, options and data files](https://pyinstaller.org/en/stable/spec-files.html), [current command-line data syntax](https://pyinstaller.org/en/stable/usage.html).
