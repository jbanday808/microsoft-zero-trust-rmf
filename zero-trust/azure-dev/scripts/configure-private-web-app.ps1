#Requires -RunAsAdministrator
#Requires -Version 5.1
<#
Creates an isolated DEV HTTPS site and exports only a public lab root certificate.
Run on the dedicated ezta-app01 VM, not on a shared IIS server.
#>
[CmdletBinding()]
param(
    [string]$DnsName = 'app.ezta.internal',
    [string]$ConnectorAddress = '10.42.10.10',
    [string]$RootCertificatePath = 'C:\EZTA\EZTA-DEV-Lab-Root.cer'
)

$ErrorActionPreference = 'Stop'
Import-Module ServerManager
$null = Install-WindowsFeature Web-Server -IncludeManagementTools
Import-Module WebAdministration

if (Test-Path 'IIS:\Sites\EZTA-DEV') {
    throw 'EZTA-DEV already exists. Inspect its bindings and certificate before making another change.'
}

$outDir = Split-Path -Parent $RootCertificatePath
$null = New-Item -ItemType Directory -Path $outDir -Force
$webRoot = 'C:\inetpub\ezta-dev'
$null = New-Item -ItemType Directory -Path $webRoot -Force

$root = New-SelfSignedCertificate -Type Custom -Subject 'CN=EZTA DEV Lab Root' `
    -KeyAlgorithm RSA -KeyLength 3072 -HashAlgorithm SHA256 `
    -KeyUsage CertSign, CRLSign, DigitalSignature `
    -TextExtension @('2.5.29.19={critical}{text}ca=1&pathlength=0') `
    -CertStoreLocation 'Cert:\LocalMachine\My' -KeyExportPolicy NonExportable `
    -NotAfter (Get-Date).AddDays(180)

$leaf = New-SelfSignedCertificate -Type Custom -DnsName $DnsName -Subject "CN=$DnsName" `
    -Signer $root -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 `
    -KeyUsage DigitalSignature, KeyEncipherment `
    -TextExtension @('2.5.29.37={text}1.3.6.1.5.5.7.3.1') `
    -CertStoreLocation 'Cert:\LocalMachine\My' -KeyExportPolicy NonExportable `
    -NotAfter (Get-Date).AddDays(90)

$null = Export-Certificate -Cert $root -FilePath $RootCertificatePath
$null = Import-Certificate -FilePath $RootCertificatePath -CertStoreLocation 'Cert:\LocalMachine\Root'

@'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>EZTA DEV</title></head>
<body><h1>EZTA DEV — Protected Application</h1>
<p>This page contains synthetic demonstration data only.</p>
<p>Record the access result together with the Entra sign-in log.</p></body></html>
'@ | Set-Content -Path (Join-Path $webRoot 'index.html') -Encoding UTF8

if (Test-Path 'IIS:\Sites\Default Web Site') {
    Stop-Website -Name 'Default Web Site'
}
$null = New-Website -Name 'EZTA-DEV' -PhysicalPath $webRoot -IPAddress '*' -Port 443 -HostHeader $DnsName -Ssl
Get-WebBinding -Name 'EZTA-DEV' -Protocol https | ForEach-Object {
    $_.AddSslCertificate($leaf.Thumbprint, 'My')
}

# The dedicated lab permits backend HTTPS only from the connector address.
# Effective NSG rules provide the independent network boundary.
Get-NetFirewallRule -Name 'IIS-WebServerRole-HTTP-In-TCP', 'IIS-WebServerRole-HTTPS-In-TCP' -ErrorAction SilentlyContinue |
    Disable-NetFirewallRule
if (-not (Get-NetFirewallRule -Name 'EZTA-DEV-HTTPS-Connector' -ErrorAction SilentlyContinue)) {
    $null = New-NetFirewallRule -Name 'EZTA-DEV-HTTPS-Connector' -DisplayName 'EZTA DEV HTTPS from connector' `
        -Direction Inbound -Action Allow -Protocol TCP -LocalPort 443 -RemoteAddress $ConnectorAddress -Profile Any
}

Write-Output ('Site URL: https://{0}/' -f $DnsName)
Write-Output ('Public root certificate: {0}' -f $RootCertificatePath)
Write-Output ('Root certificate SHA256: {0}' -f (Get-FileHash -Path $RootCertificatePath -Algorithm SHA256).Hash)
Write-Output ('Leaf certificate expires: {0:u}' -f $leaf.NotAfter)
Write-Output 'Import the public root into LocalMachine\Root on the connector and test HTTPS without bypassing validation.'
Write-Output 'This script configures the server; it does not verify Entra access or claim a successful deployment.'
