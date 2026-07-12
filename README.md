
# Microsoft Zero Trust and RMF Executive Security Architecture

## Project Purpose

This portfolio project shows how a fictional organization can reduce cyber risk by combining:

- Microsoft Zero Trust
- NIST Risk Management Framework
- Identity, endpoint, cloud, data, and monitoring controls
- Clear leadership decisions, risk ownership, and measurable outcomes

It is written for non-technical stakeholders, executives, program managers, and hiring managers.

## Table of Contents

- [Project Purpose](#project-purpose)
- [Architecture Diagrams](#architecture-diagrams)
- [Plain-Language Overview](#plain-language-overview)
- [Fictional Organization](#fictional-organization)
- [Business Challenge](#business-challenge)
- [Target Business Outcomes](#target-business-outcomes)
- [Repository Contents](#repository-contents)
- [Recommended Review Order](#recommended-review-order)
- [Lessons Learned](#lessons-learned)
- [WSL and VS Code Setup](#wsl-and-vs-code-setup)
- [GitHub Publishing Commands](#github-publishing-commands)
- [Skills Demonstrated](#skills-demonstrated)
- [References](#references)
- [Disclaimer](#disclaimer)
- [Let's Connect](#lets-connect)
- [Author](#author)

## Architecture Diagrams

- Figure 1. Zero Trust Architecture — [Zero Trust Governance Policy](governance/05-zero-trust-governance-policy.md)
- Figure 2. Risk Management Framework Lifecycle — [RMF for Leaders and Stakeholders](rmf/04-rmf-for-leaders.md)
- Figure 3. DISA STIG Implementation Lifecycle — [DISA STIG Governance and Implementation](compliance/10-disa-stig-governance-and-implementation.md)

## Plain-Language Overview

**Zero Trust** means access is never assumed to be safe. Every request is checked, access is limited, and suspicious activity is monitored.

**RMF** is a seven-step process used to understand risk, choose protections, verify that they work, approve the remaining risk, and keep improving over time.

## Fictional Organization

**Organization:** Northstar Mission Services  
**System:** Mission Collaboration Platform  
**Users:** 1,200 employees and approved partners  
**Endpoints:** 850 managed Windows devices  
**Environment:** Microsoft Azure, Microsoft 365, selected AWS workloads, and on-premises services  
**Impact assumption:** Moderate confidentiality, integrity, and availability  

## Business Challenge

The organization has five priority concerns:

1. Too much permanent administrative access.
2. Inconsistent checks on endpoint security.
3. Incomplete logging across cloud and applications.
4. Sensitive data is not consistently classified and protected.
5. Security evidence is collected manually.

## Target Business Outcomes

- Reduce the chance of account compromise.
- Limit the damage caused by a successful attack.
- Protect sensitive information.
- Detect and contain incidents faster.
- Improve audit readiness.
- Give leaders a clear view of cyber risk.

## Repository Contents

```text
.
├── README.md
├── lessons-learned.md
├── executive/
│   └── 01-executive-brief.md
├── architecture/
│   ├── 02-target-security-architecture.md
│   └── 03-rmf-lifecycle.png
├── rmf/
│   └── 04-rmf-for-leaders.md
├── governance/
│   └── 05-zero-trust-governance-policy.md
├── risk/
│   └── 06-enterprise-risk-register.csv
├── roadmap/
│   └── 07-180-day-roadmap.md
├── procedures/
│   └── 08-major-incident-playbook.md
└── metrics/
    └── 09-executive-dashboard.md
```

## Recommended Review Order

1. Executive brief
2. Target security architecture
3. RMF lifecycle image
4. RMF guide for leaders
5. Zero Trust governance policy
6. Enterprise risk register
7. 180-day roadmap
8. Major incident playbook
9. Executive dashboard
10. DISA STIG governance and implementation
11. [Lessons Learned](lessons-learned.md)

## Lessons Learned

The [Lessons Learned](lessons-learned.md) summary explains the project’s key business, governance, implementation, and leadership insights.

## WSL and VS Code Setup

```bash
mkdir -p ~/projects
cd ~/projects

cp /mnt/c/Users/james/Downloads/microsoft-zero-trust-rmf-executive-architecture-v3.zip .

unzip microsoft-zero-trust-rmf-executive-architecture-v3.zip

cd microsoft-zero-trust-rmf-executive-architecture

code .
```

## GitHub Publishing Commands

```bash
git init
git branch -M main

git add .
git commit -m "Create executive Zero Trust and RMF architecture"

git remote add origin https://github.com/jbanday808/microsoft-zero-trust-rmf-executive-architecture.git
git push -u origin main
```

## Skills Demonstrated

- Cybersecurity architecture
- Zero Trust design
- RMF governance
- Risk communication
- Executive reporting
- Identity and privileged-access design
- Cloud and endpoint security
- Incident response
- Continuous monitoring
- DISA STIG governance and implementation
- Technical documentation

## References

### NIST and Federal Guidance

- [NIST Risk Management Framework](https://csrc.nist.gov/Projects/risk-management/about-rmf)
- [NIST SP 800-37 Rev. 2 — Risk Management Framework for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/37/r2/final)
- [NIST SP 800-53 Rev. 5 — Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [NIST SP 800-53A Rev. 5 — Assessing Security and Privacy Controls in Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final)
- [NIST SP 800-61 Rev. 3 — Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### DISA and DoD Guidance

- [DISA Security Technical Implementation Guides (STIGs) Document Library](https://public.cyber.mil/stigs/downloads/)
- [DoD Cyber Exchange](https://public.cyber.mil/)

### Microsoft Security and Cloud Guidance

- [Microsoft Zero Trust](https://learn.microsoft.com/en-us/security/zero-trust/)
- [Microsoft Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/overview)
- [Microsoft Cybersecurity Reference Architectures](https://learn.microsoft.com/en-us/security/adoption/mcra)
- [Microsoft cloud security benchmark](https://learn.microsoft.com/en-us/security/benchmark/azure/introduction)
- [Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/)
- [Microsoft Intune](https://learn.microsoft.com/en-us/intune/fundamentals/what-is-intune)
- [Microsoft Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint)
- [Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender)
- [Microsoft Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/)
- [Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/overview)
- [Microsoft Purview](https://learn.microsoft.com/en-us/purview/purview-where-to-start)
- [Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview)
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/overview)

### Threat Frameworks

- [MITRE ATT&CK](https://attack.mitre.org/)

## Disclaimer

This is an independent educational project. The organization, systems, risks, data, and metrics are fictional. The project does not represent an official authorization package, legal opinion, government policy, customer environment, or production design.

---

## Let's Connect

- **LinkedIn:** [James Banday](https://www.linkedin.com/in/james-allen-morta-banday-62a391128/)
- **GitHub:** [jbanday808](https://github.com/jbanday808)
- **Email:** [jamesbanday1@gmail.com](mailto:jamesbanday1@gmail.com)

## Author

**James Banday**

Threat Hunter | Cyber Intrusion Analyst | Cloud Security | Kubernetes | DevSecOps | Incident Response
