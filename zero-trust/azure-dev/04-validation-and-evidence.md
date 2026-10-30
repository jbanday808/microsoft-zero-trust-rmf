# Validation and evidence plan

## Evidence rule

Record the actual result, UTC time, source device, principal, policy or rule state, private evidence location, and reviewer for every test. A screenshot of a setting is supporting configuration evidence; an access result and its corresponding log establish observed behavior.

The [test-results template](evidence/templates/test-results.json) deliberately starts with every case **NOT RUN** and no actual outcome. Store the populated version in an ignored private directory. Do not substitute expected outcomes for observations.

| State | Meaning |
|---|---|
| NOT RUN | The case has not been executed. |
| PASS | The observed result matches the expectation and the evidence supports the conclusion. |
| FAIL | The observed result does not meet the expectation. |
| BLOCKED | A missing license, permission, source, or other prerequisite prevents a valid test. |

## Acceptance cases

| ID | Source and action | Expected result | Evidence needed |
|---|---|---|---|
| ID-01 | Assigned pilot opens the external app on compliant Windows client after policy enforcement | App allowed and applicable MFA/compliance controls satisfied | Page result and matching sign-in policy/authentication/device details. |
| ID-02 | Same assigned pilot opens the app on an unmanaged device | App denied by the enforced compliant-device control | Matching policy failure and device state; no backend page access. |
| ID-03 | Licensed but unassigned user requests the app | App access denied by assignment | Assignment state and actual user access/sign-in result. |
| ID-04 | Review the policy in report-only, then perform a test sign-in | Prospective evaluation recorded; the policy itself does not enforce denial | Policy state, report-only result, and actual access result. |
| ID-05 | Test both emergency accounts before enforcement and review exclusions afterward | Both can recover administration, with strong authentication and restrictive-policy exclusions | Private sign-in tests, role state, exclusion review, and alert record. |
| DEV-01 | Enrolled Windows client syncs compliance policy | Device is compliant with recent details for the intended requirements | Intune device and policy records; no inferred result from enrollment alone. |
| NET-01 | Connector requests app HTTPS on 443 | Allowed, with valid backend certificate | HTTPS response, DNS result, and explicit allow rules. |
| NET-02 | Connector attempts app RDP on 3389 | Denied | TCP result plus source/destination effective NSG deny; RDP remains reachable from Bastion. |
| NET-03 | Connector attempts app HTTP on 80 | Denied | TCP result plus effective rule; a stopped HTTP listener alone is insufficient. |
| NET-04 | Connector attempts vault endpoint HTTPS on 443 | Denied | Private DNS, TCP result, connector outbound rule, endpoint network-policy and NSG review. |
| NET-05 | App VM connects to vault HTTPS on 443 | Allowed through the private endpoint | Private endpoint address, successful connection, network rules. |
| NET-06 | App attempts connector RDP on 3389 | Denied | TCP result and the explicit effective deny rules. |
| DATA-01 | App managed identity reads `ezta-demo` | Read succeeds | Secret ID only, identity/RBAC state, and corresponding vault audit event. |
| DATA-02 | Same managed identity attempts a secret write | Write denied for authorization reasons | HTTP authorization failure and vault audit record, with no successful new write. |
| DATA-03 | External device attempts vault data access through the public network | Public data access unavailable | Public network configuration and actual network-denial reason, distinguished from missing authentication. |
| LOG-01 | Repeat known login, vault, and Azure management actions | Each required source produces a recent event in the intended destination | Table, event time, ingestion time, source action, and query. |
| DET-01 | Generate permitted lab sign-in failures or emergency sign-in | Configured alert or Sentinel incident created and reviewed | Rule configuration, run result, actual alert/incident, and analyst action. |
| POL-01 | Evaluate protected vault and optional disposable negative case | Private vault compliant; disposable public-access vault noncompliant in audit mode | Actual policy evaluation and recorded effect. |
| PRIV-01 | Activate a scoped PIM role, perform one permitted action, let access expire | Scoped activation and expiry work as intended | Actual activation, Azure/directory action, and expired-access test; BLOCKED if unlicensed. |
| OPS-01 | Change pilot policy to report-only, verify recovery, then restore enforcement | Recovery works and the final enforced pilot state passes the access tests | Change record, test results before/after, and final policy state. |
| OPS-02 | Stop the sole connector temporarily, test app, and restore service | New backend access is unavailable; service returns after restoration | Timed access attempts and connector health; documents single-connector availability risk. |

## Network check commands

See Step 19 for the PowerShell commands and their explanations. Save output privately. A denied connection needs independent evidence of the enforcing rule. These TCP tests do not verify TLS trust, identity authorization, data authorization, or every possible network path.

## Managed identity denied-write test

Run this only on `ezta-app01` against the synthetic lab vault after the successful read. Replace the vault name. The body contains demonstration data; the test attempts a write that the read-only identity should be unable to perform.

```powershell
$LabVaultName = 'REPLACE_WITH_DEPLOYED_VAULT_NAME'
$LabToken = Invoke-RestMethod -Headers @{Metadata='true'} -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net'
$LabWriteResult = $null
try {
    $null = Invoke-RestMethod -Method Put -ContentType 'application/json' -Body '{"value":"synthetic-negative-test"}' -Headers @{Authorization="Bearer $($LabToken.access_token)"} -Uri "https://$LabVaultName.vault.azure.net/secrets/ezta-write-negative-test?api-version=7.4"
    $LabWriteResult = 'FAIL: write unexpectedly succeeded; inspect excessive permissions and remove the synthetic test secret with an authorized administrator.'
} catch {
    $LabStatus = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 0 }
    $LabWriteResult = "Observed HTTP status: $LabStatus. Verify the authorization reason and matching vault audit event; only the expected authorization denial can pass this test."
} finally {
    Remove-Variable LabToken
}
$LabWriteResult
```

**Command overview:** The identity metadata call obtains the VM's short-lived token. The `Put` request attempts to create a synthetic secret. `try` detects an unexpected successful write; `catch` reports the HTTP result for review. `finally` clears the token variable. A network timeout, missing token, or unrelated `403` cannot establish correct RBAC enforcement.

## Detection acceptance

Before passing DET-01, confirm the source events arrived, the query returned those exact events, the rule evaluated the same time window, and a real alert or incident was created. Record any ingestion delay. A failure threshold may need tuning to observed lab traffic; keep the change history and retest.

## Evidence register

Use the [control evidence template](evidence/templates/control-evidence-register.md) to connect the tests to candidate controls. Retain raw evidence privately. A public summary may include sanitized screenshots and measured outcomes only after review.

Keep configuration evidence, execution evidence, and interpretation distinguishable in each record. If a finding remains unresolved, identify its owner, risk, planned action, target date, and retest condition in a POA&M rather than hiding it behind a successful screenshot.
