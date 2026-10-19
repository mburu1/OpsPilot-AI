# API Authentication and Authorization

> Status: Proposed security design for Django and Django REST Framework. Verify actual settings, authentication classes, permissions, middleware, routes, and tests before claiming controls are active.

## Objectives

Identify callers reliably, enforce least privilege and object-level authorization, isolate tenants across HTTP and asynchronous workflows, protect credentials, support revocation, and audit security-relevant events. Authentication alone does not authorize access to a resource.

## Choose an authentication model

For a first-party browser application on a trusted site, Django session authentication with secure, HttpOnly cookies is a strong default. Enable CSRF protection for unsafe methods and configure cookie scope and SameSite behavior for the actual deployment.

For separate SPA or API clients, use a maintained OAuth 2.0/OpenID Connect identity provider or vetted token implementation. Define issuer, audience, expiry, key rotation, roles/scopes, refresh, and revocation behavior. Avoid storing long-lived credentials in browser local storage where possible. Do not invent a custom token format or implement cryptography by hand. Record the final choice in an ADR.

## Authentication behavior

Protected endpoints reject missing, malformed, expired, or invalid credentials. Return 401 for missing/invalid authentication and 403 for an authenticated caller lacking permission. Do not reveal token contents, signing details, or sensitive account state in errors. Public endpoints must be explicitly designated. Administrative access should use strong identity controls, including MFA through the identity system where available.

For bearer tokens, validate signature, issuer, audience, expiry, and permitted algorithms with a maintained library. Never accept unsigned or algorithm-confused tokens. For session authentication, configure secure cookies, CSRF middleware, and trusted origins correctly.

## Authorization model

Use deny-by-default permissions and action-specific checks. Example roles are illustrative and require product approval:

| Role | Intended access |
|---|---|
| Platform administrator | Platform configuration and explicitly privileged support operations |
| Tenant administrator | Users and configuration within their tenant |
| Incident responder | Investigate incidents permitted by tenant policy |
| Read-only auditor | Read permitted incident records and audit history |

Do not rely on role names alone. Check capabilities such as view, create, investigate, export, manage membership, and approve remediation. High-impact operations require explicit permission and independent approval.

## Tenant isolation

Resolve tenant scope from the authenticated identity and a verified membership or authorized resource relationship. A client-provided tenant identifier is a selector, not proof of access. Enforce scope in DRF querysets and detail lookups, create/update validation, service rules, PostgreSQL/vector retrieval, Celery task processing, cache keys, idempotency records, report downloads, exports, Channels subscriptions, attachments, and audit records.

Avoid unscoped object retrieval followed by an assumption of authorization. Centralized scoping helpers are useful but must be covered by tests. Database row-level security may add defense in depth when its operational behavior is understood and tested.

## Background tasks and real-time updates

Queue messages should carry a stable run/task ID and minimum required context. Workers must not blindly trust tenant IDs from queue messages; verify the initiating request and re-check access where membership or permissions may have changed. Authenticate Channels connections and authorize each subscription. Use tenant-scoped group names, avoid global broadcasts of sensitive progress, and revoke access when policy requires it.

## Secrets, rate limits, and transport

Keep signing keys, provider tokens, and database credentials out of source control and client bundles. Use environment configuration or a managed secret store, separate secrets by environment, and document rotation. Never place credentials in URLs. Apply throttling to authentication, investigation creation, uploads, search, and export. Use generic recovery/login responses where detailed responses could enable account enumeration.

Require HTTPS in deployed environments. Configure CORS to explicit trusted origins; never combine wildcard origins with credentials. For cookie auth, enforce CSRF and appropriate secure cookie flags. CORS is not access control.

## Audit and logging

Record security-relevant authentication outcomes, permission denials, membership changes, privileged configuration updates, credential rotation, and remediation approvals. Include actor, tenant scope, timestamp, action, target ID, outcome, and correlation ID where appropriate. Never log passwords, raw tokens, session cookies, or full authorization headers. Restrict audit-log access and define retention.

## Required tests

- Anonymous requests cannot access protected resources.
- Invalid and expired credentials are rejected.
- Users cannot access another tenant's objects by changing identifiers.
- List, detail, mutation, retrieval, export, and report endpoints enforce consistent tenant scope.
- Permissions are enforced independently of UI visibility.
- CSRF/CORS/cookie or bearer-token behavior matches the chosen model.
- Background jobs and real-time subscriptions preserve authorization.
- Secrets do not appear in logs or errors.
- Revocation behaves according to documented policy.

## Implementation checklist

- [ ] Select session or token-based authentication and document the decision.
- [ ] Configure DRF authentication and permission classes explicitly.
- [ ] Define user, tenant, and membership lifecycle rules.
- [ ] Implement object-level authorization and tenant-scoped querysets.
- [ ] Configure HTTPS, CSRF/CORS, throttling, and secret management.
- [ ] Test API, worker, retrieval, cache, channel, export, and report boundaries.
- [ ] Verify recovery, revocation, audit, and incident-response procedures before production.
