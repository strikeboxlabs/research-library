---
name: dotnet
description: Select a .NET SDK/runtime and build or run a reviewed Linux project with explicit restore and launch behavior. Use when a DLL, project, target framework or inherited build settings causes confusing execution failures.
---

# Separate inspection, build and execution

Read this entire SKILL.md before acting. Require a reviewed project/application and its intended framework/platform; inspect the environment and imported build settings before restoring, building or launching. No conditional resources are required. Finish with the selected SDK, actual build/startup result or specific missing prerequisite; compilation alone is not application completion.

Inspect the environment from the intended working directory:

~~~bash
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
~~~

A runtime can run a compatible compiled application but does not provide the SDK needed to build a project. `global.json` can select an SDK based on the working directory and its ancestors; the selected SDK version is distinct from the project's `TargetFramework`. Preserve a recovered project's framework before considering migration. Do not install an obsolete runtime merely because a historical writeup used it.

Distinguish modern .NET targets from **.NET Framework 4.x**. A project targeting `net48` or declaring `<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>` targets Windows .NET Framework; it is not the same runtime as `net8.0`. A Visual Studio retarget prompt changes project requirements, not just build configuration. Selecting Release does not resolve platform/API compatibility, and copying a Windows executable to Linux does not make it portable. Inspect framework, native dependencies and Windows APIs before choosing the build host or proposing a migration. See Microsoft's [runtime/platform distinction](https://learn.microsoft.com/en-us/dotnet/standard/choosing-core-framework-server).

Read the `.csproj`, imports, referenced projects and applicable `Directory.Build.props`/`.targets` before invoking build tools on unfamiliar material. MSBuild tasks, package build assets and compiler analyzers can execute during restore/build. Running an arbitrary project under privileged `dotnet` grants that build/application the same execution context. A build is not passive decompilation.

For `MSB3644`, retain the exact requested framework identifier/version and inspect the project's evaluated framework properties. This is a **reference-assembly** resolution failure, distinct from a runtime missing when launching an already built application. A newer installed .NET SDK does not supply every Windows .NET Framework targeting pack. Check the matching developer/targeting pack or the project's reviewed `Microsoft.NETFramework.ReferenceAssemblies` package requirement; missing packages/packs remain a prerequisite gap, not permission to install or retarget automatically. A malformed framework property can request a nonexistent framework, so resolve that before acquiring dependencies.

If an existing Linux build environment uses Mono reference assemblies, verify the actual assembly set against the requested framework. A copied `FrameworkPathOverride` directory can override normal resolution without establishing the right API contract; do not export a historical path into the whole session. Compilation against available assemblies does not supply Windows native database libraries, prove architecture compatibility or make that program runnable on Linux. A managed reference's `HintPath`, matching native dependencies and execution host remain separate decisions. See [MSB3644 diagnosis](https://learn.microsoft.com/en-us/visualstudio/msbuild/errors/msb3644?view=visualstudio).

For a reviewed fixture, define `project` as its absolute `.csproj` path, `configuration` as the chosen configuration and `framework` as an actual target from the project. Restore dependencies explicitly with the intended NuGet configuration when needed; `dotnet restore "$project"` can contact feeds and change caches/`obj`. After successful restore:

~~~bash
dotnet build "$project" --no-restore --configuration "$configuration" --framework "$framework" &&
dotnet run --project "$project" --no-build --configuration "$configuration" --framework "$framework" --no-launch-profile
~~~

`--no-build` also suppresses implicit restore; it can run stale output if build inputs/options differ. `--no-launch-profile` avoids unexpected settings from `launchSettings.json`. Put application arguments after `--`. A successful build does not establish successful application startup, listening, authentication or task completion. Conversely, an executable left in `bin/` after a failed build may be stale or belong to a project that finished before another target failed. Retain the build status, failed target and artifact identity; its presence is not a successful rebuild or a reason to run it.

For an existing framework-dependent application, `dotnet "$application_dll"` launches the actual assembly; `dotnet run` selects a project. Define the DLL path and retain its matching `.runtimeconfig.json`, `.deps.json`, dependencies and content where supplied. Missing framework, wrong architecture, absent native library and incomplete deployment are different failure classes. Not every managed DLL has an application entrypoint.

A PE-labelled managed DLL can be portable; native dependencies and platform-specific APIs can still prevent Linux execution. Preserve stderr/exit status and verify the intended application's observable result before changing target frameworks or rebuilding.

Resolve SDK/build differences with [dotnet environment](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet), [build](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build), [run](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run), [SDK selection](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json), [MSBuild execution boundaries](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-security-best-practices), [deployment](https://learn.microsoft.com/en-us/dotnet/core/deploying/).
