# Azure DEV evidence

## Current status

No tenant deployment, live authentication test, network test, incident response result, or STIG assessment is supplied by this repository integration. The tracked files under `templates/` are empty evidence structures, not proof of successful implementation.

Copy them to an ignored `private/` directory to record actual work. Keep raw logs, certificate exports, detailed account inventories, and operational screenshots private. Publish only reviewed, sanitized results with their real timestamps and test IDs.

## Suggested screenshot names

| Filename | Capture only after |
|---|---|
| `01_Entra_EZTA_DEV_Groups.png` | Current group configuration and membership are checked. |
| `02_Azure_EZTA_DEV_Network.png` | Actual deployment and network boundaries are reviewed. |
| `03_Azure_EZTA_DEV_KeyVault_PrivateEndpoint.png` | Private endpoint approval and vault configuration are checked. |
| `04_Entra_EZTA_DEV_Private_App.png` | The published app settings and assignment are reviewed. |
| `05_Intune_EZTA_DEV_Device_Compliance.png` | The pilot client reports the intended compliance result. |
| `06_Entra_EZTA_DEV_CA_Pilot.png` | Policy scope, grant controls, and state are confirmed. |
| `07_Azure_EZTA_DEV_Segmentation_Test.png` | A source-specific test and enforcing rule are recorded. |
| `08_Sentinel_EZTA_DEV_Test_Incident.png` | A real permitted test produces the reviewed incident. |

## Public result summary

When tests have been executed, replace this paragraph with a concise description of the actual scope, dates, passed/failed/blocked cases, and material limitations. Keep the original template test results unchanged; use a separately reviewed sanitized summary for publication.
