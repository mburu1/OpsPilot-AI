# OpenAPI Specification

> Status: Proposed API documentation and validation workflow. OpenAPI must describe implemented routes; this repository's architecture documentation does not prove that schema or interactive-documentation endpoints already exist.

## Objectives and source of truth

Publish a versioned, machine-readable API contract that documents authentication, permissions, request and response schemas, errors, pagination, and asynchronous state transitions. Generate the schema from implemented Django/DRF routes, serializers, permissions, and view metadata using a maintained library compatible with pinned dependencies. A common option is drf-spectacular; choose and pin one library rather than maintaining duplicate schemas for the same endpoints.

Generated schema is a build artifact that requires review. Add annotations where automatic introspection cannot infer response variants, permissions, pagination, filters, or job-state transitions. Do not add invented routes simply to match a design document.

## Required metadata

Include API title, description, version, ownership/contact, non-secret server URLs, authentication requirements, resource tags, request/response schemas, error statuses, pagination/filtering behavior, fictional examples, and deprecation information. Keep API version separate from application package version and change it deliberately when compatibility changes.

## Authentication and documentation access

Describe the chosen security scheme accurately. For bearer-token deployments, document the HTTP bearer scheme and token expectations. For session-based browser access, document cookie/session behavior and CSRF requirements. OpenAPI security metadata does not enforce security by itself.

Suggested paths might be /api/schema/, /api/docs/, and /api/redoc/; these are examples, not claims that such routes currently exist. Decide whether the schema and interactive documentation are public, authenticated, staff-only, or published as a controlled release artifact. Never expose internal-only operations or sensitive configuration.

## Illustrative schema fragment

The following is an example only, not a complete OpsPilot API contract:

    openapi: 3.0.3
    info:
      title: OpsPilot AI API
      version: 1.0.0
      description: Proposed contract; verify against implemented routes.
    paths:
      /api/v1/health/:
        get:
          summary: Read service health
          operationId: getHealth
          responses:
            "200":
              description: Health information returned
            "503":
              description: Service unavailable

Use the version emitted by the selected generator if it differs. A health endpoint must not expose secrets, internal topology, or detailed dependency failures to anonymous callers.

## Validation and CI

Recommended workflow:

1. Install pinned application and schema dependencies.
2. Load test settings and generate schema from the application.
3. Validate syntax and OpenAPI structural rules.
4. Fail on unresolved references and invalid operation definitions.
5. Compare against the approved baseline to detect unexpected breaking changes.
6. Run contract tests for representative requests and responses.
7. Publish the reviewed schema as a build artifact where appropriate.

With drf-spectacular installed and configured, a command may resemble:

    python manage.py spectacular --file schema.yml --validate

Adapt this to the selected library and pinned version. CI should be deterministic and must not require production credentials.

## Contract quality checks

- Every operation has a stable operationId.
- Protected operations declare appropriate security requirements.
- Reusable request/response schemas are used where suitable.
- Error responses follow the API's standard error convention.
- Pagination/filter parameters have explicit types and bounds.
- Date/time formats, enums, optionality, and nullability match serializers.
- Examples are fictional and contain no secrets.
- Internal or undocumented routes are not accidentally published.
- Breaking changes receive review and release notes.

## Client generation and compatibility

Generate clients only from a reviewed schema, pin generator versions, and do not manually edit generated files. Removed or renamed fields, changed types, authentication changes, and changed semantics may be breaking. Compare schemas between releases and document compatibility impact.

## Security and release checklist

Schema generation should not execute user-supplied input or call external AI providers. Restrict documentation endpoints according to the deployment threat model. Do not expose environment values, stack traces, database details, provider keys, or internal hostnames.

- [ ] Schema generated from implemented routes and serializers.
- [ ] Authentication and permission metadata reviewed.
- [ ] Schema validates with the selected tool.
- [ ] Contract tests cover success and error paths.
- [ ] Breaking-change comparison reviewed.
- [ ] Examples contain no secrets or production-sensitive data.
- [ ] Documentation endpoint access policy verified.
- [ ] Published schema corresponds to the release commit.
