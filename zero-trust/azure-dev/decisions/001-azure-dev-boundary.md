# Decision 001 — Azure DEV implementation boundary

**Status:** Proposed implementation; repository assets authored.

**Owner:** James Banday.

**Date:** October 29, 2026, Hawaii time.

## Decision

Place the lab under `zero-trust/azure-dev/` in `microsoft-zero-trust-rmf`. Extend the existing governance and RMF material with Azure-only implementation assets. Use Entra Application Proxy for a private HTTP application access exercise; this path does not require the separate Entra Private Access product.

## Reasons

The repository already organizes architecture, governance, risk, STIGs, and simulated eMASS evidence. The supplied ZT Engineer Lead description emphasizes all of these alongside implementation and testing. The Elastic repository documents a different monitoring stack and remains a separate project.

Use two private Windows VMs to separate the connector from the application. Add explicit outbound NAT so installation and connector connectivity do not rely on implicit outbound service. Use HTTPS to the backend with certificate verification. Use a managed identity for the separate secret access exercise instead of a stored application password.

## Constraints and gaps

| Item | Consequence and next action |
|---|---|
| Commercial Azure and test identities | This is not a government cloud or classified environment. Reassess endpoints, service availability, identity integration, authorization boundaries, and approved controls for any real defense deployment. |
| One connector and one app server | A single failure can interrupt service. A resilience extension needs two connectors, workload redundancy, regional design, and recovery tests. |
| Lab-generated certificate authority on the app VM | Suitable only for isolated synthetic-data testing. Production needs managed PKI, protected signing keys, renewal, and revocation design. |
| Internet 80/443 egress allowed | Network access is constrained by port, not by approved domain. Add reviewed firewall or proxy rules and retest connector TLS without interception. |
| Public Azure management and monitoring endpoints | Authentication and RBAC protect these endpoints. No Azure Monitor Private Link Scope or private management plane is implemented. |
| Static IIS demonstration page | The page proves protected access. It does not implement business roles, per-record data authorization, or a production secret-backed application. |
| Compliance mappings | They identify candidate controls and evidence, not a completed assessment or authorization. |
| Licensing and paid resources | Confirm current entitlements and estimates before deployment; retain a cost owner and cleanup date. |

## Completion rule

Only describe a control as verified after its positive test, negative test where applicable, source evidence, UTC timestamp, and reviewer are recorded. An absent license or missing log source is a blocked test, not a passing result.
