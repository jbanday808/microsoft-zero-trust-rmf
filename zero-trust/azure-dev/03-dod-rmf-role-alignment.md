# DoD, RMF, and ZT Engineer Lead alignment

## Assessment boundary

This matrix maps selected lab activities to public Zero Trust capability areas. It is an educational crosswalk, not an assessment that all DoD Target Level activities are complete. Microsoft's public DoD guide describes 45 capabilities and 152 activities, including 92 target and 60 advanced activities. A small lab addresses only a subset and cannot establish enterprise-wide completion.

Use the current public DoD strategy, reference architecture, and activity execution guidance when building an actual program plan. Record the exact adopted versions. Product availability in a commercial tenant does not establish approval for a government or classified deployment.

## Seven-pillar crosswalk

Capability numbers below follow the public DoD Zero Trust Strategy's capability model. They are capability references, not claims that each related activity has been satisfied.

| DoD pillar | Selected capability areas | Lab implementation | Required evidence | Remaining scope |
|---|---|---|---|---|
| User | 1.1 inventory; 1.2 conditional access; 1.3 MFA; 1.4 privileged access; 1.7 least privilege | Entra inventory, direct app assignment, pilot MFA and compliance policy, scoped RBAC, optional licensed PIM | User/group inventory, allowed and denied sign-ins, role assignments and activations | Enterprise federation, non-person entities, continuous authentication, and full access lifecycle remain broader work. |
| Device | 2.1 inventory; 2.2 compliance; 2.6 management; 2.7 EDR/XDR | Windows 11 enrollment, device group, Intune compliance, optional licensed endpoint integration | Device check-in, compliance detail, health record, detection validation | Servers need separate coverage; the lab does not inventory every enterprise device type. |
| Application & Workload | 3.1 inventory; 3.2 secure development/integration; 3.4 resource authorization | Named private app, reviewed repository change, app assignment, managed identity | Application record, code review, app access tests, identity-based secret read | No full business application, API authorization model, software supply-chain program, or continuous authorization. |
| Data | 4.5 encryption/rights management; 4.7 access control; later 4.3 labeling and 4.6 DLP | HTTPS backend, private encrypted vault service, RBAC, synthetic-data scope; optional separate Purview exercise | Certificate checks, secret read/write results, data handling record | A vault secret exercise does not implement enterprise data discovery, rights management, labeling, or DLP. |
| Network & Environment | 5.1 data-flow mapping; 5.3 macro segmentation; 5.4 micro segmentation | Flow diagram, separate subnets, ASG-scoped application path, explicit default-VNet overrides, private endpoint | Allowed and denied flow tests, effective NSG rules, network-policy configuration | This demonstrates selected segmentation controls, not a complete enterprise microsegmentation program. Egress domain restrictions remain a gap. |
| Automation & Orchestration | 6.1 policy decisions/orchestration; 6.2 process automation; 6.5 SOAR; 6.7 SOC/IR | Versioned templates and policy example, scripted checks, optional incident tagging/playbook, response drill | Reviewed deployment, actual check output, alert/incident history, approval and response record | Advanced orchestration, end-to-end automated decisions, and mission integrations require separate implementation. |
| Visibility & Analytics | 7.1 traffic logging; 7.2 SIEM; 7.3 common analytics | Identity/vault/Azure logs, optional Windows and VNet logs, optional Sentinel analytics | Recent source events, known tables, coverage checks, actual detection result | This does not claim all traffic or all data transactions are logged. Source gaps and retention must be measured. |

## Candidate NIST SP 800-53 Rev. 5 mapping

Choose and tailor the actual baseline through the organization's RMF process. Control implementation statements and assessment objectives require system-specific review; products do not satisfy a control automatically.

| Candidate control | Lab implementation statement to verify | Evidence and assessment approach |
|---|---|---|
| AC-2 — Account Management | Authorized users, owners, app assignments, and changes are reviewed. | Inspect group membership, ownership, assignment records, and one authorized removal test. |
| AC-3 — Access Enforcement | Only assigned pilot identities meeting enforced access policy reach the app. | Test assigned compliant, assigned unmanaged, and unassigned cases. |
| AC-6 — Least Privilege | VM identity can read the demonstration secret but cannot create one; administrators have scoped roles. | Read test, denied write with authorization reason, and RBAC review. |
| IA-2 — Identification and Authentication | The pilot app requires an appropriate authenticated user and MFA. | Match the access test to the sign-in's authentication details and policy result. |
| CM-2 / CM-6 — Baselines and Configuration Settings | Reviewed templates and documented hardening settings define the lab baseline. | Inspect versioned files and compare deployed state; retain relevant benchmark findings. |
| CM-8 — System Component Inventory | Lab identities, endpoints, VMs, app, network, and services are identified. | Inspect a current private asset inventory with owners and versions. |
| SC-7 — Boundary Protection | Only documented connector/app/vault and management paths are allowed. | Examine effective rules and run source-specific positive and negative flow tests. |
| SC-8 — Transmission Confidentiality and Integrity | The backend uses HTTPS with validated host name and trust chain. | Review binding, expiry, connector trust, backend validation setting, and actual HTTPS request. |
| SC-28 — Protection of Information at Rest | The synthetic secret is held in the encrypted vault service with access restrictions. | Review service configuration and access tests; state that this does not cover every enterprise data store. |
| AU-2 / AU-12 — Event Logging and Audit Record Generation | Defined sources generate the events needed for the lab test cases. | Inspect diagnostic/DCR settings and actual events generated by known test actions. |
| AU-6 / SI-4 — Audit Review and System Monitoring | A defined query or rule detects the permitted test activity and is reviewed. | Run the test, inspect the actual alert or incident, and document analyst action. |
| IR-4 — Incident Handling | The lab response drill has a recorded investigation, action decision, and recovery test. | Inspect the response record and supporting timestamps. |
| CA-7 — Continuous Monitoring | Owners review health, findings, access, evidence freshness, and residual risk at defined intervals. | Review monitoring schedule, measured results, and open POA&M items. |

## RMF lifecycle and repository connection

| RMF activity | Lab deliverable | Existing repository material |
|---|---|---|
| Prepare | Boundary, stakeholders, ownership, cost and security decisions | [Executive brief](../../executive/01-executive-brief.md) and [governance](../../governance/05-zero-trust-governance-policy.md). |
| Categorize | Synthetic DEV data and documented impact assumption | [RMF overview](../../rmf/04-rmf-for-leaders.md); a real categorization needs owner approval. |
| Select | Candidate controls, applicability, and benchmark selection | This matrix and [STIG governance](../../compliance/10-disa-stig-governance-and-implementation.md). |
| Implement | Deployed configuration and actual implementation statements | Azure templates, policy examples, and Windows application script. |
| Assess | Observed test results and supporting evidence | [Validation plan](04-validation-and-evidence.md) and evidence register. |
| Authorize | Document residual risk and any required decision | [Simulated eMASS workflow](../../executive/emass/README.md); no actual authorization is issued here. |
| Monitor | Health checks, evidence freshness, findings, and retesting | [Operations](05-operations-and-rollback.md) and [executive metrics](../../metrics/09-executive-dashboard.md). |

## Alignment to R0242994

This table uses the supplied job description. It does not assert that the position remains open or that the user meets every qualification.

| Role requirement | What this project can demonstrate after verification | Limits |
|---|---|---|
| Design and integrate Zero Trust architecture | A documented access path, trust boundaries, implementation, and test results across selected pillars | Full DoD Target Level validation remains outside the lab. |
| Identity and Access Management | Entra groups, app assignment, MFA, compliance-based access, emergency access, and optional PIM | Use actual tenant results and licensed features. |
| Segmentation and secure cloud architecture | Azure subnets, ASGs/NSGs, private endpoints, DNS, and managed identities | Not multivendor backbone or tactical-network deployment experience. |
| Endpoint security | Intune compliance, supported endpoint onboarding, and harmless detection validation | Server and client coverage must be established separately. |
| Architecture documentation and lifecycle work | Decision record, cost and acquisition inputs, deployment plan, change review, validation, rollback, and operations | Planning a lifecycle is different from operating an enterprise program. |
| RMF, ATO support, and STIGs | Traceable candidate controls, assessed benchmark findings, evidence, and POA&M | No actual ATO, eMASS connection, or assessed government system is established. |
| ZTNA and legacy transition | App-specific access through Entra Application Proxy and a staged migration method | The core lab is newly built; it does not document a completed legacy migration. |
| Automation and policy as code | Repeatable infrastructure files, report-only CA representation, an audit policy, scripted checks, and an optional response extension | Only features actually deployed and tested may be claimed. |
| Leadership and stakeholder communication | Risk decisions, ownership, measurable acceptance conditions, residual gaps, and reviewable changes | This project does not establish formal management authority or enterprise responsibility. |
| 8+ years, federal/DoD experience, classified work, TS/SCI, and certifications | Must come from independently verified professional history or credentials | A home lab cannot satisfy or prove these requirements. |

## Staged migration exercise

For a later legacy-to-Zero-Trust scenario, first inventory the application, its users, data, dependencies, and existing permitted flows. Then build parallel identity and device signals and collect a baseline. Publish one low-risk test app to a small assigned pilot, evaluate report-only results, enforce the pilot, and test recovery. Expand only after the owner accepts the measured results. Finally remove the replaced broad access path and retest that it no longer works. Each wave needs an owner, rollback trigger, evidence, and a decision record.

Do not describe this proposed migration sequence as an implemented migration until those steps have been performed.
