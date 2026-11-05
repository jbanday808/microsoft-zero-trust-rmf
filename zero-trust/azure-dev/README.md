# Azure Zero Trust Architecture — DEV

**Author:** James Banday

**Role alignment:** Booz Allen Hamilton, ZT Engineer Lead, R0242994; Honolulu, Hawaii; on site, based on the supplied job description.

**Documentation date:** October 29, 2026, Hawaii time.

**Environment:** Separate Azure commercial development subscription and Microsoft Entra test tenant, with synthetic data.

## Purpose

Extend the existing Microsoft Zero Trust and RMF portfolio with a hands-on implementation path. The lab checks identity and device health before allowing access to a private application, limits network paths, protects a demonstration secret, and connects test results to RMF evidence.

## Repository decision

| Repository | Existing focus | Fit for this integration |
|---|---|---|
| [microsoft-zero-trust-rmf](https://github.com/jbanday808/microsoft-zero-trust-rmf) | Zero Trust architecture, RMF, STIG governance, risk, and leadership reporting | Recommended home for an end-to-end architecture and its implementation evidence. |
| [elastic-security-engineering-rhel10](https://github.com/jbanday808/elastic-security-engineering-rhel10) | RHEL endpoints, Elastic Agent, Logstash, and investigation dashboards | A useful separate monitoring project. Its current evidence does not establish this Azure architecture. |

## Read and build in this order

| File | Use |
|---|---|
| [01 — Architecture](01-architecture.md) | Understand the access path, trust boundaries, and allowed traffic. |
| [02 — Complete step-by-step guide](02-step-by-step-guide.md) | Prepare, deploy, configure, test, and document the lab. |
| [03 — DoD, RMF, and role alignment](03-dod-rmf-role-alignment.md) | Connect the design to the seven pillars and the supplied job requirements. |
| [04 — Validation and evidence](04-validation-and-evidence.md) | Record positive and negative tests without assuming success. |
| [05 — Operations and rollback](05-operations-and-rollback.md) | Maintain the lab, handle failures, and remove paid resources. |
| [06 — References](06-references.md) | Consult primary Microsoft, NIST, and DoD guidance. |
| [Architecture decision](decisions/001-azure-dev-boundary.md) | Review the design choices and remaining gaps. |

## What the files provide

The [foundation template](infra/azure-foundation.json) defines the network, explicit outbound NAT, application security groups, network rules, private DNS, a private Key Vault endpoint, and Log Analytics. Key Vault audit collection is configured. Sentinel onboarding is an explicit opt-in parameter and defaults to false.

The [Windows template](infra/windows-lab.json) adds two private Windows Server VMs. The [application script](scripts/configure-private-web-app.ps1) prepares the HTTPS demonstration site. Entra groups, user licensing, Intune enrollment, connector installation, app publishing, Conditional Access, endpoint protection, and additional log sources require the configuration steps in the guide.

## Implementation status

| Item | Status when this package is added |
|---|---|
| Architecture, guide, templates, scripts, and test plan | Authored; see the integration change for actual repository checks. |
| Existing `EZTA-DEV` groups | Previously reported by the user; current IDs and membership must be checked. |
| Azure deployment and Windows configuration | Not run by this repository integration. |
| Tenant policies, licenses, connectors, and device compliance | Not verified in the tenant. |
| Network, authentication, monitoring, and recovery results | Not run. Record results in the evidence templates. |
| DoD Target Level completion, STIG compliance, ATO, or classified deployment | Not established by this lab. |

## Start here

Complete Steps 1–6 of the guide before creating paid infrastructure. Start Conditional Access in report-only mode and move only the pilot application to enforcement after the required tests pass. All generated evidence starts as **NOT RUN**.

The existing [executive eMASS simulation](../../executive/emass/README.md), [RMF overview](../../rmf/04-rmf-for-leaders.md), and [STIG governance guide](../../compliance/10-disa-stig-governance-and-implementation.md) remain supporting portfolio material.
