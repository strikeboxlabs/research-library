---
name: dotnet
description: Select a .NET SDK/runtime and build or run a reviewed Linux project with explicit restore and launch behavior. Use when a DLL, project, target framework or inherited build settings causes confusing execution failures.
---

# Separate inspection, build and execution

Inspect the environment from the intended working directory:

~~~bash
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
~~~

A runtime can run a compatible compiled application but does not provide the SDK needed to build a project. `global.json` can select an SDK based on the working directory and its ancestors; the selected SDK version is distinct from the project's `TargetFramework`. Preserve a recovered project's framework before considering migration. Do not install an obsolete runtime merely because a historical writeup used it.

Read the `.csproj`, imports, referenced projects and applicable `Directory.Build.props`/`.targets` before invoking build tools on unfamiliar material. MSBuild tasks, package build assets and compiler analyzers can execute during restore/build. Running an arbitrary project under privileged `dotnet` grants that build/application the same execution context. A build is not passive decompilation.

For a reviewed fixture, define `project` as its absolute `.csproj` path, `configuration` as the chosen configuration and `framework` as an actual target from the project. Restore dependencies explicitly with the intended NuGet configuration when needed; `dotnet restore "$project"` can contact feeds and change caches/`obj`. After successful restore:

~~~bash
dotnet build "$project" --no-restore --configuration "$configuration" --framework "$framework" &&
dotnet run --project "$project" --no-build --configuration "$configuration" --framework "$framework" --no-launch-profile
~~~

`--no-build` also suppresses implicit restore; it can run stale output if build inputs/options differ. `--no-launch-profile` avoids unexpected settings from `launchSettings.json`. Put application arguments after `--`. A successful build does not establish successful application startup, listening, authentication or task completion.

For an existing framework-dependent application, `dotnet "$application_dll"` launches the actual assembly; `dotnet run` selects a project. Define the DLL path and retain its matching `.runtimeconfig.json`, `.deps.json`, dependencies and content where supplied. Missing framework, wrong architecture, absent native library and incomplete deployment are different failure classes. Not every managed DLL has an application entrypoint.

A PE-labelled managed DLL can be portable; native dependencies and platform-specific APIs can still prevent Linux execution. Preserve stderr/exit status and verify the intended application's observable result before changing target frameworks or rebuilding.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Bagel pp. 7–8, 23–26; Backfire pp. 9–10. Sources: [dotnet environment](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet), [build](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build), [run](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run), [SDK selection](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json), [MSBuild execution boundaries](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-security-best-practices), [deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/).
