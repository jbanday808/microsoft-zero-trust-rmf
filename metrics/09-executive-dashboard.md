# Executive Cybersecurity Dashboard

## Purpose

Provide leadership with a concise view of risk, control coverage, incident performance, and roadmap progress.

## Dashboard Summary

| Area | Metric | Target | Executive Meaning |
|---|---|---:|---|
| Identity | Privileged accounts using strong authentication | 100% | Reduces account-takeover risk |
| Privileged Access | Privileged roles using time-limited activation | At least 95% | Reduces permanent high-level access |
| Endpoints | Managed endpoints reporting compliant | At least 95% | Reduces access from unsafe devices |
| Monitoring | Critical log sources connected and healthy | 100% | Supports timely detection and investigation |
| Vulnerabilities | Critical vulnerabilities past due | 0 | Reduces avoidable exposure |
| Cloud | Critical resources with unauthorized public exposure | 0 | Reduces data-exposure risk |
| Governance | High-risk exceptions past expiration | 0 | Prevents temporary risk from becoming permanent |
| Incident Response | High-severity incidents contained within target | 100% | Limits business impact |
| Recovery | Critical recovery tests completed successfully | 100% | Supports operational resilience |
| Evidence | Critical controls with current evidence | 100% | Improves audit and authorization readiness |

## Status Thresholds

| Status | Meaning |
|---|---|
| Green | Target met or risk is within approved tolerance |
| Amber | Target is at risk or corrective action is required |
| Red | Target is missed, risk is high, or executive action is required |

## Monthly Technical Review

Review:

- Control health
- Vulnerabilities
- Policy compliance
- Log-source health
- Incident trends
- Open high-risk findings
- Expiring exceptions
- Corrective-action progress

## Quarterly Executive Review

Present:

1. Top risks and trend
2. Major incidents and lessons learned
3. Roadmap progress
4. Control coverage
5. Overdue critical actions
6. Exceptions requiring approval
7. Funding, staffing, or policy decisions

## Assessment Approach

Controls are evaluated by:

- **Examine:** Review policies, configurations, reports, logs, and tickets.
- **Interview:** Confirm ownership and operating procedures.
- **Test:** Validate that protections allow approved activity and block or alert on prohibited activity.

## Evidence Sources

| Area | Evidence |
|---|---|
| Identity | Conditional Access, sign-in, MFA, and PIM reports |
| Endpoints | Intune compliance and Defender coverage |
| Cloud | Azure Policy and Defender for Cloud findings |
| Data | Purview labels, DLP alerts, and encryption evidence |
| Monitoring | Sentinel connector health, analytics rules, and incidents |
| Incident Response | Timelines, containment actions, and lessons learned |
| Recovery | Backup configuration and restoration-test results |
| Governance | Risk register, exceptions, assessments, and corrective actions |

## Leadership Questions

At each quarterly review, leaders should ask:

1. What are our top three cyber risks?
2. Are those risks improving or getting worse?
3. Which high-risk actions are overdue?
4. Are critical systems being monitored?
5. Can we recover from a major incident?
6. Which decisions or investments are required now?
