# Major Security Incident Playbook

## Scenario

A user or administrator identity is suspected of being compromised and may have accessed cloud resources or sensitive information.

## Purpose

Provide a clear response process for technical teams, business owners, and leadership.

## Severity

| Severity | Business Condition |
|---|---|
| Critical | Administrator compromise, active data theft, production outage, or major mission impact |
| High | Confirmed user compromise with sensitive access |
| Medium | Suspicious activity requiring investigation |
| Low | Unconfirmed anomaly with limited impact |

## Roles

| Role | Responsibility |
|---|---|
| Incident Commander | Coordinates decisions, priorities, and communication |
| SOC Lead | Leads validation and investigation |
| Identity Lead | Revokes sessions and secures accounts |
| Endpoint Lead | Investigates and isolates affected devices |
| Cloud Platform Lead | Reviews cloud activity and restricts access |
| Data Owner | Assesses affected information |
| GRC Lead | Tracks risk, evidence, and reporting |
| Executive Sponsor | Makes high-impact business and risk decisions |

## Step 1 — Validate

1. Confirm the affected identity and alert source.
2. Review sign-in, endpoint, cloud, and application activity.
3. Determine whether activity is expected.
4. Assign severity.
5. Name the incident commander.

## Step 2 — Contain

1. Revoke active sessions and tokens.
2. Disable or restrict the account when authorized.
3. Remove unexpected privileged roles.
4. Isolate confirmed compromised endpoints.
5. Block malicious indicators when appropriate.
6. Preserve evidence.

## Step 3 — Determine Business Impact

1. Identify affected systems and services.
2. Identify sensitive data accessed or moved.
3. Determine mission or customer impact.
4. Determine whether reporting or notification is required.
5. Estimate recovery needs.

## Step 4 — Eradicate

1. Reset credentials using approved strong authentication.
2. Remove malicious files, applications, rules, tokens, and persistence.
3. Patch exploited vulnerabilities.
4. Correct unsafe configurations.
5. Rotate affected secrets, keys, and certificates.
6. Remove unauthorized access.

## Step 5 — Recover

1. Restore affected systems from a trusted state.
2. Re-enable access only after validation.
3. Require compliant endpoints.
4. Monitor for recurrence.
5. Confirm normal business operation.

## Step 6 — Improve

1. Document root cause and impact.
2. Update the risk register.
3. Assign corrective actions.
4. Improve detections and procedures.
5. Conduct lessons learned within five business days.
6. Provide an executive summary for Critical and High incidents.

## Leadership Communication

The first executive update for a Critical incident should include:

- What happened
- What is affected
- What has been contained
- Known or potential data impact
- Current business impact
- Decisions required
- Next update time

## Success Criteria

- Compromised access is removed.
- The incident scope is understood.
- Business and data impact are assessed.
- Recovery is validated.
- Evidence is preserved.
- Corrective actions have owners and dates.
