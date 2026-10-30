# Complete step-by-step guide — Azure Zero Trust DEV

**Author:** James Banday.

**Role:** ZT Engineer Lead, R0242994, based on the supplied job description.

**Last documentation review:** October 29, 2026, Hawaii time.

This guide adds a development implementation to the current `microsoft-zero-trust-rmf` repository. It uses Azure, Microsoft Entra, Intune, and Microsoft security services. The access exercise publishes a private IIS web application through Entra Application Proxy. It does not require an on-premises domain controller, identity synchronization, or the separate Entra Private Access product.

Repository files are implementation assets. They do not show that the user's tenant has been changed or that the tests have passed. Record each actual result in [the evidence package](04-validation-and-evidence.md).

## Build sequence

| Steps | Outcome |
|---|---|
| 1–6 | Confirm scope, licenses, costs, account recovery, groups, and Azure access. |
| 7–12 | Deploy private infrastructure, configure HTTPS, install a connector, and publish the app. |
| 13–16 | Establish device compliance, pilot access controls, managed identity, and endpoint protection. |
| 17–20 | Collect logs, build a detection, examine traffic, and deploy an audit policy. |
| 21–24 | Assess STIGs, test the architecture, operate the lab, and publish verified evidence. |

## Step 1 — Define the lab boundary and required licenses

1. Use a dedicated commercial Azure development subscription or a clearly isolated lab subscription and a Microsoft Entra test tenant that you control. Confirm the tenant directory associated with the subscription. Do not use an employer's or customer's tenant for this exercise.
2. Set the lab name to **Enterprise Zero Trust Architecture — DEV**. Use synthetic accounts, a static test application, and a demonstration secret without real business data.
3. Review [Figure 1 and the network plan](01-architecture.md). Confirm that `10.42.0.0/16` does not overlap any connected network. The templates use these fixed addresses; if you change them, update both templates, DNS, firewall rules, scripts, and test expectations together.
4. Confirm the following entitlements in the tenant. An Azure subscription alone does not supply all of them.

| Capability | Requirement to verify | If unavailable |
|---|---|---|
| Conditional Access, Application Proxy, and group-based app assignment | Appropriate Entra ID P1 or P2 licensing for participating users | Stop before these configuration steps; mark related tests BLOCKED. |
| Windows client management and compliance | Intune Plan 1 or a suite that includes the required features, assigned to test users | Do not enforce the compliant-device control. |
| Windows test client | Supported, licensed Windows 11 Pro, Enterprise, or Education; a TPM and Secure Boot capable device or VM | Prepare a supported client before enrollment. Windows Home is unsuitable for the intended Entra join path. |
| Time-limited directory or Azure privilege management | Applicable Entra ID P2 or ID Governance entitlement for PIM features | Keep the PIM exercise as a documented gap; use minimal scoped roles for the core lab. |
| Endpoint detection and device risk | Applicable Defender for Endpoint or Defender for Business entitlement and supported Intune integration | Record the feature actually available; do not claim unsupported risk or response features. |
| Protection of Windows Server VMs | Appropriate server coverage, such as a selected Defender for Servers plan | Client endpoint licensing does not automatically establish server coverage. |
| Log collection and Sentinel | Azure billing enabled; the required service and data-source permissions | Log Analytics is the starting point; Sentinel is an explicit paid extension. |

5. Record the tenant, subscription, license names, trial end dates, and lab owner in a private lab record. Do not publish this inventory with live account details.
6. For real DoD work, separately validate approved cloud environments, classification, required authorizations, and service availability. This commercial lab supports learning and selected control demonstrations.

**Completion check:** The boundary, owner, participating accounts, licensing decisions, and intended cleanup date are recorded.

## Step 2 — Estimate costs and prepare a spending plan

1. Open the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) and choose the intended region. `westus2` is the sample region; verify service availability, VM quota, and the current estimate before adopting it.
2. Estimate two Windows Server VMs, their managed disks, a Standard NAT Gateway, its Standard public IP, a Key Vault private endpoint, private DNS, Log Analytics ingestion and retention, and a dedicated Bastion Basic deployment. Add Sentinel, server security plans, VNet flow logging storage, and Traffic Analytics only if you will enable them.
3. Include per-user Microsoft licensing separately. Do not assume a trial, credit, or bundled license covers every service.
4. In Azure **Cost Management → Budgets**, create a lab budget at the subscription or dedicated resource group scope. Choose your own affordable amount and configure notifications at 50%, 80%, and 100%.
5. Record who reviews charges and when. A budget sends notifications; it does not stop resources automatically.
6. Reserve time to remove Bastion, NAT, and other paid resources after testing. Deallocating the VMs leaves disks, networking, logs, and other charges.

**Completion check:** You have reviewed the estimate and established a budget before deployment. The foundation template creates paid networking even before you deploy VMs.

## Step 3 — Open the integration files and prepare the tools

Use Bash in WSL or Azure Cloud Shell for commands marked `bash`. Use elevated Windows PowerShell on the named VM for commands marked `powershell`. Keep these environments separate.

1. Install Git, Python 3, VS Code, and the Azure CLI from their official sources if using WSL. Azure Cloud Shell already includes the Azure CLI. Use the current [Azure CLI installation guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Clone the integration branch, then open the repository. After the integration is merged, use `--branch main` instead; the same files will be available there.

```bash
git clone --branch feat/azure-zero-trust-dev-20261029 https://github.com/jbanday808/microsoft-zero-trust-rmf.git
cd microsoft-zero-trust-rmf
code .
```

**Command overview:** `git clone` downloads the repository; `--branch` chooses the integration branch. `cd` enters the project directory. `code .` opens that directory in VS Code; skip it in Cloud Shell.

3. Check the files locally. The checker has no third-party Python dependencies.

```bash
python3 zero-trust/azure-dev/scripts/check-package.py
```

**Command overview:** `python3` runs the package checker, which checks JSON, local links, and selected security settings without deploying anything.

4. Read [the architecture decision](decisions/001-azure-dev-boundary.md). Keep local IDs, logs, passwords, certificate files, and screenshots outside tracked content. The repository's ignore rules cover `private/`, local configuration, and common sensitive exports.

**Completion check:** The repository is open and the local package check succeeds. This is not Azure deployment validation.

## Step 4 — Prepare emergency access and administrator accounts

1. Check whether two usable emergency access accounts already exist in the test tenant. If they do not, create two cloud-only accounts using the tenant's `.onmicrosoft.com` domain.
2. Follow [Microsoft's emergency access guidance](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access). Use strong phishing-resistant authentication, such as separate FIDO2 security keys, and keep recovery independent of the normal administrator's device and sign-in dependencies.
3. Establish the required permanent active Global Administrator role for these recovery accounts and use them only for recovery and planned validation. Do not use them as daily administrators.
4. Verify both sign-ins from a secure workstation before changing access policies. Store recovery credentials securely and keep the two account object IDs in the private lab record.
5. Exclude both accounts from restrictive pilot Conditional Access policies. Exclusion from a custom policy does not remove Microsoft's service-level mandatory MFA requirements.
6. Use a separate normal administrator account for the build. Activate only the roles required for the task. For example, application work uses Application Administrator, compliance work uses Intune Administrator or an appropriate delegated role, and Conditional Access work uses Conditional Access Administrator.
7. Configure sign-in monitoring for every use of the emergency accounts in Step 18. Recheck their functionality at least every 90 days.

**Completion check:** Both recovery accounts work, their credentials are protected, and the build account is separate from them.

## Step 5 — Verify or complete the existing Entra groups

Your prior setup included `EZTA-DEV-Users` and `EZTA-DEV-Admins`, with `EZTA-DEV-App-Access` as the next group. Verify the current tenant before creating another object.

1. Open [Microsoft Entra admin center](https://entra.microsoft.com), confirm the selected tenant, and open **Entra ID → Groups → All groups**.
2. Search for each exact name below. Reuse the correct existing group. If duplicates exist, inspect ownership, members, and assignments before choosing; names are not unique identifiers.
3. For a missing group, choose **New group**, use **Security**, select **Assigned** membership, enter the name and description, select the lab administrator as owner, and create it.

| Group | Description | Intended members |
|---|---|---|
| `EZTA-DEV-Users` | Authorized Zero Trust development users. | Ordinary test users. |
| `EZTA-DEV-Admins` | Authorized Zero Trust development administrators. | Separate administrator identities. |
| `EZTA-DEV-App-Access` | Access to protected Zero Trust development applications. | Users authorized for the private app. |
| `EZTA-DEV-Pilot` | Pilot testing for Zero Trust access policies. | One or two ordinary test users initially. |
| `EZTA-DEV-Devices` | Test devices for Zero Trust endpoint policies. | Entra device objects, not user accounts. |

4. Keep **Microsoft Entra roles can be assigned to the group** set to **No** for these ordinary lab groups. Membership in `EZTA-DEV-Admins` grants no role by itself. You can assign this group scoped Azure resource permissions separately.
5. If a later exercise needs a directory role assigned through a group, create a separate role-assignable group through the appropriate privileged workflow. An existing ordinary group cannot simply have that property switched on later. Direct eligible role assignments are another licensed PIM option.
6. Create two ordinary test users: an authorized pilot and an unassigned negative-test user. Assign required licenses to both. Put the authorized pilot directly into `EZTA-DEV-Users`, `EZTA-DEV-App-Access`, and `EZTA-DEV-Pilot`. Keep the negative-test user outside the app access group.
7. Use direct user membership for the enterprise app assignment exercise. Do not rely on nested group membership to provide application access.
8. Record the five group object IDs privately. Capture sanitized group overview and membership evidence after review.

**Suggested screenshot:** `01_Entra_EZTA_DEV_Groups.png`.

**Completion check:** All five groups have the right object types and intended membership. You have not assumed that being an administrator group member supplies privilege.

## Step 6 — Sign in to Azure and prepare the resource group

1. Open the intended Bash environment and sign in. Replace the subscription placeholder with the actual subscription ID privately.

```bash
az login
az account set --subscription "REPLACE_WITH_LAB_SUBSCRIPTION_ID"
az account show --query '{subscription:name,tenant:tenantId}' --output table
```

**Command overview:** `az login` signs in. `az account set --subscription` selects the lab subscription. `az account show --query ... --output table` displays the selected subscription and tenant for review.

2. Confirm the selected tenant and subscription against the private lab record. Your deployment account needs resource deployment and network permissions in the lab resource group. Role assignment operations later require separate RBAC administration rights.
3. Define non-secret working values and create a dedicated resource group.

```bash
LAB_RG="rg-ezta-dev"
LAB_LOCATION="westus2"
LAB_DIR="zero-trust/azure-dev"
az group create --name "$LAB_RG" --location "$LAB_LOCATION" --tags Environment=DEV Project=EZTA Data=Synthetic
```

**Command overview:** The three variables store the lab group, region, and file directory. `az group create` creates the deployment boundary; `--tags` identifies the resources as a synthetic development lab.

4. If the resource group already existed, inspect its contents before continuing. Do not deploy these fixed VM and DNS names over another environment.

```bash
az resource list --resource-group "$LAB_RG" --output table
```

**Command overview:** `az resource list` displays the existing resources in the selected group so you can confirm the deployment scope.

5. If required providers are not registered, an authorized subscription administrator can register them. Sentinel needs its provider only when that extension is selected.

```bash
for LAB_PROVIDER in Microsoft.Network Microsoft.Compute Microsoft.KeyVault Microsoft.OperationalInsights Microsoft.Insights; do
  az provider register --namespace "$LAB_PROVIDER" --wait
done
```

**Command overview:** The loop registers each Azure service provider. `--namespace` selects the service and `--wait` waits for that registration to finish.

**Completion check:** The intended lab subscription is selected, the resource group is dedicated to this exercise, and required providers and VM quota are available.

## Step 7 — Validate and deploy the Azure foundation

1. Review `infra/azure-foundation.json` and its example parameters. Leave `enableSentinel` set to `false` for the foundation exercise.
2. The template creates a VNet with connector, application, private endpoint, and Bastion subnets; ASGs; NSGs; NAT and an egress public IP; private DNS; a private Key Vault; Log Analytics; and Key Vault audit diagnostics. It creates neither VM, Bastion, Entra policies, nor an Intune enrollment.
3. Validate the template against Azure, then preview the proposed changes.

```bash
az deployment group validate --resource-group "$LAB_RG" --template-file "$LAB_DIR/infra/azure-foundation.json" --parameters @"$LAB_DIR/infra/azure-foundation.parameters.example.json"
az deployment group what-if --resource-group "$LAB_RG" --template-file "$LAB_DIR/infra/azure-foundation.json" --parameters @"$LAB_DIR/infra/azure-foundation.parameters.example.json"
```

**Command overview:** `validate` asks Azure to check the deployment. `what-if` previews resource changes. `--template-file` identifies the configuration, and `--parameters @...` reads the non-secret parameter file.

4. Resolve validation errors and inspect the preview before creating resources. Confirm the scope and absence of changes to unrelated resources.
5. Deploy the reviewed foundation.

```bash
az deployment group create --name ezta-foundation --resource-group "$LAB_RG" --template-file "$LAB_DIR/infra/azure-foundation.json" --parameters @"$LAB_DIR/infra/azure-foundation.parameters.example.json"
az deployment group show --name ezta-foundation --resource-group "$LAB_RG" --query properties.outputs --output json
```

**Command overview:** `create` applies the foundation under the deployment name `ezta-foundation`. `show --query properties.outputs` displays its vault, workspace, and network output values.

6. In the Azure portal, verify the four subnet ranges. For the private endpoint subnet, confirm network policies are **Enabled** and the endpoint NSG is attached. Check that the vault connection is approved and the private DNS zone group is present.
7. Confirm Key Vault public network access is disabled, Azure RBAC is enabled, and purge protection is on. Purge protection means a deleted vault cannot be purged immediately; the template uses a seven-day soft-delete retention period.
8. Confirm the NAT Gateway is attached to the connector and application subnets. The VMs will have no public IP. The NAT egress IP is intentionally public and provides outbound connectivity without publishing inbound VM services.
9. Record the deployment result privately. A successful foundation deployment does not prove the application or policy controls work.

**Suggested screenshots:** `02_Azure_EZTA_DEV_Network.png` and `03_Azure_EZTA_DEV_KeyVault_PrivateEndpoint.png`.

**Completion check:** Azure reports a successful deployment and you have inspected the network, DNS, vault, and logging resources.

## Step 8 — Deploy the two private Windows Server VMs

1. Confirm the VM SKU quota and Windows Server image availability in your selected region. The sample uses `Standard_D2as_v5` and the Windows Server 2022 Azure Edition image. If the SKU is unavailable, choose a compatible size after checking cost and Trusted Launch support.
2. Validate the VM template in the same resource group. The CLI prompts for the missing `adminPassword` secure parameter; enter a strong lab-only password in the protected prompt. Do not place it in a command, tracked file, screenshot, or chat.

```bash
az deployment group validate --resource-group "$LAB_RG" --template-file "$LAB_DIR/infra/windows-lab.json" --parameters prefix=ezta-dev adminUsername=eztaadmin
az deployment group what-if --resource-group "$LAB_RG" --template-file "$LAB_DIR/infra/windows-lab.json" --parameters prefix=ezta-dev adminUsername=eztaadmin
```

**Command overview:** These commands validate and preview the private VM deployment. `prefix` must match the foundation; `adminUsername` supplies the local lab account. The password is requested through the secure parameter prompt.

3. Deploy after reviewing the preview. The password is requested again as needed.

```bash
az deployment group create --name ezta-windows --resource-group "$LAB_RG" --template-file "$LAB_DIR/infra/windows-lab.json" --parameters prefix=ezta-dev adminUsername=eztaadmin
```

**Command overview:** This command creates `ezta-conn01` and `ezta-app01`, their private NICs, and their OS disks. The application VM also receives a system-assigned managed identity.

4. Verify `ezta-conn01` has `10.42.10.10` and membership in `ezta-dev-conn-asg`. Verify `ezta-app01` has `10.42.20.10` and membership in `ezta-dev-app-asg`.
5. Confirm neither NIC has a public IP. Check Secure Boot, vTPM, boot diagnostics, and the application VM identity. Record the resolved image version, deployment timestamp, and actual VM size privately.

**Completion check:** Both VMs are running with private addresses, the intended ASG membership, and no public VM IPs.

## Step 9 — Configure controlled administration through Bastion

1. In Azure, open the lab VNet or VM and choose **Bastion**. Select manual configuration so you can review the SKU and resource group before deployment.
2. For the supplied network rules, select dedicated **Basic** Bastion, the same VNet, the existing `AzureBastionSubnet`, and a new Standard static public IP. Use `ezta-dev-bastion` as the name and place it in the lab resource group.
3. Review its cost and deploy it. Developer SKU uses a different access pattern and may need different source rules; do not substitute it without revising the design and tests.
4. Connect to each VM through Bastion using the lab local administrator account. No internet-facing RDP rule is needed on either VM.
5. Install Windows updates and reboot each VM as required. Confirm outbound web access works through NAT. Use separate Bastion sessions or reconnect as needed.
6. Review the effective inbound NSG rules. RDP is allowed from `10.42.40.0/26`, while other VNet-sourced inbound access is denied unless an earlier explicit rule allows it.

**Completion check:** You can administer both private VMs through Bastion and have not added public RDP access.

## Step 10 — Build the private HTTPS test application

1. In the Bastion session on **ezta-app01**, copy the reviewed repository script `scripts/configure-private-web-app.ps1` into `C:\EZTA\`. You can paste its text into a local PowerShell editor and compare it with the reviewed source. Never copy a private signing key between servers.
2. Open elevated Windows PowerShell and run the script on this dedicated lab VM.

```powershell
C:\EZTA\configure-private-web-app.ps1
```

**Command overview:** The script installs IIS, creates the synthetic HTTPS site, generates a short-lived lab certificate chain, stops the default site, and allows inbound web traffic only from the connector address in Windows Firewall. It exports only the public root certificate.

3. If execution is blocked, review the machine's execution policy and use your normal approved signed-script process or run the reviewed commands interactively. Do not disable tenant or organization controls to run a lab script.
4. Record the root certificate's SHA-256 file hash and the leaf certificate's expiry from the output. The leaf lasts 90 days and the lab root lasts 180 days.
5. Review IIS **Sites → EZTA-DEV → Bindings**. The site must listen on HTTPS port 443 for `app.ezta.internal`. The static page must contain only the demonstration text.
6. Transfer `C:\EZTA\EZTA-DEV-Lab-Root.cer` to the connector through an approved private method. For this isolated lab, you may base64-encode only the public `.cer`, copy the text through the two administrator sessions, and decode it on the connector. Verify the same SHA-256 hash after transfer. Do not expose a public file share or export a PFX.

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes('C:\EZTA\EZTA-DEV-Lab-Root.cer'))
```

**Command overview:** On the app VM, this prints a transportable text representation of the public certificate. It contains no private key; keep operational exports private anyway.

7. On **ezta-conn01**, create `C:\EZTA` and decode the copied text, replacing only the placeholder. Compare its hash with the source and import it into the machine trust store.

```powershell
New-Item -ItemType Directory -Path C:\EZTA -Force
[IO.File]::WriteAllBytes('C:\EZTA\EZTA-DEV-Lab-Root.cer', [Convert]::FromBase64String('PASTE_PUBLIC_CERTIFICATE_BASE64_HERE'))
Get-FileHash C:\EZTA\EZTA-DEV-Lab-Root.cer -Algorithm SHA256
Import-Certificate -FilePath C:\EZTA\EZTA-DEV-Lab-Root.cer -CertStoreLocation Cert:\LocalMachine\Root
Resolve-DnsName app.ezta.internal
Invoke-WebRequest https://app.ezta.internal/ -UseBasicParsing
```

**Command overview:** `New-Item` creates the directory. `WriteAllBytes` reconstructs the public certificate. `Get-FileHash` checks transfer integrity. `Import-Certificate` establishes lab trust. `Resolve-DnsName` checks private DNS. `Invoke-WebRequest` checks HTTPS without skipping certificate validation.

8. Expect DNS to resolve to `10.42.20.10` and the HTTPS response to succeed. If TLS fails, fix the trust chain, host name, clock, or certificate expiry. Do not bypass validation. A local test from the connector proves backend reachability, not user authorization through Entra.

**Completion check:** The connector can fetch the synthetic page over validated HTTPS. The lab root's private signing key stays on the app VM and is never published.

## Step 11 — Install the Microsoft Entra private network connector

1. On **ezta-conn01**, confirm Windows Server updates, .NET prerequisites, and TLS 1.2 using [the current connector prerequisites](https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-configure-connectors).
2. The supplied NSG permits outbound 80 and 443 through NAT. Confirm the Microsoft connector service destinations and DNS CNAME chains are reachable. Do not introduce TLS interception for the connector's cloud tunnel.
3. Follow the documented WinHTTP requirement for Application Proxy on Windows Server 2019 or later. In elevated PowerShell on the connector, set the documented value and restart during the lab maintenance window.

```powershell
$LabWinHttp = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\WinHttp'
if (-not (Test-Path $LabWinHttp)) { New-Item -Path $LabWinHttp -Force | Out-Null }
New-ItemProperty -Path $LabWinHttp -Name EnableDefaultHTTP2 -Value 0 -PropertyType DWord -Force
Restart-Computer
```

**Command overview:** `$LabWinHttp` identifies the WinHTTP registry path. `Test-Path` and `New-Item` ensure it exists. `New-ItemProperty` disables default HTTP/2 for this documented connector requirement. `Restart-Computer` applies the machine-wide change.

4. In Entra's **Enterprise applications → Application proxy**, download the current private network connector installer. Verify its Microsoft publisher signature and install it on `ezta-conn01` as administrator.
5. Register it with the intended tenant using the appropriate Application Administrator identity. Do not install it on the application VM or combine it with an incompatible password-protection proxy service.
6. Create the connector group **EZTA-DEV-Connectors** and move this connector into it. Confirm the connector reports **Active** and its updater service is running.
7. Recheck the HTTPS backend from the connector. One active connector is enough for this lab; a production resilience design normally needs at least two per group.

**Completion check:** The correct tenant shows the connector active in `EZTA-DEV-Connectors` and the backend remains reachable.

## Step 12 — Publish the application and restrict assignment

1. In Entra, create an on-premises enterprise application with Application Proxy, using these values.

| Setting | Value |
|---|---|
| Display name | `EZTA-DEV-Private-App` |
| Internal URL | `https://app.ezta.internal/` |
| External URL | Keep the generated HTTPS `msappproxy.net` URL. |
| Preauthentication | Microsoft Entra ID. |
| Connector group | `EZTA-DEV-Connectors`. |
| Validate Backend TLS Certificate | Enabled. |
| Backend single sign-on | Disabled for this static demonstration site. |

2. Save the application and inspect its properties. Set **Assignment required? → Yes** and enable user sign-in. Under **Users and groups**, assign `EZTA-DEV-App-Access` with the default access role.
3. Complete the explicit admin consent step for the app's Microsoft Graph delegated `User.Read` permission using an authorized consent administrator and Microsoft's current Application Proxy setup instructions. New apps created from June 30, 2026 no longer receive that consent automatically. Do not grant unrelated Graph permissions.
4. Record the application/client ID and the separate enterprise application object ID privately. The Conditional Access example uses the **application/client ID**, not the enterprise application object ID.
5. From the authorized pilot's browser, open the generated external URL and sign in. Before enforcement, confirm that application assignment works and the static page is reachable. Then sign out and repeat with the licensed unassigned user; that user should be refused application access.
6. Record both outcomes and matching sign-in records. A working authorized login is not yet evidence of a compliant-device requirement; that is configured in Steps 13–14.

**Suggested screenshot:** `04_Entra_EZTA_DEV_Private_App.png`.

**Completion check:** The assigned pilot reaches the app, the unassigned user is refused, backend TLS validation is enabled, and the required consent is recorded.

## Step 13 — Enroll a Windows 11 pilot device and establish compliance

1. Use a supported physical Windows 11 client or a Generation 2 test VM with a virtual TPM, Secure Boot, and suitable licensing. Do not use the two Windows Server VMs as the Intune compliance clients.
2. In Entra's mobility/Intune settings, confirm automatic MDM enrollment is configured for a selected pilot user scope. Check enrollment restrictions, enrollment permissions, and device limits before joining the test client.
3. On the Windows 11 client, open **Settings → Accounts → Access work or school → Connect → Join this device to Microsoft Entra ID**. Sign in as the licensed authorized pilot and complete the join and enrollment prompts.
4. Confirm the device appears in Entra and in Intune. Add the **device object** to `EZTA-DEV-Devices` using assigned membership. A user in that group is not a substitute for the device object.
5. In Intune, open **Devices → Compliance → Policies → Create policy**. Choose the current Windows platform and name the policy `EZTA-DEV-Windows-Compliance`.
6. Require supported settings such as Secure Boot, BitLocker/device encryption, an active firewall, antivirus, and an up-to-date supported OS baseline. Check each setting's hardware and edition support on the chosen client. Configure its noncompliance action and document any grace period.
7. Assign the policy to `EZTA-DEV-Devices` and synchronize the device. Compliance policies assess settings; use a separate configuration or endpoint security policy to turn on protections that are missing.
8. Review the tenant-level treatment of devices with no compliance policy. In the dedicated test tenant, select the intended strict handling after checking the effect on all enrolled devices. In a shared tenant, this is a separate tenant-wide change.
9. Wait for the client to report **Compliant** with recent check-in details. Confirm the intended policy, device identity, and user relationship. Do not enforce the next step while the only pilot device remains noncompliant or unknown.
10. Test with the work profile in Microsoft Edge on the joined client. Private browsing and unsupported browser/device combinations may not present the required device signal; verify the device ID in the sign-in record.

**Suggested screenshot:** `05_Intune_EZTA_DEV_Device_Compliance.png`.

**Completion check:** A real enrolled pilot client is compliant and can present its device identity during sign-in.

## Step 14 — Create, evaluate, and enforce the pilot Conditional Access policy

### Prerequisite when security defaults are enabled

In the dedicated test tenant, check **Entra ID → Properties → Manage security defaults** before starting the policy transition. Security defaults and a custom Conditional Access design require a planned transition. Register the users' authentication methods, test recovery, and prepare the replacement configuration first. Existing shared tenants need their own approved baseline change.

| Prepared baseline policy | User/resource scope | Intended control |
|---|---|---|
| `EZTA-DEV-BASE01-AllUsers-MFA` | All lab users and resources; exclude the two protected emergency accounts | Require the built-in multifactor authentication strength. |
| `EZTA-DEV-BASE02-Block-Legacy` | Same scope; client apps limited to Exchange ActiveSync and other legacy clients | Block access through the selected legacy clients. |
| `EZTA-DEV-BASE03-Block-DeviceCode` | Same scope; authentication flow limited to device code | Block device code authentication unless the documented lab requirements justify a separately reviewed exception. |

Use the current Microsoft baseline templates and security defaults transition guidance, review **What If** and any available report-only results, and inspect other managed policies. During the controlled transition, disable security defaults and activate the prepared replacement baseline immediately; verify normal administrator and pilot access and recheck emergency recovery. If the baseline cannot be established, restore the previous protection and defer the custom policy work. These examples are a starting baseline for this isolated lab, not a complete enterprise identity security design.

Continue with the application-specific pilot only after the tenant baseline is established. This transition must not leave the tenant with just an application-scoped MFA policy.

### Application-specific pilot

1. Verify both emergency accounts again. Confirm that the pilot has registered an allowed MFA method and can use the compliant device.
2. In Entra **Protection → Conditional Access → Policies**, create `EZTA-DEV-CA01-Pilot-App-MFA-Compliant` with the following scope.

| Setting | Value |
|---|---|
| Included users | `EZTA-DEV-Pilot` only. |
| Excluded users | Both emergency access accounts. |
| Target resource | `EZTA-DEV-Private-App` only. |
| Grant controls | Require MFA **and** require device to be marked compliant. |
| Multiple controls | Require all selected controls. |
| Initial policy state | Report-only. |

3. The versioned [Graph policy example](policy/ca-pilot-report-only.example.json) expresses this scope. Replace IDs only in a private copy. For API-based management, use Microsoft Graph's documented conditional access permissions and administrative consent; the example is not a one-command tenant deployment. Prefer the portal for the first lab policy.
4. Review **What If** for the authorized pilot, the unassigned test user, both emergency accounts, and the target app. A simulation helps evaluate scope; it does not replace actual sign-in tests.
5. Complete sign-ins from the compliant pilot device and from a separate unmanaged device or ordinary unsupported session. Inspect the policy's report-only results and the recorded device ID. Report-only logs a prospective decision; it does not enforce the block.
6. Review other existing policies and confirm the established tenant baseline. An app-scoped policy alone does not replace tenant-wide MFA, legacy authentication blocking, or the other protections previously supplied by security defaults.
7. Keep a normal administrator session open outside the test app scope. When the intended positive and negative results are understood, switch only this pilot policy from **Report-only** to **On**.
8. Repeat the actual app tests. The assigned pilot on a compliant device should be allowed after MFA requirements are met. The assigned pilot on an unmanaged device should be denied. The unassigned user should still be denied by app assignment.
9. Use a fresh supported browser session, sign out, or revoke the test user's sessions through the appropriate test workflow when needed to trigger a new evaluation. Record delays and existing session behavior instead of promising immediate revocation.
10. If the authorized pilot is unexpectedly blocked, return this policy to report-only or disabled using the retained administrator session. Diagnose the failure before expanding scope.

**Suggested screenshot:** `06_Entra_EZTA_DEV_CA_Pilot.png`.

**Completion check:** Actual enforced tests demonstrate both successful authorized access and denied unmanaged-device access, with matching sign-in evidence. Broader rollout is a separate change.

## Step 15 — Demonstrate private secret access with a managed identity

1. Retrieve the vault and application identity IDs from the deployment outputs. Run these control-plane commands in the same Bash session used for Azure deployment.

```bash
LAB_VAULT_ID=$(az deployment group show --resource-group "$LAB_RG" --name ezta-foundation --query properties.outputs.vaultId.value --output tsv)
LAB_VAULT_NAME=$(az deployment group show --resource-group "$LAB_RG" --name ezta-foundation --query properties.outputs.vaultName.value --output tsv)
LAB_APP_ID=$(az deployment group show --resource-group "$LAB_RG" --name ezta-windows --query properties.outputs.appPrincipalId.value --output tsv)
az role assignment create --assignee-object-id "$LAB_APP_ID" --assignee-principal-type ServicePrincipal --role "Key Vault Secrets User" --scope "$LAB_VAULT_ID"
```

**Command overview:** The first three commands read non-secret deployment outputs into task variables. `az role assignment create` gives the app VM's service identity read access to secret contents at this vault; it does not give write or administrator permission.

2. Your role-assignment account needs the appropriate RBAC administration permissions at the scope. A Contributor assignment alone is insufficient. Allow propagation time and inspect the actual assigned principal.
3. Give a designated lab administrator temporary **Key Vault Secrets Officer** access at this vault, using the appropriate authorized RBAC workflow. Record and later remove this temporary assignment.
4. The vault data plane is private and the endpoint NSG allows the app VM. From **ezta-app01**, use a supported browser inside the Bastion session to open the Azure portal, sign in as that designated administrator, open the vault's **Secrets**, and create a synthetic secret named `ezta-demo` with the value `synthetic-dev-value`. Signing in from the ordinary laptop or Cloud Shell does not provide the private network path to this vault.
5. On **ezta-app01**, use PowerShell to resolve the vault name and request a vault token from the VM's managed identity. Replace the vault-name placeholder only; do not paste a token into any file.

```powershell
$LabVaultName = 'REPLACE_WITH_DEPLOYED_VAULT_NAME'
Resolve-DnsName "$LabVaultName.vault.azure.net"
$LabToken = Invoke-RestMethod -Headers @{Metadata='true'} -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net'
$LabSecret = Invoke-RestMethod -Headers @{Authorization="Bearer $($LabToken.access_token)"} -Uri "https://$LabVaultName.vault.azure.net/secrets/ezta-demo?api-version=7.4"
$LabSecret.id
Remove-Variable LabToken, LabSecret
```

**Command overview:** `Resolve-DnsName` must show a private endpoint address in `10.42.30.0/24`. The first `Invoke-RestMethod` obtains a short-lived VM identity token. The second retrieves the demonstration secret. Printing only `.id` confirms the object without showing its value. `Remove-Variable` clears the token and response variables.

6. Test that the same managed identity cannot create a secret, using the negative test procedure in [validation](04-validation-and-evidence.md). A `403` with the expected authorization reason is useful evidence; a timeout is not proof of RBAC denial.
7. From **ezta-conn01**, confirm a new TCP connection to the vault endpoint on 443 is denied. Pair that result with effective rules or IP flow verification.
8. From a device outside the VNet, confirm vault data access cannot succeed through the public endpoint. Record the network reason rather than treating an authentication error as evidence of private networking.
9. Remove the temporary administrator Secrets Officer assignment when setup is complete. Keep the app identity's read-only assignment for the exercise.

**Completion check:** The app VM reads the synthetic secret through private networking, its identity cannot write, and the connector cannot connect directly to the vault. This does not mean the static IIS page is a secret-backed production application.

## Step 16 — Integrate endpoint protection and optional device risk

1. Confirm the purchased or trial endpoint protection feature set and its current prerequisites before enabling the integration. In the Defender portal, verify access to endpoint settings; in Intune, open the Microsoft Defender for Endpoint connector settings.
2. Enable the supported Intune and Defender connection using the required security and Intune administrative roles. Choose the enrolled Windows 11 client as the initial scope.
3. Create the supported endpoint detection and response onboarding policy, assign it to the test device group, synchronize the client, and confirm it appears in Defender's device inventory with recent health information.
4. Run only the harmless Microsoft-provided onboarding/detection validation procedure for that service. Record the alert, device, event timestamp, and analyst review. Do not assume a healthy agent proves all prevention capabilities.
5. If the available licenses support device-risk integration, add a separate pilot compliance requirement using the supported machine risk score, for example requiring low risk or below. Review its impact before enforcing it.
6. Do not intentionally infect the device to create a high-risk state. Document unsupported risk tests as blocked or use an approved service test method.
7. Server coverage is separate. If you enable a paid Defender for Servers plan, choose its scope and plan deliberately, verify both server onboarding results, and include the added charge in the budget. Do not label the servers protected solely because the Windows client is onboarded.

**Completion check:** You have verified the endpoint capabilities actually licensed and enabled, or have marked this extension blocked with a clear reason.

## Step 17 — Connect identity, Azure, vault, and endpoint logs

1. Confirm the deployed Log Analytics workspace. The foundation configures Key Vault `AuditEvent` diagnostics, but events arrive only after vault operations occur.
2. In Entra **Monitoring & health → Diagnostic settings**, create `EZTA-DEV-Entra-Logs`. Send **AuditLogs**, **SignInLogs**, and the available noninteractive sign-in category to `ezta-dev-law`. Use the required Security Administrator role and destination permissions; verify any license-dependent categories.
3. Repeat a pilot login and an app assignment or group change. Query the workspace for `SigninLogs` and `AuditLogs`. New diagnostic settings do not backfill an earlier history automatically.
4. In the Azure subscription's **Activity log → Export Activity Logs**, add a diagnostic setting sending the required categories, including administrative and policy events, to the same workspace. This subscription-level export is not created by the resource-group foundation template.
5. Verify `AzureActivity` after a benign lab management action. Keep this management activity distinct from Windows logon and application request logs.
6. After the secret read exercise, query `AzureDiagnostics` for Key Vault audit events. The supplied diagnostic setting uses this table; a separately configured resource-specific destination may instead use another documented table.
7. For Windows event collection, create a Windows **Data Collection Rule**, select the workspace, choose a small reviewed set of Windows Security/System/Application events, and associate the two servers. Use the current Azure Monitor Agent workflow. Do not treat enabling VM insights as equivalent to selecting Windows Security events.
8. If collecting Security events through Sentinel's Windows Security Events via AMA solution, follow that connector's DCR workflow and query `SecurityEvent`. Avoid duplicate collection of the same events through overlapping rules.
9. For IIS request logs, add a separate supported collection configuration if required. They are not collected by the foundation or by the static site script. Record its table and a real generated request before claiming application request monitoring.
10. Endpoint events remain in Defender unless the selected Sentinel/Defender integration is configured. Distinguish a Defender alert from a row in the Log Analytics workspace.

**Completion check:** Each claimed log source has a recent event, a known table, a retention setting, and an owner. Missing tables remain a collection gap.

## Step 18 — Create a detection and a response exercise

1. Start by running each separate query in [identity-and-secrets.kql](queries/identity-and-secrets.kql) in the intended workspace. Replace private object IDs in a local copy of the emergency-account query.
2. In Azure Monitor, create a scheduled log-search alert for any interactive or noninteractive emergency account sign-in. Use both real emergency user object IDs, a short lookback suitable for observed ingestion delay, and a threshold greater than zero. Configure a permitted notification destination you control. Test and review the event; do not publish the account IDs.
3. For the Sentinel extension, first register `Microsoft.SecurityInsights` and enable onboarding intentionally. You may use the current Sentinel onboarding interface for the existing workspace or redeploy the reviewed foundation with `enableSentinel=true`. Do not assume toggling the parameter back to false removes the existing service or stops its charges.
4. Prefer the Microsoft Defender portal for Sentinel operations. At the documentation review date, Microsoft's announced end of Sentinel support in the Azure portal is after March 31, 2027. Check current service guidance when you deploy.
5. Install the required Microsoft Entra solution from the Content hub if you use its Sentinel connectors or templates. Confirm the workspace's existing diagnostic collection before enabling overlapping connectors.
6. Create a scheduled analytics rule for failed sign-ins to the private app. In a private copy of the query, filter `AppId` to the actual app client ID, set a 15-minute lookback, group by user and app, and use a small lab threshold such as three failures. Run it every five minutes, map the account entity, and enable incident creation.
7. Generate the permitted failures through ordinary test sign-in attempts or expected policy denials. Record whether an incident actually appears, the ingestion delay, rule run result, and reason for any miss. A query that returns rows is not proof that an analytics rule is operating.
8. For an orchestration exercise, create an automation rule that tags the lab incident and assigns a triage task. If adding a Logic Apps playbook, use managed identity, only the required connector/API permissions, and an explicit analyst approval before any account disablement or device isolation. Verify permissions and connector authentication separately.
9. Perform a manual response drill: inspect the sign-in, verify the denied device or user, identify the app, choose an appropriate action, document the decision, and confirm recovery with the authorized pilot. Record containment timing only if it was actually measured.

**Completion check:** At least one benign test produces a real alert or incident and a reviewed response record, or the missing capability is recorded as a gap.

## Step 19 — Verify segmentation and collect network flow evidence

1. Copy `scripts/Test-EztaNetwork.ps1` to each VM. Run the checks from the named source, replacing the vault placeholder.

```powershell
# On ezta-conn01
C:\EZTA\Test-EztaNetwork.ps1 -Role Connector -VaultName 'REPLACE_WITH_DEPLOYED_VAULT_NAME'
# On ezta-app01
C:\EZTA\Test-EztaNetwork.ps1 -Role Application -VaultName 'REPLACE_WITH_DEPLOYED_VAULT_NAME'
```

**Command overview:** `-Role` selects tests appropriate to the source VM. `-VaultName` identifies the private vault. The script reports expected and actual TCP reachability as JSON and exits with an error if any checked result differs.

2. Expect connector-to-app 443 and app-to-vault 443 to work. Expect connector-to-app 3389 and 80, connector-to-vault 443, and app-to-connector 3389 to fail.
3. A stopped service can also cause a failed TCP test. For the denied paths, use **Network Watcher → IP flow verify** on the source/destination VM NIC with the matching IPs, protocol, direction, and port. Record the named effective deny rule. For the private endpoint path, inspect its enabled network policies and endpoint subnet NSG as well.
4. Review both NICs' effective rules and ASG membership. Default NSG VNet allow rules must be overridden by the earlier explicit deny rules. Merely creating separate subnets is insufficient evidence of segmentation.
5. For retained traffic evidence, use **Network Watcher → Flow logs → Create**, select the lab **virtual network** as the target, and select a supported storage account and retention period in the appropriate region/subscription. Add that storage cost to the budget.
6. Follow the current VNet flow log permissions, storage restrictions, and Traffic Analytics requirements. If enabled, point Traffic Analytics to the intended workspace and record the actual table and processing delay.
7. Generate the test flows again and inspect the matching addresses, ports, and timestamps. Not all platform or private endpoint traffic is represented identically; document observed coverage rather than claiming that every transaction was collected.
8. Use **VNet flow logs** for this new deployment. Do not base the lab on creating new NSG flow logs; Microsoft has announced their retirement and has directed new implementations to VNet flow logging.

**Suggested screenshot:** `07_Azure_EZTA_DEV_Segmentation_Test.png`.

**Completion check:** Every required allowed/denied path has a source-specific result and supporting enforcement evidence. Flow logging has separate verified evidence if you claim it.

## Step 20 — Add an Azure Policy example in audit mode

1. Review [key-vault-public-access.policy.json](policy/key-vault-public-access.policy.json). It defines a custom policy that detects Key Vaults whose public network access is not disabled. Its default effect is **Audit**.
2. The definition is subscription-scoped; the assignment below is restricted to the lab resource group. Use an account permitted to create definitions and assignments, such as an appropriately scoped Resource Policy Contributor. This does not require making the app identity a policy administrator.

```bash
LAB_SUB_ID=$(az account show --query id --output tsv)
LAB_POLICY_URL="https://management.azure.com/subscriptions/$LAB_SUB_ID/providers/Microsoft.Authorization/policyDefinitions/ezta-dev-vault-private?api-version=2023-04-01"
az rest --method put --url "$LAB_POLICY_URL" --body @"$LAB_DIR/policy/key-vault-public-access.policy.json"
az policy assignment create --name ezta-dev-vault-audit --scope "/subscriptions/$LAB_SUB_ID/resourceGroups/$LAB_RG" --policy "/subscriptions/$LAB_SUB_ID/providers/Microsoft.Authorization/policyDefinitions/ezta-dev-vault-private"
```

**Command overview:** `az account show` reads the selected subscription ID. `az rest --method put --body @...` creates the reviewed custom definition from the file. `az policy assignment create --scope` applies its default audit effect only to the lab group.

3. Trigger a resource-group compliance evaluation and review the resulting policy state when it completes.

```bash
az policy state trigger-scan --resource-group "$LAB_RG"
az policy state list --resource-group "$LAB_RG" --query "[?policyAssignmentName=='ezta-dev-vault-audit'].{resource:resourceId,state:complianceState}" --output table
```

**Command overview:** `trigger-scan` requests a new evaluation. `policy state list` displays the relevant assignment's compliance records; results may take time to appear.

4. The intended vault should evaluate compliant. For a negative policy test, use an isolated disposable vault with public access enabled, no secrets, and no access grants, then verify a noncompliant audit result and delete it. Do not weaken the protected lab vault to produce a screenshot.
5. Audit reports a configuration; it does not block a deployment. Moving to **Deny** requires a separate reviewed change and a safe disposable-resource denial test. Document this distinction in the evidence register.

**Completion check:** The assignment evaluates the actual vault, the effect is recorded as audit, and any negative test uses a disposable resource.

## Step 21 — Assess STIG settings and connect evidence to RMF

1. Read the existing [STIG governance and implementation guide](../../compliance/10-disa-stig-governance-and-implementation.md) and [RMF overview](../../rmf/04-rmf-for-leaders.md).
2. From the current official DISA distribution site, obtain the applicable Windows Server, IIS, Windows client, and other relevant STIG/SRG materials. Record the exact title, release/version, download date, and asset applicability. Use only publicly releasable materials for this portfolio.
3. Use the current supported STIG Viewer/checklist workflow and the approved assessment method for each applicable benchmark. Automated tools cover only supported checks; review manual items separately.
4. Inventory the VM or client, create a baseline checklist, and capture the initial finding states before making changes. Do not mark a requirement not applicable merely because it is inconvenient in a lab.
5. Choose a small supported hardening change, such as verifying firewall policy or an applicable audit setting. Record the vulnerability/rule ID from the actual benchmark, the original value, implementation instructions, dependencies, rollback, and post-change result. Do not invent STIG IDs.
6. Test changes on a snapshot or disposable clone where possible. Protect connector functionality, certificate trust, updates, agent communication, and administrative recovery. Retest affected access and log paths after hardening.
7. Use [the candidate DoD/RMF matrix](03-dod-rmf-role-alignment.md) to connect the implementation to control objectives. For each control, record the implementation statement, boundary, owner, evidence location, test date, outcome, and unresolved findings.
8. Create a POA&M entry for missing or failed requirements with the risk, responsible owner, planned action, target date, and retest. Do not copy simulated results from the existing executive eMASS section into the live lab's result column.
9. Treat **Prepare, Categorize, Select, Implement, Assess, Authorize, and Monitor** as separate RMF activities. An educational mapping does not complete an authorization decision.

**Completion check:** The package distinguishes assessed controls, failed controls, blocked checks, and candidate mappings. No full DoD Target Level or ATO claim is made.

## Step 22 — Execute the complete acceptance tests

1. Copy [test-results.json](evidence/templates/test-results.json) into an ignored private working directory. Leave the tracked original unchanged as a clean template.
2. Execute the cases in [the validation plan](04-validation-and-evidence.md). For every case, record the actual outcome, UTC timestamp, relevant log record or rule, private evidence location, and reviewer.
3. Run both allowed and denied application cases after enforcement. Run the identity, network, managed identity, logging, policy, and rollback cases from the correct source devices.
4. Use **PASS** only when the observed result matches the expectation and supporting evidence exists. Use **FAIL** for a mismatch, **BLOCKED** for missing prerequisites, and **NOT RUN** for an unexecuted test.
5. Perform a rollback drill by returning the pilot policy to report-only and verifying recovery, then restore the intended pilot state and retest. Preserve the active normal administrator session and recovery accounts.
6. Record whether a connector outage prevents access and what restores service. A single connector outage test demonstrates the current availability limitation, not high availability.
7. Close critical access-control failures before describing the lab as functioning. Keep residual gaps visible in the private evidence record and sanitized public status summary.

**Completion check:** Every acceptance test has an honest final state. Passing source-file checks alone cannot pass tenant or network acceptance tests.

## Step 23 — Establish maintenance, measures, and cleanup

1. Follow [operations and rollback](05-operations-and-rollback.md) for daily health, weekly patching and log review, monthly access review, and recovery drills.
2. Track the percentage of tested accounts protected by the pilot policy, compliant pilot devices, required sources producing recent events, tested denied network paths, unresolved findings, and measured response time where available. Keep a defined numerator, denominator, owner, and measurement window for each metric.
3. For a leader's review, show the mission or business risk, the implemented protection, the actual test evidence, the remaining gap, the owner, and the next decision. Avoid using product installation counts as the only measure of success.
4. Stop and deallocate the lab VMs between sessions if retaining the environment, while accounting for continuing networking and storage charges. When the exercise is finished, follow the staged cleanup steps and verify remaining resources and external tenant objects.
5. Preserve private evidence before deletion and retain the documented results. Remove unused enterprise app access, connector registrations, temporary RBAC grants, and test assignments using the scope checks in the cleanup guide.

**Completion check:** Health ownership, cost ownership, review dates, unresolved risks, and cleanup responsibilities are assigned.

## Step 24 — Publish only the reviewed implementation and evidence

1. Keep the architecture, guide, templates, policy examples, query logic, and empty evidence templates in this repository. Keep operational secrets and raw evidence private.
2. Before adding evidence, inspect screenshots for usernames, tenant domains, public or private addresses, subscription and object IDs, tokens, license details, personal data, and browser information. Redact as needed for the public portfolio. A configuration screenshot alone must not be labeled as a successful access test.
3. Use concise captions. For example: **Figure 3. The pilot policy requires MFA and a compliant device before the assigned user can access the private application.** Use that wording only with the actual enforced policy and matching test results.
4. Run the package checker again and inspect the exact files being committed.

```bash
python3 zero-trust/azure-dev/scripts/check-package.py
git status --short
git diff --check
git diff --stat
```

**Command overview:** The Python checker reviews package consistency. `git status --short` lists changed files. `git diff --check` finds whitespace errors. `git diff --stat` summarizes the change size. Review untracked files separately before adding them.

5. Create a separate evidence branch, add only reviewed public files by exact path, and inspect the staged changes before committing. Do not use a blanket add command for a working directory containing raw evidence.

```bash
git switch -c docs/azure-dev-verified-evidence
git add zero-trust/azure-dev/evidence/README.md
git diff --cached
git commit -m "Document verified Azure Zero Trust DEV results"
git push -u origin docs/azure-dev-verified-evidence
```

**Command overview:** `git switch -c` creates a branch. `git add` stages the specified reviewed file; add any separately reviewed sanitized evidence by its exact path. `git diff --cached` displays the staged content. `git commit` records it. `git push -u` publishes the branch and establishes its upstream.

6. Open a pull request explaining what was deployed, what was tested, what passed or failed, and which material gaps remain. Keep interview or portfolio claims limited to work actually completed and verified.

**Completion check:** A reviewer can follow the design, reproduce the build, inspect truthful test outcomes, and understand the remaining limitations.

## References

See [References and descriptions](06-references.md) for the primary-source guidance behind the implementation and the current product requirements.
