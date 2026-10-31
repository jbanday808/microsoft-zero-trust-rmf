# What is eMASS?

**eMASS stands for Enterprise Mission Assurance Support Service.** It is a government web application that helps security teams organize the records needed to assess a system, track weaknesses, and support an authorization decision.

In simple terms, eMASS keeps security requirements, supporting evidence, corrective actions, and approval records together so reviewers can understand the system's current risk.

## How eMASS relates to RMF

The **Risk Management Framework (RMF)** defines the process for managing system risk. **eMASS** supports the records, reviews, and workflows used to carry out that process.

The Authorizing Official reviews assessed risk and records the authorization decision. Using eMASS does not automatically make a system compliant or grant an Authorization to Operate (ATO).

## What teams organize in eMASS

| Record | Plain-language purpose |
|---|---|
| System information | Describes the system, its owner, boundaries, and impact. |
| Security controls | Documents the safeguards the system must implement. |
| Assessment evidence | Supports conclusions about whether safeguards work. |
| Findings and POA&M | Tracks weaknesses, responsible owners, and corrective milestones. |
| Authorization package | Brings the assessed system records together for the required decision. |
| Monitoring records | Keeps evidence, changes, and remaining risk current. |

Sources: [DISA eMASS Overview](https://www.disa.mil/~/media/files/disa/fact-sheets/emass.pdf) and [CDSE eMASS Training](https://www.cdse.edu/Training/eLearning/DISA-100/).

## Example: CVE-2026-42831 Office case study

This is a proposed documentation workflow for the [Office case study](../../cve-case-studies/CVE-2026-42831-office-rce-rmf/README.md), not a record of actions performed in a government system.

1. Identify affected assets and the responsible system owner.
2. Link the applicable controls to the documented weakness.
3. Associate update and validation evidence with the system's assessment records.
4. Track unfinished remediation through a POA&M with an owner and milestones.
5. Have the authorized assessor review the evidence and record the remaining gaps.
6. Provide the results to the appropriate risk and authorization authority.
7. Refresh the records as updates, reassessments, and monitoring change the risk.

## Files in this portfolio

| File | How to use it |
|---|---|
| [Simulated RMF workflow](01-emass-rmf-workflow.md) | Follow the example roles, activities, evidence, and review gates. |
| [Control evidence register](02-control-evidence-register.csv) | Review a fictional example connecting controls to supporting evidence. |
| [POA&M tracker](03-poam-tracker.csv) | Review a fictional corrective-action and milestone tracker. |
| [ATO milestone dashboard](04-ato-milestone-dashboard.md) | Review a fictional summary of authorization readiness and remaining work. |

These files illustrate record organization. They do not connect to a live eMASS instance, contain actual government findings, or establish that a system has been authorized. Use an organization's approved process and file formats when working in its authorized environment.

## References

- [DISA eMASS Overview](https://www.disa.mil/~/media/files/disa/fact-sheets/emass.pdf): Explains eMASS capabilities for security assessment, reporting, and authorization.
- [CDSE eMASS Training — DISA-100.06](https://www.cdse.edu/Training/eLearning/DISA-100/): Introduces system records, control assessment, POA&M, workflows, continuous monitoring, and reporting.
- [NIST SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final): Explains the RMF process supported by the portfolio workflow.

[Return to the eMASS section](README.md) · [View all CVE case studies](../../cve-case-studies/README.md)
