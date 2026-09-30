# Day 44: Minimum-Permission Control

## Objective

Ensure that the Platform AI has only the permissions required for each authorized task.

Common rules, vocabulary, and AI–Human boundaries are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

This is Stage 4 of the End-to-End Partner Workflow (Days 41–50).

---

## Stage Specification

### Inputs

- minimized Evidence Package from Day 43
- required task
- required permissions
- granted permissions
- approved scope and duration
- Access Control Owner verification

### Stage-Specific Role

**Access Control Owner:** grants, removes, and verifies permissions against the approved minimum scope and duration.

### Permission Rules

Permissions must:

- support only the approved task
- use the minimum required scope
- use the minimum required duration
- exclude Production changes and external communication
- be verified by the Access Control Owner
- support required audit recording

### Outputs

- `READY`
- `BLOCKED`

A blocked result must identify:

- missing permissions
- excessive permissions
- next owner
- Resume Condition

### Stop Conditions

Stop when:

- a prohibited permission is granted
- scope or duration exceeds the requirement
- a required permission is missing
- permission verification is incomplete

### Workflow

1. Identify the authorized task.
2. Compare required and granted permissions.
3. Detect missing or excessive access.
4. Validate scope, duration, and owner verification.
5. Stop and escalate blocked access.
6. Resume only after the Resume Condition is verified.
7. Perform only the authorized task.

---

## Applied to This Case

### Case

The Platform AI supports the internal handling of a rate-limit request.

These test cases evaluate separate permission boundaries across the workflow. They are not sequential actions in one request.

### Actions

**Excessive rate-limit permission**

- Action: `STOP_EXCESSIVE_PERMISSION`
- Permission status: `BLOCKED`
- Excessive permission: `CHANGE_RATE_LIMIT`
- Next owner: `ACCESS_CONTROL_OWNER`
- Resume Condition: `EXCESSIVE_PERMISSIONS_REMOVED_AND_VERIFIED`

**Overbroad log permission**

- Action: `STOP_OVERBROAD_PERMISSION`
- Permission status: `BLOCKED`
- Missing permission: `READ_SANITIZED_ERROR_LOGS`
- Excessive permission: `READ_ALL_RAW_PRODUCTION_LOGS`
- Problem: scope and duration exceed the approved requirement
- Next owner: `ACCESS_CONTROL_OWNER`
- Resume Condition: `EXCESSIVE_PERMISSION_REMOVED_SCOPE_AND_DURATION_CORRECTED_AND_VERIFIED`

**Missing audit-write permission**

- Action: `STOP_MISSING_PERMISSION`
- Permission status: `BLOCKED`
- Missing permission: `APPEND_AUDIT_RECORD`
- Next owner: `ACCESS_CONTROL_OWNER`
- Resume Condition: `REQUIRED_PERMISSIONS_ADDED_TESTED_AND_VERIFIED`

**Minimum permissions verified**

- Action: `AUTHORIZE_MINIMUM_PERMISSION`
- Permission status: `READY`
- Routing: `PLATFORM_PARTNER_LEAD`
- Resume Condition: `NOT_REQUIRED`

### Test Result

| Test case | Expected result | Result |
|---|---|---|
| Excessive rate-limit permission | Stop and remove Production-change permission | Passed |
| Overbroad log permission | Stop and correct scope and duration | Passed |
| Missing audit-write permission | Stop and add append-only audit access | Passed |
| Minimum permissions verified | Authorize the defined internal task | Passed |

---

## Governance

Common governance requirements are defined in the [Shared Framework](../AGENTS.md#shared-framework-end-to-end-partner-workflow-days-41-50).

### Stage-Specific Audit Requirements

Record:

- authorized task
- required permissions
- granted permissions
- missing and excessive permissions
- approved scope and duration
- Access Control Owner
- verification result
- Resume Condition

### Human Review Points

A Human must confirm:

- permissions match the authorized task
- prohibited permissions were removed
- scope and duration are minimal
- append-only audit access works
- corrected permissions were verified before resumption

### Future Compatibility

The permission record can later support controlled access requests from a Partner AI Agent. Agent-to-Agent access is not implemented in Day 44.