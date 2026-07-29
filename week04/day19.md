# Day 19: Technical Decision Case Study

## HTTP 401 Unauthorized in a Server-to-Server Integration

## Objective

Use AI to support technical diagnosis and compare solution options while keeping the final recommendation and accountability with the human decision-maker.

---

## Scenario

A partner's production API requests are consistently returning `HTTP 401 Unauthorized`.

The partner recently changed from a user-based authorization model to a server-to-server integration.

Confirmed facts:

- The OAuth access token is valid and not expired
- The issuer and audience are correct
- No other partners are affected
- The integration still requests user-delegated scopes
- The platform requires client credentials for this integration type

---

## Evidence and Interpretation

| Evidence | Interpretation |
|---|---|
| Valid, unexpired token | The issue is not basic token validity |
| Correct issuer and audience | The token is intended for the correct platform |
| User-delegated scopes remain | The old authorization model is still being used |
| Server-to-server integration | Application-level authorization is required |
| Only one partner affected | The issue is likely partner-specific |
| Failures are consistent | The issue is deterministic, not intermittent |

---

## Root Cause

The root cause is an authorization-model mismatch.

The partner migrated to a server-to-server integration but continued using user-delegated scopes.

The token is valid, but it does not match the authorization model required for this integration type.

---

## Options and Trade-offs

| Option | Benefit | Risk |
|---|---|---|
| Keep user-delegated authentication | Low short-term effort | Preserves the wrong trust model and creates a long-term exception |
| Migrate to OAuth 2.0 client credentials | Correct, scalable server-to-server model | Requires partner migration effort |
| Add a temporary compatibility path | Reduces immediate disruption | Adds security, governance, and operational risk |

---

## Recommendation

My recommendation is to migrate the integration to OAuth 2.0 client credentials.

This option:

- matches the server-to-server use case
- removes dependency on user context
- improves audit clarity
- avoids a long-lived partner exception
- creates a scalable pattern for future integrations

A temporary compatibility path should be considered only if there is a confirmed migration blocker, a defined owner, and an explicit expiry date.

---

## Next Actions

1. Confirm the partner's current grant type and requested scopes
2. Define the required application-level scopes
3. Update the partner's client configuration
4. Test token acquisition outside production
5. Validate production traffic after migration
6. Monitor `401` rates and token grant failures

---

## Human Review Points

Before accepting an AI-generated diagnosis, confirm:

- whether the evidence is complete
- whether the issue is authentication or authorization
- whether the problem is partner-specific or platform-wide
- whether the recommended scopes follow least-privilege principles
- whether any temporary exception has an owner and expiry date

AI can help structure the diagnosis, but technical and security owners must validate the final change.

---

## Measurable Outcome

Success would mean:

- partner `401` responses are reduced to near zero
- production requests use client credentials
- no other partners are affected
- the correct authorization pattern is documented for future onboarding

---

## Platform Learning

A valid token can still fail when the authorization model is wrong.

The durable platform response is not only to fix one partner's incident, but also to make the correct integration model clear and repeatable through:

- onboarding guidance
- grant-type and scope validation
- useful authentication logs
- migration checklists
- controls for temporary exceptions

---

## Plain-English Summary

The partner had a valid token, but it was using the wrong type of authorization.

The correct fix is to move the server-to-server integration to OAuth 2.0 client credentials.

AI helped organize the evidence and compare the options.

The human decision-maker validated the recommendation and owned the outcome.