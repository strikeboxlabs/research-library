# Retrieve reviewed wheels without source-build fallback

Use a trusted selected interpreter with pip installed, a local approved wheelhouse containing reviewed regular wheel files, and a fresh owned destination directory. Define `python` as that interpreter's absolute path, `wheelhouse` and `destination` as those absolute directories, and `requirement` as one exact distribution pin such as the **illustrative** `example-package==1.2.3`. This task takes a plain name/version requirement, not a URL, VCS reference or requirements file. Review active pip configuration/environment settings before resolution.

~~~bash
"$python" -m pip --version
"$python" -m pip download --no-index --find-links="$wheelhouse" --only-binary=:all: --no-deps --dest="$destination" "$requirement"
~~~

Retain status, selected filenames and exact artifact hashes. A compatible reviewed wheel is copied to the destination; the application environment is not installed by this command. A no-match error requires checking the pin, wheel tags, interpreter and available files. Do not turn on source fallback to make an unknown input resolve. `--no-deps` means the artifact set is incomplete when dependencies are required; it does not prove a deployable environment. Existing/stale destination files would weaken attribution to this invocation.

`pip download` is not a general passive downloader for untrusted source archives. Resolution may invoke build-backend hooks to obtain metadata, including legacy setup code, even without installation. Build isolation separates build dependencies from runtime dependencies; it does not confine arbitrary build code. Neither `--no-deps` nor `--no-build-isolation` supplies that confinement. Do not run source metadata/build code with elevated privileges as a diagnostic.

An HTTP 404 can reflect an incorrect artifact path or a private resource hidden from the command's authentication context. A browser login is separate from pip's credentials. Verify the approved artifact endpoint and access method; an HTML repository page is not distribution bytes. Making the repository public changes access scope and is not a retrieval repair. Keep authentication material out of URLs and saved logs. A source `.tar.gz` distribution and a `.whl` wheel are distinct outputs; seeing both names does not prove build completion or safe code.

References: [pip download](https://pip.pypa.io/en/stable/cli/pip_download/), [build metadata and isolation](https://pip.pypa.io/en/stable/reference/build-system/), [authentication](https://pip.pypa.io/en/stable/topics/authentication/).
