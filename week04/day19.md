# Day19 - Technical Case Study: HTTP 401 Unauthorized

## 1. Executive Summary

This fictional case study describes a production API integration returning `HTTP 401 Unauthorized` for one partner after the partner migrated from a user-based authorization model to a server-to-server integration.

The evidence indicates that the access token itself is valid, not expired, and issued for the correct audience. The failure is caused by an authorization model mismatch: the integration is still requesting user-delegated scopes, while the platform now requires OAuth 2.0 client credentials for this integration type.

I recommended migrating the partner integration to OAuth 2.0 client credentials, with explicit partner onboarding steps, validation checks, and rollback-safe communication. Continuing with user-delegated authentication is not appropriate because there is no end user in the server-to-server flow, and it creates an authorization model that is harder to operate, audit, and scale.

## 2. Incident Context

**Confirmed facts:**

- A production API integration is returning `HTTP 401 Unauthorized` for one partner.
- The partner is sending a valid OAuth access token.
- The token is not expired.
- The token issuer and audience are correct.
- The partner recently migrated from a user-based authorization model to a server-to-server integration.
- The existing integration still requests user-delegated scopes.
- The platform now requires client-credentials authentication for this integration type.
- Requests are failing consistently in production.
- No other partners are affected.

**Assumptions:**

- The partner's application is now acting as a backend service rather than acting on behalf of a signed-in user.
- The authorization server can issue client-credentials tokens for this partner once the correct client configuration and scopes are in place.
- The partner can update its token acquisition flow without changing the API contract itself.

**Recommendation:**

- Move the integration to OAuth 2.0 client credentials and remove dependency on user-delegated scopes for this server-to-server use case.

## 3. Evidence Collected

I reviewed the failure pattern and separated token validity from authorization-model compatibility.

| Evidence | Interpretation |
|---|---|
| Valid OAuth access token | The request is authenticated at the token format and signature level. |
| Token is not expired | The failure is not caused by token lifetime. |
| Correct issuer and audience | The token is intended for the platform and trusted issuer. |
| User-delegated scopes still requested | The integration is using the old authorization model. |
| Client credentials now required | The platform expects application-level authorization. |
| One partner affected | The issue is scoped to this partner's integration configuration or migration state. |
| Consistent production failures | The issue is deterministic, not intermittent infrastructure instability. |

## 4. Root Cause

The root cause is an authorization model mismatch.

The partner migrated to a server-to-server integration but continued requesting user-delegated scopes. The platform requires OAuth 2.0 client credentials for this integration type, so the token can be valid while still being rejected for the requested access pattern.

Continuing with user-delegated authentication is not appropriate because server-to-server integrations do not represent a specific signed-in user. User-delegated scopes make access dependent on a user context that the integration no longer has, which weakens audit clarity, increases operational confusion, and does not scale well for backend partner workloads.

## 5. Solution Options

### Option A: Keep User-Delegated Authentication

Continue using the existing user-delegated scopes and attempt to adjust policy exceptions around the partner.

This is not recommended. It preserves the incompatible model and creates a special case that would be difficult to govern.

### Option B: Migrate to OAuth 2.0 Client Credentials

Update the partner integration to request a client-credentials token with application-level scopes approved for the server-to-server use case.

This is the recommended option because it aligns the partner integration with the required platform model.

### Option C: Temporary Compatibility Shim

Create a short-lived compatibility path that accepts the old delegated scope pattern while the partner completes migration.

This may reduce immediate partner disruption, but it adds operational risk and should only be considered if there is a time-bound migration blocker and explicit human approval.

## 6. Trade-off Analysis

| Option | Security | Implementation Effort | Scalability | Operational Risk | Partner Impact |
|---|---|---:|---|---|---|
| A. Keep user-delegated auth | Weak: preserves wrong trust model | Low | Poor | High: exception becomes long-lived | Low short-term, high long-term |
| B. Migrate to client credentials | Strong: matches server-to-server model | Medium | Strong | Medium during migration, low after | Medium short-term, positive long-term |
| C. Temporary compatibility shim | Medium to weak: controlled exception | High | Poor to medium | High: added policy surface | Low short-term, risky if extended |

I compared the options across security, implementation effort, scalability, operational risk, and partner impact. Option B is the best long-term path because it fixes the model mismatch instead of hiding it.

## 7. Technical Decision

I recommended migrating the integration to OAuth 2.0 client credentials.

The decision is based on these points:

- The token is valid, so the problem is not basic authentication failure.
- The integration type changed to server-to-server.
- The platform requires client credentials for this integration type.
- User-delegated scopes are no longer appropriate because the integration is not acting on behalf of an end user.
- A one-off exception would increase operational risk and reduce consistency across partner integrations.

## 8. My Direct Contribution

I identified the distinction between token validity and authorization-model compatibility.

I compared the available solution options and documented the trade-offs.

I recommended OAuth 2.0 client credentials as the correct target model.

I defined the evidence needed to confirm the migration path with the partner.

I reviewed the operational risks around temporary exceptions and recommended avoiding a long-lived compatibility path.

I did not claim sole ownership of implementation. The recommended migration would require coordination across partner engineering, API architecture, security review, platform operations, and the partner's technical team.

## 9. Implementation Plan

1. Confirm the partner's current token request uses user-delegated scopes.
2. Confirm the required application-level scopes for the server-to-server integration.
3. Register or update the partner client configuration for client credentials.
4. Provide the partner with the token endpoint, required scopes, and validation expectations.
5. Ask the partner to test client-credentials token acquisition in a non-production environment.
6. Validate that production requests use client-credentials tokens before switching production traffic.
7. Monitor `401` rates, token grant errors, and partner request success after migration.
8. Remove any temporary migration notes or exceptions after successful validation.

No operational action should be executed without the appropriate approval owner reviewing the change plan.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Partner implements the wrong OAuth grant type | Provide a short integration checklist and require evidence from a test token request. |
| Incorrect application-level scopes are assigned | Review scopes with API architecture and security before production use. |
| Production traffic remains on delegated scopes | Monitor token grant type and `401` rates during migration. |
| A temporary exception becomes permanent | Require an explicit expiry date and owner for any compatibility path. |
| Partner-facing communication overstates certainty | Separate confirmed facts from assumptions and recommendations in updates. |

## 11. Ownership and RACI

| Work Item | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Diagnose authorization model mismatch | Partner Engineering | Partner Engineering Lead | API Architect | Support |
| Approve client-credentials scope model | API Architect | Security / Platform Owner | Partner Engineering | Support |
| Update partner client configuration | Platform Operations | Platform Owner | Security, Partner Engineering | Partner |
| Implement partner token request change | Partner Technical Team | Partner Technical Lead | Partner Engineering | Support |
| Prepare partner communication | Platform Partnerships Manager | Partnerships Lead | Partner Engineering, Support | Partner |
| Monitor post-migration success | Platform Operations | Platform Owner | Partner Engineering | Support, Partner |

## 12. Measurable Impact

Proposed success metrics:

- Reduce affected partner `HTTP 401` responses to near zero after migration.
- Confirm production requests use the client-credentials grant type.
- Confirm no increase in authentication failures for other partners.
- Complete partner migration validation within the agreed incident response window.
- Document the final authorization model so future server-to-server partners use the same pattern.

These are proposed success metrics, not historical results.

## 13. Lessons Learned

- A valid token can still fail if the authorization model is wrong.
- Server-to-server integrations should use application-level authorization, not user-delegated scopes.
- Migration plans should explicitly verify grant type, scopes, issuer, audience, and production behavior.
- Temporary compatibility paths need ownership, expiry, and approval.
- Partner-facing updates should avoid claiming root cause until the evidence supports it.

## 14. Platform Builder View

This case study highlights a reusable platform pattern: separate authentication validity from authorization suitability.

For platform builders, the durable fix is not just to resolve one partner's `401` responses. The durable fix is to make the correct integration model obvious, testable, and repeatable:

- clear guidance for user-delegated versus client-credentials flows
- validation checks during partner onboarding
- logs that expose grant type and scope mismatches
- partner-facing migration checklists
- approval controls for high-risk or temporary exceptions

The recommended path is to migrate the partner to OAuth 2.0 client credentials and use this incident pattern to improve future server-to-server onboarding.