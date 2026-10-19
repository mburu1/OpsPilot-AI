# ADR-003: Evidence-grounded, provider-neutral AI

- **Status:** Specified by README; implementation unverified
- **Date:** 2026-10-19

## Context

Incident investigations can be high-impact. An LLM may produce plausible but unsupported root-cause explanations, and the platform must distinguish hypotheses from confirmed causes.

## Decision

Place model access behind provider adapters. Use retrieval-augmented generation (RAG), structured model outputs, source-linked evidence, validation of citation identifiers, prompt/model version metadata, and human review. Treat AI output as an unconfirmed hypothesis. Do not automatically execute production remediation.

## Consequences

- The domain workflow should remain useful when a model provider is unavailable.
- Model output is untrusted input and must be schema-validated and checked against authorized stored evidence.
- Prompt injection in imported documents, timeouts, rate limits, empty retrieval, and refusal cases need explicit handling.
- Retrieval and generation quality must be evaluated separately with a versioned benchmark.
- Reviewer feedback should be auditable.

## Verification required

Inspect provider adapters, prompt templates, structured-output validators, retrieval implementation, evaluation tests, and reviewer workflow. Provider names in the specification are examples, not a claim that all providers are integrated.
