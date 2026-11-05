# Operations, troubleshooting, and rollback

## Operating schedule

| Frequency | Review | Required result |
|---|---|---|
| Each active lab session | Connector health, VM state, recent sign-ins, log ingestion, current cost | Identify unhealthy services, missing logs, and unexpected charges before testing. |
| Weekly while retained | Windows updates, endpoint health, certificate expiry, recent policy failures | Patch in a maintenance window and retest the affected app/network paths. |
| Monthly | Group and app assignment, Azure RBAC, policy scope, cost estimate, open findings | Remove unnecessary access; document the owner and action for each gap. |
| At least every 90 days | Emergency account authentication and recovery | Both recovery accounts function using the intended strong authentication. |
| After any architecture or security change | Affected positive/negative tests and rollback | The change is supported by fresh evidence and a known recovery path. |

## Optional PIM setup and validation

1. Confirm the applicable license and use a separate authorized resource administrator to create the assignment. The test administrator must not already have a permanent assignment that would mask expiry.
2. In Entra **ID Governance → Privileged Identity Management → Azure resources**, select the lab subscription and then the `rg-ezta-dev` resource group. Open **Roles → Add assignments**.
3. Select the minimum role required for the test, such as Contributor for deployment work within this disposable group. Choose the normal test administrator, make the assignment **Eligible**, and set a short eligibility window. This role does not provide Key Vault secret contents or permission to create RBAC grants.
4. Configure the role's activation settings with a short duration, such as one hour, and the supported MFA, justification, and approval requirements. If using approval, choose an independent available approver and test that path.
5. As the test administrator, open **PIM → My roles → Azure resources**, activate the role with the required justification, and complete the configured checks. Perform one benign permitted action, such as updating a lab resource tag.
6. Deactivate or allow the assignment to expire. After relevant session and permission caches refresh, verify the same action is denied without another role supplying access. Record the actual scope, approver, timing, permitted action, expiry test, and Azure Activity evidence.

Ordinary admin-group membership alone is not proof of PIM. Mark PRIV-01 blocked if the required license or administrative prerequisite is unavailable.

## Troubleshooting guide

| Symptom | Inspect first | Correction to test |
|---|---|---|
| Assigned pilot cannot access app | Sign-in log, exact app client ID, direct group membership, app consent, policy scope | Correct the specific assignment, consent, or policy issue; retest a fresh supported session. |
| Compliant client is treated as unmanaged | Sign-in device ID, browser work profile, Entra join, MDM enrollment, recent compliance | Fix enrollment or browser device signaling; do not remove the compliance requirement to label the test successful. |
| Application Proxy gateway/backend error | Connector health, private DNS, HTTPS response from connector, root trust, certificate name and expiry | Restore backend reachability or certificate validation and test the external access path again. |
| Connector cannot reach cloud | NAT association, NSG egress rules, current destination prerequisites, TLS 1.2, WinHTTP setting, interception | Correct the documented dependency and check connector activation. |
| Vault connection times out | Private DNS, approved endpoint, subnet network policies, source ASG, effective rules | Verify the request originates from the app VM and the allowed path is in place. |
| Vault read returns authorization failure | Actual VM identity, vault scope, role name, propagation time, token resource | Correct RBAC at the intended scope and retest. Avoid broad administrator grants. |
| Negative network test unexpectedly succeeds | Effective NSGs on both subnets, priorities, ASG membership, existing established connections | Correct rules and retry a new connection. NSG changes may not terminate established flows immediately. |
| Log query has no table or rows | Source configuration, generated source event, permissions, destination/table, time range | Verify one source at a time. Do not treat an empty query as absence of an attack or a passing detection test. |
| Costs continue after VM shutdown | VM allocation state, disks, NAT, Bastion, public IPs, endpoint, logging and security plans | Review billed resources and remove the services no longer needed. |

## Conditional Access rollback

Keep a normal administrator session and tested recovery path before enforcement. If the pilot is unexpectedly blocked, change only `EZTA-DEV-CA01-Pilot-App-MFA-Compliant` to report-only or disabled. Record its previous state, the reason, and the time. Confirm the administrator and pilot can recover access, inspect the exact sign-in result, and correct the problem. Restore pilot enforcement and repeat ID-01, ID-02, and ID-03 before expanding the policy.

A report-only policy cannot serve as evidence that unmanaged devices are blocked. Rollback changes the protection state and must appear in the final record.

## Network and certificate rollback

Before editing a network rule, save its exact previous source, destination, ports, priority, and action privately. Make one reviewed change at a time. If access breaks, restore the known rule and retry a new connection. Preserve Bastion recovery access. Do not add a broad VNet or internet inbound allow rule as a permanent workaround.

The IIS setup script intentionally stops if its named site already exists. For renewal, issue and bind a replacement leaf through a reviewed maintenance procedure, verify the trusted chain and expiry, and test from the connector with validation enabled. For a failed initial lab setup, rebuilding the disposable app VM may be clearer than repeatedly adding certificate chains. Never export or publish the lab root's private key.

## Connector outage drill

Record the current active connector and app state. During the lab window, stop the connector service on the sole connector VM, then attempt a fresh application request and record the actual result. Restore the service, wait for active health, and retest. Existing sessions and cached content can affect the observation, so record the requested resource and test method. This documents a single point of failure. A resilience extension needs another connector and independent failover tests.

## Deallocate retained VMs

Run from the intended Azure Bash session after checking the resource group.

```bash
az vm deallocate --resource-group "$LAB_RG" --name ezta-conn01
az vm deallocate --resource-group "$LAB_RG" --name ezta-app01
```

**Command overview:** `az vm deallocate` releases the VM's compute allocation. `--resource-group` and `--name` select the exact lab VM. Managed disks and other services remain billable.

## Staged cleanup

1. Preserve reviewed private evidence, the current deployment outputs, policy and role records, findings, and actual test results.
2. Confirm that the lab app is no longer in use. Disable its user sign-in and its pilot policy as part of a documented retirement change. Do not delete unrelated tenant policies or recovery accounts.
3. Unregister the lab connector and remove the dedicated enterprise application and associated registration according to their ownership and dependency checks. Remove temporary vault administration and other lab-only assignments.
4. Remove or update the **lab-created** Entra diagnostic setting and subscription Activity log export that reference the retiring workspace. Preserve any shared or pre-existing settings.
5. Inspect the lab resource group. Verify every listed resource belongs to this disposable exercise. If Bastion, flow log storage, Network Watcher flow logs, playbooks, or other extensions were created in another group, inventory and retire them separately.

```bash
az account show --query '{subscription:name,tenant:tenantId}' --output table
az resource list --resource-group "$LAB_RG" --output table
az group delete --name "$LAB_RG"
```

**Command overview:** The first two commands display the active account context and deletion scope. `az group delete` removes the named resource group and its resources after the CLI confirmation. This is the destructive cleanup step; verify the displayed scope before confirming.

6. Verify deletion and inspect Cost Management for any remaining resources and later-arriving usage records. Log Analytics soft-delete and vault retention may leave recoverable service objects for their documented retention windows.
7. Purge protection prevents immediate Key Vault purge during the configured seven-day retention. Do not disable or bypass it to reuse a name. Recreating the same group may require recovering the intended vault or deliberately selecting a different lab prefix after reviewing the retained state.
8. The resource-group deletion removes its policy assignment but does not remove the subscription-level custom policy definition. Delete `ezta-dev-vault-private` only after confirming it has no other assignments.
9. Keep pre-existing `EZTA-DEV` groups or devices that support other work. Remove only objects and memberships created solely for the retired lab after checking their current use. The SharePoint DEV site has a separate lifecycle.
10. Publish a sanitized final status that distinguishes retained documentation from retired infrastructure. Stop reporting connector or device health as current after the environment is deleted.
