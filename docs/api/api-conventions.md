# API Conventions

> Status: Proposed REST API conventions for the intended Django REST Framework backend. Implemented routes, serializers, permissions, and tests remain the source of truth.

## General rules

- Use HTTPS outside local development.
- Use a versioned prefix, initially /api/v1/.
- Use resource-oriented nouns and standard HTTP methods.
- Use JSON and UTF-8 unless an endpoint documents another media type.
- Serialize timestamps as ISO 8601 with timezone information, normally UTC.
- Document authentication, permissions, validation, status codes, and side effects for every operation.
- Keep synchronous and asynchronous workflow semantics consistent.

## Methods and status codes

| Method | Semantics | Typical success |
|---|---|---|
| GET | Read resource or collection without state-changing side effects | 200 |
| POST | Create resource or initiate a job | 201 created resource; 202 accepted asynchronous work |
| PUT | Replace a representation when supported | 200 or 204 |
| PATCH | Partially update a representation | 200 or 204 |
| DELETE | Delete or deactivate according to documented retention rules | 204 |

Use 400 for invalid input, 401 for missing or invalid authentication, 403 for forbidden operations, 404 for unavailable resources, 405 for unsupported methods, 409 for state conflicts, 413 for oversized payloads, 415 for unsupported media types, 429 for rate limits, and 500/503 for unexpected or temporarily unavailable services. Do not disguise failures as successful responses.

## Validation and response shape

Validate input at the DRF serializer boundary and enforce business invariants in the service/domain layer. Set explicit limits for lengths, list sizes, uploads, pagination, and timeouts. Reject ambiguous or unsupported values where they could cause unsafe behavior. Frontend validation is not a security control.

Use a consistent response shape and error envelope across endpoints. An illustrative resource response:

    {
      "id": "inc_example",
      "status": "in_progress",
      "created_at": "2026-10-19T12:00:00Z"
    }

An illustrative error response:

    {
      "error": {
        "code": "validation_error",
        "message": "One or more fields are invalid.",
        "details": {"name": ["This field is required."]},
        "request_id": "req_example"
      }
    }

These examples are not implemented contracts. Decide and enforce the exact envelope consistently. Never return ORM objects directly, Python tracebacks, SQL statements, secrets, provider credentials, or raw provider exceptions.

## Collections, filtering, and pagination

Document filter names, types, operators, defaults, ordering, and maximum page size. Use allowlisted sort fields; never interpolate client-supplied sort values into SQL. Enforce tenant scope before filtering or pagination. Use stable ordering with a unique tie-breaker. Offset pagination may suit small collections; cursor pagination is preferable for large or frequently changing event streams.

## Asynchronous operations

Long-running investigations should be accepted as jobs rather than held open in a single HTTP request. A proposed flow is: submit a request, authorize and validate it, return 202 with a run/job ID and status URL, poll the status resource or subscribe to an authorized real-time channel, then fetch the report through a separately authorized endpoint.

Document state transitions, retry/cancellation behavior, and duplicate-submission semantics. Use idempotency keys where duplicate submissions would be harmful. Queue acceptance does not mean processing succeeded.

## Security and observability

Authenticate every non-public endpoint and enforce object-level permissions. Derive tenant scope from authenticated identity and verified membership, not an unchecked request field. Apply rate limits to expensive investigation, upload, search, and export operations. Validate upload size/type and storage behavior. Protect cookie-authenticated unsafe methods against CSRF. Configure CORS narrowly; CORS is not authentication.

Assign request/correlation IDs and propagate them to background jobs. Log route template, status, latency, and normalized failure category while excluding tokens, authorization headers, sensitive payloads, and full AI prompts by default.

## Versioning and tests

Prefer additive, backward-compatible changes. Treat removed/renamed fields, changed types or semantics, and incompatible status behavior as breaking changes. Document deprecations and update generated OpenAPI and client tests.

Required tests include serializer validation, object and tenant permissions, status/error schemas, pagination and ordering, idempotency and job state transitions, OpenAPI validation, and regressions for reported security issues.

## Source of truth

Generate the API contract from implemented DRF routes and review it against this guidance. Where code and documentation disagree, record and correct the discrepancy deliberately. Proposed routes in design documents must not be presented as existing endpoints.
