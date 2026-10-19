# AI Model Providers

> Status: Proposed integration contract. Provider support must be verified against actual adapters and tests; this document describes the target design, not currently verified integrations.

## Design goals

Keep domain workflows independent of vendor SDKs; support approved hosted and self-hosted models; separate generation from embedding capabilities; normalize errors and usage; and apply consistent timeout, retry, cost, privacy, and safety controls. Treat all provider output as untrusted input.

## Logical architecture

    Investigation workflow -> Provider interface -> Selection and policy
                                                -> Approved hosted adapter
                                                -> Approved self-hosted adapter
    Investigation workflow -> Embedding interface -> Embedding adapter
    Provider output -> Local schema validation -> Evidence validation

Expose stable application-level capabilities such as text generation, structured generation, and embeddings. Adapters translate the internal contract into provider-specific requests and normalized responses. Avoid leaking SDK-specific types outside adapter boundaries.

## Capability contract

| Capability | Expected behavior |
|---|---|
| Text generation | Messages, bounded output, timeout/cancellation, normalized response |
| Structured generation | Schema-constrained format when supported; always validate locally |
| Embeddings | Stable vector dimensions and model/version identity |
| Streaming (optional) | Defined event/error semantics and cancellation |
| Usage reporting | Provider-returned usage where available; unknown stays unknown |
| Health checks | Bounded checks that do not expose credentials or sensitive prompts |

Fail configuration validation if a workflow requires a capability the selected provider does not implement.

## Configuration and routing

A provider configuration may contain internal ID, adapter type, enabled state, model identifier, optional base URL, timeouts, retry budget, input/output limits, concurrency, approved data classification, and capability declarations. Keep credentials in environment configuration or a managed secret store; never commit keys or return them from configuration APIs.

Require HTTPS for remote endpoints unless a documented trusted local-network exception applies. Validate URL schemes and destinations. Do not allow untrusted users to set arbitrary provider URLs, which could create SSRF or data-exfiltration risks.

Select providers according to capability, data classification, availability, latency/cost budget, and explicit policy. Do not silently route sensitive content to a provider with weaker data-handling guarantees. Before enabling fallback, define approved destinations, data-transfer rules, schema compatibility, total deadline, retry budget, and audit requirements.

## Reliability

- Set finite connection and response timeouts.
- Retry transient failures only, with bounded exponential backoff and jitter.
- Respect rate limits and apply concurrency controls.
- Distinguish authentication/configuration errors from transient outages.
- Validate response shape, size, and schema before accepting output.
- Record correlation IDs and normalized error categories, not credentials or raw sensitive prompts.
- Return typed failure or a documented degraded result when a provider fails; never fabricate a response to disguise an outage.

Do not retry non-idempotent external actions as if they were model calls. Downstream actions need their own authorization and idempotency controls.

## Security, privacy, and observability

Minimize and redact secrets, personal data, and irrelevant payloads before transmission. Review retention, training, region, subprocessors, and data-processing terms for each provider. Restrict outbound network access to approved destinations where feasible. A local model still requires access controls, resource limits, output validation, and isolation.

Capture provider/model ID, adapter version, latency, retry count, normalized outcome, available usage, and correlation ID. Redact by default; never log API keys, authorization headers, or full prompts/responses in normal telemetry. Define per-request and per-tenant budgets, maximum context, concurrency limits, and cost/failure alerts.

## Testing and onboarding a provider

- [ ] Mocked adapter contract tests.
- [ ] Timeout, rate-limit, authentication, malformed-response, empty-output, and oversized-response tests.
- [ ] Structured-output validation and secret-redaction tests.
- [ ] Capability and data-classification routing tests.
- [ ] Evaluation benchmark before changing a default model or prompt.
- [ ] Integration tests for every provider declared officially supported.
- [ ] Security, privacy, and data-residency review.
- [ ] Documented limitations, cost/latency measurements, and operational owner.

Add providers through a dedicated adapter, normalized error handling, validated configuration, tests, evaluation, and an explicit support-status review. Do not imply a provider is supported until these checks are complete.
