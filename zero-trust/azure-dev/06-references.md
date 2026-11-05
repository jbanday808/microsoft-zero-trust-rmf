# References

Primary sources reviewed for the October 29, 2026 documentation. Product interfaces, prerequisites, licensing, and service transitions can change; check the linked guidance again before deployment. Repository implementation choices and proposed control mappings remain the author's lab design.

## Zero Trust, DoD, and RMF

- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final): This publication explains Zero Trust principles and the roles of access decisions and enforcement.
- [DoD Zero Trust Strategy](https://dodcio.defense.gov/Portals/0/Documents/Library/DoD-ZTStrategy.pdf): This strategy defines the seven pillars and target/advanced capability structure used for the educational crosswalk.
- [DoD Zero Trust Reference Architecture, Version 2.0](https://dodcio.defense.gov/Portals/0/Documents/Library/%28U%29ZT_RA_v2.0%28U%29_Sep22.pdf): This public reference describes architectural principles and relationships; confirm the version adopted by a real program.
- [Configure Microsoft cloud services for the DoD Zero Trust Strategy](https://learn.microsoft.com/en-us/security/zero-trust/dod-zero-trust-strategy-intro): This guide maps Microsoft capabilities to DoD activities and distinguishes selected implementations from full target-level completion.
- [NIST SP 800-37 Rev. 2 — Risk Management Framework](https://csrc.nist.gov/pubs/sp/800/37/r2/final): This publication describes the seven RMF activities and authorization responsibilities.
- [NIST SP 800-53 Rev. 5 — Security and Privacy Controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final): This catalog provides the candidate control references used in the evidence mapping.
- [DISA STIG downloads](https://public.cyber.mil/stigs/downloads/): This official distribution entry provides applicable hardening materials; select the current benchmark release and record its version rather than assuming lab compliance.

## Identity, application access, and device compliance

- [Conditional Access overview](https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview): This guide explains policy signals, access controls, and licensing requirements.
- [Security defaults](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults): This guide explains the default identity protections and considerations when moving to Conditional Access.
- [Require MFA for all users](https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-mfa-strength): This guide explains the baseline authentication-strength policy that complements the app pilot.
- [Block legacy authentication](https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-block-legacy-authentication): This guide explains scoping and testing a legacy-client block policy.
- [Emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access): This guide explains recovery accounts, strong authentication, exclusions, monitoring, and regular validation.
- [Add an application through Application Proxy](https://learn.microsoft.com/en-us/entra/identity/app-proxy/application-proxy-add-on-premises-application): This guide covers app publishing, preauthentication, backend TLS validation, and the explicit consent requirement for new apps from June 30, 2026.
- [Configure private network connectors](https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-configure-connectors): This guide provides Windows, TLS, WinHTTP, and network prerequisites for Application Proxy and Private Access connectors.
- [Private network connector concepts](https://learn.microsoft.com/en-us/entra/global-secure-access/concept-connectors): This guide explains outbound connectivity, connector groups, and availability planning.
- [Application Proxy security considerations](https://learn.microsoft.com/en-us/entra/identity/app-proxy/application-proxy-security): This guide explains the connector's outbound TLS communication model.
- [Require device compliance with Conditional Access](https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-device-compliance): This guide explains using an established Intune compliance policy as an access requirement.
- [Windows compliance settings in Intune](https://learn.microsoft.com/en-us/intune/device-security/compliance/ref-windows-settings): This guide describes supported compliance checks and their platform dependencies.
- [Privileged Identity Management overview](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure): This guide explains eligible, time-limited privileged access and the applicable licensing model.
- [Assign Azure roles through PIM](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-resource-roles-assign-roles): This guide explains selecting the resource scope and making an administrator eligible for a resource role.

## Azure infrastructure and data protection

- [Azure CLI installation](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli): This guide provides supported installation routes for the command-line tool used in deployment examples.
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/): This calculator estimates current regional infrastructure costs before the lab is deployed.
- [Default outbound access in Azure](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access): This guide explains private subnets and why the design supplies an explicit outbound method.
- [Azure NAT Gateway design](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-gateway-design): This guide explains NAT egress behavior and its relationship to subnet routing.
- [Private endpoint network policies](https://learn.microsoft.com/en-us/azure/private-link/disable-private-endpoint-network-policy): This guide explains enabling NSG and routing policies for private endpoint subnets.
- [Deploy Azure Bastion](https://learn.microsoft.com/en-us/azure/bastion/quickstart-host-portal): This guide explains Bastion setup, private VM administration, SKU choices, and billing behavior.
- [Virtual network ARM reference, 2024-05-01](https://learn.microsoft.com/en-us/azure/templates/microsoft.network/2024-05-01/virtualnetworks): This reference describes the network resource schema used by the foundation template.
- [Key Vault ARM reference, 2023-07-01](https://learn.microsoft.com/en-us/azure/templates/microsoft.keyvault/2023-07-01/vaults): This reference describes the vault's RBAC, private networking, and retention settings.
- [Windows VM ARM reference, 2024-03-01](https://learn.microsoft.com/en-us/azure/templates/microsoft.compute/2024-03-01/virtualmachines): This reference describes the virtual machine and security configuration used in the lab template.
- [Use a VM managed identity to obtain a token](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token): This guide explains the metadata endpoint and short-lived resource tokens.
- [Key Vault RBAC guide](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide): This guide explains data-plane permissions and the roles used for separate read and administrative tasks.
- [Get Azure Policy compliance data](https://learn.microsoft.com/en-us/azure/governance/policy/how-to/get-compliance-data): This guide explains compliance evaluation and querying policy state.

## Monitoring and endpoint security

- [Entra diagnostic settings](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-configure-diagnostic-settings): This guide explains sending sign-in and audit activity to a selected destination.
- [Log Analytics ARM reference, 2023-09-01](https://learn.microsoft.com/en-us/azure/templates/microsoft.operationalinsights/2023-09-01/workspaces): This reference describes workspace retention, authentication, and network settings.
- [Collect VM logs with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection): This guide explains Azure Monitor Agent and Data Collection Rule configuration.
- [Onboard Windows clients through Intune](https://learn.microsoft.com/en-us/defender-endpoint/configure-endpoints-mdm): This guide explains supported Defender for Endpoint onboarding through Intune.
- [Choose a Defender for Servers plan](https://learn.microsoft.com/en-us/azure/defender-for-cloud/plan-defender-for-servers-select-plan): This guide explains server coverage and the plan choices that need separate cost and capability review.
- [Manage VNet flow logs](https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-manage): This guide explains creating and inspecting virtual network traffic records.
- [NSG flow log retirement guidance](https://learn.microsoft.com/en-us/azure/network-watcher/nsg-flow-logs-overview): This guide explains the retirement of NSG flow logs and the move to VNet flow logging.
- [Microsoft Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal): This guide explains the current Sentinel interface and the announced Azure portal support transition.
- [Sentinel onboarding ARM reference, 2024-03-01](https://learn.microsoft.com/en-us/azure/templates/microsoft.securityinsights/2024-03-01/onboardingstates): This reference describes the optional workspace onboarding resource used by the template.

## Role source

The role alignment uses the ZT Engineer Lead description for requisition **R0242994** supplied with this request. It is not a verification of current opening status, eligibility, clearance, or the user's professional experience.
