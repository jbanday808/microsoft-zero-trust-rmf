#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Connector', 'Application')]
    [string]$Role,
    [string]$VaultName
)

$ErrorActionPreference = 'Stop'
$checks = @()
function Add-NetworkCheck {
    param([string]$Name, [string]$Target, [int]$Port, [bool]$Expected)
    $actual = [bool](Test-NetConnection -ComputerName $Target -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue)
    $script:checks += [pscustomobject]@{
        Test = $Name; Target = $Target; Port = $Port; ExpectedReachable = $Expected
        ActualReachable = $actual; Passed = ($actual -eq $Expected)
        TimeUtc = [DateTime]::UtcNow.ToString('o')
    }
}

if ($Role -eq 'Connector') {
    # A denied port alone cannot distinguish an NSG deny from a stopped service.
    # Pair negative results with Network Watcher IP flow verification.
    Add-NetworkCheck 'NET-01 App HTTPS allowed' 'app.ezta.internal' 443 $true
    Add-NetworkCheck 'NET-02 App RDP denied' '10.42.20.10' 3389 $false
    Add-NetworkCheck 'NET-03 App HTTP denied' '10.42.20.10' 80 $false
    if ($VaultName) {
        Add-NetworkCheck 'NET-04 Connector vault denied' "$VaultName.vault.azure.net" 443 $false
    }
} else {
    if (-not $VaultName) { throw 'Application checks require -VaultName.' }
    Add-NetworkCheck 'NET-05 App vault HTTPS allowed' "$VaultName.vault.azure.net" 443 $true
    Add-NetworkCheck 'NET-06 App connector RDP denied' '10.42.10.10' 3389 $false
}

$checks | ConvertTo-Json -Depth 4
if (@($checks | Where-Object { -not $_.Passed }).Count -gt 0) { exit 1 }
