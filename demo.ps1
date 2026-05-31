# Mythosguard Demo Script
# Run this script from the project root directory

param(
    [int]$Rounds = 3,
    [int]$Seed = 42,
    [switch]$DryRun = $true,
    [switch]$ShowLogs = $false,
    [switch]$ShowStructure = $false,
    [switch]$Clean = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=== Mythosguard Demo ===" -ForegroundColor Cyan
Write-Host ""

# Show project structure if requested
if ($ShowStructure) {
    Write-Host "Project Structure:" -ForegroundColor Yellow
    Get-ChildItem -Recurse -File | Select-Object FullName, Length | Format-Table -AutoSize
    Write-Host ""
}

# Show vulnerable code
Write-Host "=== Target: sample_vulnerable_code\vuln.py ===" -ForegroundColor Yellow
Get-Content "sample_vulnerable_code\vuln.py"
Write-Host ""

# Clear logs if requested
if ($Clean) {
    Write-Host "=== Clearing Old Logs ===" -ForegroundColor Yellow
    if (Test-Path "logs\rounds.jsonl") {
        Remove-Item "logs\rounds.jsonl"
        Write-Host "Cleared: logs\rounds.jsonl" -ForegroundColor Green
    } else {
        Write-Host "No logs to clear" -ForegroundColor Gray
    }
    Write-Host ""
}

# Run the demo
Write-Host "=== Running Demo ($Rounds rounds, seed=$Seed) ===" -ForegroundColor Yellow
$providerArg = "--provider"
$providerSeedArg = "--provider-seed"
$dryRunArg = "--dry-run"
$noRichArg = "--no-rich"
$cleanArg = if ($Clean) { "--clean" } else { "" }

& python demo.py $dryRunArg $noRichArg $providerArg "mock" $providerSeedArg $Seed $cleanArg
Write-Host ""

# Show logs if requested
if ($ShowLogs) {
    Write-Host "=== Latest Round Log ===" -ForegroundColor Yellow
    $lastLog = Get-Content "logs\rounds.jsonl" | Select-Object -Last 1
    $lastLog | ConvertFrom-Json | ConvertTo-Json -Depth 10
    Write-Host ""
}

Write-Host "=== Demo Complete ===" -ForegroundColor Green
Write-Host "View full logs: type logs\rounds.jsonl"
Write-Host "Run again: .\demo.ps1 -Seed 123 -ShowLogs"
Write-Host "Clean logs: .\demo.ps1 -Clean"
