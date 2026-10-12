param([Parameter(Mandatory)][string]$SourcePath)

$ErrorActionPreference = 'Stop'
try {
    $sourceItem = Get-Item -LiteralPath $SourcePath
    if ($sourceItem.PSIsContainer) { throw 'Select one source file, not a directory.' }
    $sourceTokens = $null
    $sourceErrors = $null
    $sourceAst = [System.Management.Automation.Language.Parser]::ParseFile(
        $sourceItem.FullName, [ref]$sourceTokens, [ref]$sourceErrors)
    $sourceNodes = @($sourceAst.FindAll({ param($node)
        $node -is [System.Management.Automation.Language.CommandAst] -or
        $node -is [System.Management.Automation.Language.FunctionDefinitionAst]
    }, $true) | ForEach-Object {
        $nodeName = if ($_ -is [System.Management.Automation.Language.CommandAst]) {
            $_.GetCommandName()
        } else { $_.Name }
        [pscustomobject]@{ line = $_.Extent.StartLineNumber
            kind = $_.GetType().Name; name = $nodeName }
    })
    $sourceDiagnostics = @($sourceErrors | ForEach-Object {
        [pscustomobject]@{ line = $_.Extent.StartLineNumber
            id = $_.ErrorId; message = $_.Message }
    })
    [pscustomobject]@{ file = $sourceItem.FullName
        parserVersion = $PSVersionTable.PSVersion.ToString()
        nodes = $sourceNodes; errors = $sourceDiagnostics } | ConvertTo-Json -Depth 5
    if ($sourceDiagnostics.Count) { exit 1 }
} catch {
    Write-Error -Message $_.Exception.Message -ErrorAction Continue
    exit 2
}
