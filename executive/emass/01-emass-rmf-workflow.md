# Simulated eMASS RMF Workflow

> **Fictional portfolio demonstration:** This workflow is not exported from eMASS and does not connect to a live eMASS environment.

## Purpose

This workflow demonstrates how a cybersecurity team could use an eMASS-style process to maintain RMF records, connect security controls to evidence, manage findings and POA&M items, support an authorization decision, and sustain continuous monitoring. It is designed for the fictional Northstar Mission Services Mission Collaboration Platform.

## Roles and Responsibilities

| Role | Primary Responsibility |
|---|---|
| Authorizing Official | Reviews the authorization package, accepts or rejects residual risk, and records the authorization decision |
| Information System Owner | Owns mission requirements, resources, system risk, and the completeness of the authorization package |
| ISSM | Oversees the cybersecurity program, RMF execution, escalations, and authorization readiness |
| ISSO | Maintains system security records, coordinates evidence, monitors controls, and tracks corrective actions |
| Security Control Assessor | Independently assesses control implementation and documents findings |
| System Administrator | Implements technical safeguards and produces system-generated evidence |
| Cybersecurity Analyst | Reviews evidence, analyzes risk, reports metrics, and monitors remediation |
| Control Owner | Documents control implementation, maintains evidence, and corrects assigned weaknesses |

## Workflow

| Step | Activity | Primary Roles | Simulated eMASS Record or Action | Completion Criterion |
|---:|---|---|---|---|
| 1 | Register the information system | Information System Owner, ISSM | Create the system record and assign a fictional system identifier | Required system profile fields are complete and reviewed |
| 2 | Assign RMF and cybersecurity roles | Information System Owner, ISSM | Record role assignments and points of contact | Each required role has an accountable individual or organization |
| 3 | Define the authorization boundary | Information System Owner, ISSM, System Administrator | Document components, interfaces, data flows, dependencies, and exclusions | Boundary narrative and diagrams agree with the asset inventory |
| 4 | Select and tailor security controls | ISSM, Control Owner | Establish the baseline and document overlays, tailoring, and rationale | Applicable controls and approved tailoring decisions are recorded |
| 5 | Assign control responsibility | ISSM, ISSO, Control Owner | Assign common, system-specific, and hybrid control ownership | Every applicable control has an owner and implementation responsibility |
| 6 | Collect implementation evidence | ISSO, System Administrator, Cybersecurity Analyst, Control Owner | Associate artifacts with controls and record collection and review dates | Evidence is current, readable, attributable, and stored in the approved repository |
| 7 | Review control implementation | ISSO, ISSM, Control Owner | Update implementation narratives and status values | Narrative, evidence, boundary, and actual implementation are consistent |
| 8 | Record assessment findings | Security Control Assessor, ISSO | Record assessment results, weaknesses, severity, and source | Each result is traceable to assessment procedures and supporting evidence |
| 9 | Create and manage POA&M items | ISSO, ISSM, Information System Owner | Create a POA&M item for an accepted finding requiring tracked remediation | Owner, risk, milestones, resources, and completion date are documented |
| 10 | Track remediation | Control Owner, Cybersecurity Analyst, System Administrator | Update milestones, status, percent complete, and evidence | Progress is current and missed milestones are escalated |
| 11 | Prepare the authorization package | Information System Owner, ISSM, ISSO | Assemble the system security plan, assessment report, POA&M, and supporting artifacts | Package passes completeness and quality review |
| 12 | Record the authorization decision | Authorizing Official, Information System Owner, ISSM | Record the decision, terms, conditions, and expiration or review date | Decision and any conditions are communicated to accountable owners |
| 13 | Perform continuous monitoring | ISSO, Cybersecurity Analyst, Control Owner, Security Control Assessor | Refresh evidence, reassess controls, monitor change, and report risk | Scheduled activities are completed and material changes enter risk review |
| 14 | Maintain system accreditation milestones | ISSM, ISSO, Information System Owner | Track authorization conditions, recurring reviews, and package milestones | Dashboard dates, dependencies, risks, and leadership decisions remain current |

## Required Inputs

- Fictional system profile, mission description, impact categorization, and ownership
- Authorization-boundary narrative, architecture diagrams, inventories, and data flows
- Applicable control baseline, overlays, tailoring decisions, and implementation plans
- Control implementation statements and common-control inheritance details
- Assessment plan, assessment procedures, test results, and assessor observations
- Evidence inventory with artifact owners, locations, collection dates, and review dates
- Risk assessments, findings, remediation resources, and approved risk responses
- Authorization schedule, package requirements, and continuous-monitoring strategy

## Expected Outputs

- Complete and reviewed system record
- Traceable control implementation and responsibility assignments
- Current control-evidence register
- Assessment results with documented findings
- Actionable POA&M items and remediation milestones
- Quality-reviewed authorization package
- Recorded authorization decision and conditions
- Continuous-monitoring schedule and executive milestone dashboard

## Evidence Examples

| Evidence Category | Fictional Examples |
|---|---|
| Access control | Conditional Access policy export, privileged-role review, inactive-account review |
| Audit and accountability | Log-source inventory, retention configuration, log-review ticket |
| Configuration management | Approved baseline, configuration scan, change-control record |
| Identification and authentication | MFA configuration report, authentication test results |
| Incident response | Approved response plan, tabletop exercise record, lessons learned |
| Risk assessment | Risk assessment report, vulnerability scan summary, risk-review minutes |
| System integrity | Patch compliance report, vulnerability remediation record, alert-health report |
| Contingency planning | Backup test results, recovery exercise report, corrective-action record |

Evidence descriptions should explain what the artifact proves, its scope, source, review period, owner, and relationship to the applicable control. Evidence should never include secrets, credentials, sensitive personal data, or unnecessary operational detail.

## Status Values

| Record Type | Approved Demonstration Values |
|---|---|
| Control implementation | Implemented; Partially Implemented; Planned; Not Applicable |
| Assessment result | Satisfied; Other Than Satisfied; Pending Review; Not Assessed |
| POA&M | Open; In Progress; Pending Validation; Risk Accepted; Closed; Delayed |
| Milestone or activity | Not Started; In Progress; Pending Review; Complete; At Risk; Overdue |

## Escalation Criteria

Escalate to the ISSM and Information System Owner when:

- A high-risk finding is identified or increases in severity.
- A control failure creates a credible threat to mission, data, or authorization conditions.
- A POA&M milestone is overdue or the scheduled completion date is unlikely to be met.
- Evidence is missing, stale, inconsistent, or cannot support an assessor conclusion.
- A significant system change may affect the authorization boundary or security impact.
- A continuous-monitoring activity identifies material risk or repeated control degradation.
- A requested risk acceptance exceeds delegated authority.

Notify the Authorizing Official through the organization’s approved governance process when residual risk, authorization conditions, or a significant change may require a new decision.

## Quality-Review Checklist

- [ ] System identifier, name, impact level, owners, and authorization boundary are consistent across records.
- [ ] All applicable controls have an implementation status, responsible owner, and current narrative.
- [ ] Evidence is legible, dated, scoped, attributable, and mapped to the correct control.
- [ ] Assessment results are supported by evidence and use approved status values.
- [ ] Findings are not duplicated and are linked to the correct control and POA&M item.
- [ ] Each POA&M item includes risk, ownership, milestones, completion date, validation method, and residual risk.
- [ ] Closed items include independent or authorized validation and closure evidence.
- [ ] Continuous-monitoring dates and authorization milestones agree with the dashboard.
- [ ] Package records contain no credentials, sensitive personal data, or prohibited information.
- [ ] Required management and Authorizing Official decisions are clearly identified.

## Portfolio Disclaimer

All organizations, systems, identifiers, roles, dates, evidence, findings, decisions, and metrics in this workflow are fictional. This artifact is an independent portfolio demonstration, not an official authorization package or a representation of a government system. It contains no classified, controlled, proprietary, operational, or real government system information.
