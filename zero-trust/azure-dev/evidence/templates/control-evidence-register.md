# Control evidence register template

**System:** Azure Zero Trust DEV.

**Owner:** To be recorded.

**Assessment window:** Not started.

**Evidence location:** Private record; populate after execution.

| Record | Candidate control | Implementation to assess | Tests | Actual result | Evidence reference | UTC date | Reviewer |
|---|---|---|---|---|---|---|---|
| E-01 | AC-2, AC-3, IA-2 | App assignment, MFA, and compliant-device policy | ID-01 through ID-05 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-02 | CM-8, CM-6 | Pilot inventory and device compliance | DEV-01 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-03 | SC-7 | Explicit connector/app/vault and management boundaries | NET-01 through NET-06 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-04 | AC-6, SC-8, SC-28 | Private read-only managed identity access | DATA-01 through DATA-03 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-05 | AU-2, AU-6, AU-12, SI-4 | Required logging and detection | LOG-01, DET-01 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-06 | CM-6, CA-7 | Audit policy and ongoing review | POL-01 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-07 | AC-6 | Optional temporary privileged access | PRIV-01 | NOT RUN | Not collected | Not recorded | Not assigned |
| E-08 | IR-4, CA-7 | Recovery, outage, and maintenance | OPS-01, OPS-02 | NOT RUN | Not collected | Not recorded | Not assigned |

## POA&M working template

| Finding | Type | Risk | Planned action | Owner | Target date | Retest | Status |
|---|---|---|---|---|---|---|---|
| Broad web egress | Known design limitation; not a measured incident | Outbound 80/443 is not restricted to approved domains | Design and test supported firewall/proxy destination restrictions without intercepting the connector's TLS tunnel | To assign | To assign | Connector health plus required/denied destination tests | Open design gap |
| Single connector | Known availability limitation | Connector outage can interrupt app access | Add a second connector and test failover when extending the lab | To assign | To assign | Independent connector outage drill | Open design gap |
| Additional assessment findings | Populate only after assessment | To assess | To plan | To assign | To assign | To define | NOT ASSESSED |
