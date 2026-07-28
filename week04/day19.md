# Day19 - Technical Case Study: HTTP 401 Unauthorized

## 1. Executive Summary

This fictional case study describes a production API integration returning `HTTP 401 Unauthorized` for one partner after the partner migrated from a user-based authorization model to a server-to-server integration.

The evidence indicates that the access token itself is valid, not expired, and issued for the correct audience. The failure is caused by an authorization model mismatch: the integration is still requesting user-delegated scopes, while the platform now requires OAuth 2.0 client credentials for this integration type.

I recommended direct migration to OAuth 2.0 client credentials as the target-state solution. I rejected a permanent policy exception because it would preserve an unsupported authentication pattern, and I rejected gateway-side token exchange for this scenario because the added platform complexity was not justified by the scope of impact.

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
- The authorization server can issue client-credentials tokens for this partner after the correct client registration and scopes are configured.
- The partner can update its token acquisition flow without changing the API contract itself.

**Recommendation:**

- Migrate the integration to OAuth 2.0 client credentials and remove dependency on user-delegated scopes for this server-to-server use case.

## 3. Evidence Collected

I reviewed the failure pattern and separated token validity from authorization-model compatibility.

| Evidence | Interpretation |
|---|---|
| Valid OAuth access token | The request is authenticated at the token format and signature level. |
| Token is not expired | The failure is not caused by token lifetime. |
| Correct issuer and audience | The token is intended for the platform and trusted issuer. |
| User-delegated scopes still requested | The integration is using the previous authorization model. |
| Client credentials now required | The platform expects application-level authorization. |
| One partner affected | The issue is scoped to this partner's migration state or client configuration. |
| Consistent production failures | The issue is deterministic, not intermittent infrastructure instability. |

HTTP status codes depend on platform implementation. In many systems, `HTTP 401` usually indicates missing, invalid, or unacceptable authentication credentials, while `HTTP 403` usually indicates valid authentication with insufficient permission. However, some platforms return `HTTP 401` when the token's grant type, authentication model, or authorization context is not accepted for the endpoint. In this scenario, the platform rejects the token because the authorization model is not valid for the server-to-server integration. I would not claim that `401` is universally correct for this condition; the exact status code depends on how the platform separates authentication and authorization enforcement.

## 4. Root Cause

### Working Root-Cause Hypothesis

The strongest evidence points to an authorization-model mismatch. The partner's token appears valid, but the integration is using user-delegated scopes for a server-to-server workflow that requires OAuth 2.0 client credentials.

Final confirmation requires verification of:

- token grant type
- issued scopes
- client registration type
- endpoint-required scopes
- authorization server logs
- API gateway or resource-server logs
- failing request correlation ID

**Confirmed facts at this stage:**

- The token is valid and not expired.
- Issuer and audience are correct.
- The partner is still requesting user-delegated scopes.
- The endpoint now requires client-credentials authentication for this integration type.

**Assumption at this stage:**

- The rejected request is failing because the grant model and scope model are incompatible with the endpoint's required authorization context.

**Recommendation at this stage:**

- Continue investigation against grant type, scopes, client registration, endpoint policy, and resource-server logs before making production changes.

### Confirmed Root Cause

After verifying the token grant type, issued scopes, client registration type, endpoint-required scopes, authorization server logs, API gateway or resource-server logs, and the failing request correlation ID, the confirmed cause is the continued use of user-delegated authorization for an integration that now requires OAuth 2.0 client credentials.

Continuing with user-delegated authentication is not appropriate because server-to-server integrations do not represent a specific signed-in user. User-delegated scopes make access dependent on a user context that the integration no longer has, which weakens audit clarity, increases support burden, and does not scale well for backend partner workloads.

## 5. Solution Options

### Option A: Direct Migration to OAuth 2.0 Client Credentials

Migrate the partner integration to request a client-credentials token with application-level scopes approved for the server-to-server use case.

- **Security implications:** Strong alignment with the intended server-to-server trust model and least-privilege application scopes.
- **Implementation effort:** Medium. Requires partner token-flow changes and platform client configuration.
- **Scalability:** Strong. Establishes the same model for future server-to-server partners.
- **Operational risk:** Medium during migration, low after cutover.
- **Partner impact:** Requires partner implementation work but creates a stable long-term pattern.
- **Long-term maintainability:** Strong. This is the target-state solution.

### Option B: Time-Limited Compatibility Window

Temporarily permit the legacy user-delegated model while the partner completes migration.

- **Security implications:** Acceptable only as a controlled exception with explicit constraints.
- **Implementation effort:** Medium. Requires policy exception handling, monitoring, and expiry controls.
- **Scalability:** Weak if repeated across partners.
- **Operational risk:** Medium to high because temporary exceptions can become permanent without ownership.
- **Partner impact:** Low short-term disruption, but it still requires migration.
- **Long-term maintainability:** Weak unless strictly time-boxed.

Option B may be used only as a tightly controlled temporary migration measure with an explicit expiration date, owner, monitoring, and rollback conditions.

### Option C: Gateway-Side Token Exchange or Authentication Broker

Introduce a gateway-side token exchange or authentication broker that converts the partner's existing token into a platform-approved application token.

- **Security implications:** Adds security boundaries and increases token-lifecycle responsibility for the platform.
- **Implementation effort:** High. Requires broker design, token exchange policy, audit logging, failure handling, and operational ownership.
- **Scalability:** Potentially useful as a broader platform capability, but excessive for a single-partner issue.
- **Operational risk:** High because the platform becomes responsible for more token transformation and policy enforcement.
- **Partner impact:** Lower partner-side change, because the partner may keep more of its current flow.
- **Long-term maintainability:** Weak for this case unless there is a wider platform-level requirement.

Option C may reduce partner-side changes, but it increases platform complexity, token-lifecycle responsibility, audit requirements, and the number of security boundaries. I would reject it for this scenario unless a broader platform-level requirement justifies the additional architecture.

## 6. Trade-off Analysis

| Option | Security | Implementation Effort | Scalability | Operational Risk | Partner Impact | Long-Term Maintainability |
|---|---|---:|---|---|---|---|
| A. Direct migration to client credentials | Strong: matches server-to-server model and least privilege | Medium | Strong | Medium during migration, low after cutover | Medium short-term change | Strong |
| B. Time-limited compatibility window | Medium: controlled temporary exception | Medium | Weak if repeated | Medium to high | Low short-term disruption | Weak unless strictly temporary |
| C. Gateway-side token exchange or broker | Mixed: can centralize control but adds security boundaries | High | Medium only if reused platform-wide | High | Low partner-side change | Weak for a one-partner issue |

I compared the options across security, implementation effort, scalability, operational risk, partner impact, and long-term maintainability. Option A is the strongest target-state solution because it fixes the authorization model mismatch directly. Option B is acceptable only as a short-lived migration bridge. Option C is not appropriate for this case because it creates platform complexity that is not justified by one affected partner.

## Decision Criteria

I selected the recommendation against these criteria:

1. Security model alignment
2. Least-privilege access
3. Auditability
4. Partner implementation effort
5. Platform scalability
6. Operational support burden
7. Migration reversibility
8. Long-term maintainability

Option A best satisfies the decision criteria because it aligns the integration with the required server-to-server security model, provides clearer auditability, scales to future partners, and avoids a permanent exception path.

## 7. Technical Decision

I recommended direct migration to OAuth 2.0 client credentials.

The decision is based on these points:

- The token is valid, so the problem is not basic authentication failure.
- The integration type changed to server-to-server.
- The platform requires client credentials for this integration type.
- User-delegated scopes are no longer appropriate because the integration is not acting on behalf of an end user.
- A permanent policy exception would increase operational risk and create an unsupported authentication pattern.
- Gateway-side token exchange would add complexity, audit requirements, and security boundaries that are not justified for this scoped incident.

Recommended target state:

- Partner uses OAuth 2.0 client credentials.
- Partner receives application-level scopes approved for the integration.
- Resource-server authorization checks validate application scopes rather than user-delegated scopes.
- Monitoring confirms the old user-delegated token path is no longer used after cutover.

## 8. My Direct Contribution

I identified that the incident was being treated as a token-validity problem, while the evidence pointed to a grant-model mismatch. This reframed the investigation from "is the token valid?" to "is this token acceptable for this endpoint and integration type?"

I redirected the investigation toward grant type, issued scopes, client registration, endpoint-required scopes, authorization server logs, resource-server authorization logs, and the failing request correlation ID. This created a concrete evidence path to confirm or reject the working hypothesis.

I compared direct migration, a temporary compatibility window, and gateway-side token exchange. This made the decision more explicit than simply choosing the fastest short-term workaround.

I recommended rejecting a permanent policy exception because it would create an unsupported authentication pattern and increase long-term support burden.

I defined migration acceptance criteria, rollback triggers, monitoring requirements, and the ownership model. This helped convert the technical recommendation into an executable plan without adding action execution capability to the workflow.

I reviewed the proposed implementation with the API Architect, Security Owner, Platform Operations, and the partner's technical team. I did not claim sole implementation ownership; the migration requires coordinated execution across platform and partner teams.

## 9. Implementation Plan

1. Confirm the partner's current token request uses user-delegated scopes.
2. Confirm token grant type, issued scopes, client registration type, and endpoint-required scopes.
3. Review authorization server logs, API gateway logs, resource-server logs, and the failing request correlation ID.
4. Confirm required application-level scopes for the server-to-server integration.
5. Register or update the partner client configuration for client credentials.
6. Provide the partner with the token endpoint, required scopes, and validation expectations.
7. Ask the partner to test client-credentials token acquisition in a non-production environment.
8. Validate that production requests use client-credentials tokens before switching production traffic.
9. Monitor `401` and `403` rates, token grant errors, grant type, audience, scopes, and partner request success after migration.
10. Remove any temporary compatibility exception after successful validation.

Rollback triggers:

- token acquisition failure above an agreed threshold
- unexpected increase in `HTTP 401` or `HTTP 403` responses
- scope or audience mismatch
- downstream authorization regression
- impact to previously unaffected partners

Rollback would return the integration to the approved temporary compatibility state, not to an indefinite legacy model.

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Partner implements the wrong OAuth grant type | Provide a token-flow checklist and require evidence from a test token request. |
| Incorrect application-level scopes are assigned | Review scopes with the API Architect and Security Owner before production use. |
| Production traffic remains on delegated scopes | Monitor grant type and reject unexpected delegated-token use after final cutover. |
| A temporary exception becomes permanent | Require an explicit expiry date, owner, monitoring, and rollback conditions. |
| Gateway-side token exchange is selected for convenience | Require architecture and security approval and reject it unless there is a broader platform requirement. |
| Partner-facing communication overstates certainty | Separate confirmed facts, assumptions, hypotheses, and recommendations in updates. |
| Rollback becomes indefinite legacy support | Restrict rollback to the approved temporary compatibility state with a defined end date. |

## 11. Ownership and RACI

| Work Item | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Incident coordination | Technical Partner Manager | Platform Owner | Internal Partner Engineer, Platform Operations | Support, Partner Technical Team |
| Evidence collection | Technical Partner Manager | Platform Owner | API Architect, Security Owner, Platform Operations | Partner Technical Team |
| Decision facilitation | Technical Partner Manager | Platform Owner | API Architect, Security Owner, Internal Partner Engineer | Partner Technical Team |
| Authentication model approval | API Architect, Security Owner | Platform Owner | Technical Partner Manager, Platform Operations | Partner Technical Team |
| Partner-facing execution planning | Technical Partner Manager | Platform Owner | Internal Partner Engineer, Partner Technical Team | Support |
| Partner token-flow implementation | Partner Technical Team | Partner Technical Team | Technical Partner Manager, API Architect | Platform Operations |
| Platform client configuration | Platform Operations | Platform Owner | API Architect, Security Owner | Technical Partner Manager |
| Post-migration monitoring | Platform Operations | Platform Owner | Technical Partner Manager, Internal Partner Engineer | Partner Technical Team |

The Technical Partner Manager is responsible for incident coordination, evidence collection, decision facilitation, and partner-facing execution planning. The Technical Partner Manager is not solely responsible for technical implementation.

## 12. Measurable Impact

Proposed acceptance criteria:

- 99.9% or higher successful authenticated request rate over 24 hours after cutover.
- Zero use of user-delegated tokens after final cutover.
- Zero authentication regressions for previously unaffected partners.
- All temporary exceptions removed within five business days.
- Runbook, onboarding guidance, and monitoring dashboards updated before incident closure.
- Production `HTTP 401` and `HTTP 403` rates remain within agreed thresholds after migration.
- Partner confirms successful production calls using the client-credentials grant type.

These are proposed acceptance criteria, not historical results.

## 13. Lessons Learned

- A valid token can still fail if the grant model or authorization context is not accepted by the endpoint.
- `HTTP 401` and `HTTP 403` behavior depends on platform implementation; teams should inspect the authentication and authorization enforcement path before assuming meaning from the status code alone.
- Server-to-server integrations should use application-level authorization, not user-delegated scopes.
- Migration plans should explicitly verify grant type, scopes, issuer, audience, client registration, endpoint policy, and production behavior.
- Temporary compatibility paths need ownership, expiry, monitoring, and rollback criteria.
- Partner-facing updates should avoid claiming confirmed root cause until the evidence supports it.

## 14. Platform Builder View

This case study highlights a reusable platform pattern: separate authentication validity from authorization suitability.

For platform builders, the durable fix is not just to resolve one partner's `401` responses. The durable fix is to make the correct integration model obvious, testable, and repeatable:

- clear guidance for user-delegated versus client-credentials flows
- onboarding checks for grant type, scopes, client registration, issuer, and audience
- logs that expose grant type, scope mismatch, endpoint-required scopes, and correlation IDs
- partner-facing migration checklists
- approval controls for high-risk or temporary exceptions
- dashboards that distinguish authentication failures from authorization-model failures

The recommended path is to migrate the partner to OAuth 2.0 client credentials and use this case pattern to improve future server-to-server onboarding.
