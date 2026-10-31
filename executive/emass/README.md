# Simulated eMASS Compliance Management

> **Portfolio demonstration:** All systems, identifiers, dates, findings, evidence, metrics, and decisions in this directory are fictional. This project does not connect to, export from, or represent a live eMASS environment.

## What is eMASS?

**eMASS stands for Enterprise Mission Assurance Support Service.** It is a government web application used to organize RMF security records, assessment evidence, corrective actions, and authorization workflows.

Start with [What is eMASS?](00-what-is-emass.md) for a plain-language overview, then follow the simulated workflow and trackers below.

## Purpose

This section demonstrates how an eMASS-style compliance-management workflow could support the Risk Management Framework (RMF) and system authorization for the fictional Northstar Mission Services Mission Collaboration Platform. It shows how an Information Security Analyst could organize control implementation records, assessment evidence, Plans of Action and Milestones (POA&M), continuous-monitoring activities, and Authorization to Operate (ATO) milestones.

Security controls define required safeguards. Evidence demonstrates how those safeguards are implemented and assessed. Control weaknesses become findings and, when remediation must be tracked, POA&M items. Continuous monitoring refreshes evidence and identifies changes in risk. Together, these records support an authorization package and give leadership a current view of ATO milestones and residual risk.

Developed a simulated eMASS workflow to track RMF security controls, implementation evidence, POA&M remediation activities, continuous-monitoring requirements, and ATO milestones for a Microsoft Zero Trust environment.

## Directory Contents

| File | Description |
|---|---|
| [00-what-is-emass.md](00-what-is-emass.md) | Plain-language explanation of eMASS, its relationship to RMF, and the Office case-study example |
| [01-emass-rmf-workflow.md](01-emass-rmf-workflow.md) | Step-by-step simulated eMASS workflow, roles, inputs, outputs, escalation criteria, and quality checks |
| [02-control-evidence-register.csv](02-control-evidence-register.csv) | Fictional register connecting NIST SP 800-53 controls to implementation evidence and assessment results |
| [03-poam-tracker.csv](03-poam-tracker.csv) | Fictional POA&M tracker for findings, remediation milestones, validation, and residual risk |
| [04-ato-milestone-dashboard.md](04-ato-milestone-dashboard.md) | Executive-level simulated authorization, control, POA&M, and continuous-monitoring dashboard |

## Related CVE Case Studies

- [CVE-2026-42831 — Microsoft Office](../../cve-case-studies/CVE-2026-42831-office-rce-rmf/README.md#what-is-emass): Connects Office remediation evidence, risks, and POA&M records to the simulated workflow.
- [CVE-2026-109618 and CVE-2026-109619 — PHP](../../cve-case-studies/CVE-2026-109618-109619-php-rce-rmf/README.md): Provides the PHP RMF, mitigation, and DISA STIG response guide.

## Skills Demonstrated

- eMASS workflow knowledge
- Risk Management Framework
- NIST SP 800-53 control management
- ATO support
- POA&M management
- Continuous monitoring
- Evidence management
- Cybersecurity reporting

## Portfolio Disclaimer

This material is an independent educational portfolio artifact. It contains no classified, controlled, proprietary, operational, or real government system information. Terminology and workflows are illustrative and must be tailored to the policies, procedures, and eMASS configuration of an authorized organization.
