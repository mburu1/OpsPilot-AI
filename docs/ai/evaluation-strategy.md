# AI Evaluation Strategy

> Status: Proposed evaluation baseline. The repository describes a proposed platform; this document does not claim that an evaluation harness or benchmark is implemented.

## Purpose and principles

Measure the quality, safety, traceability, reliability, latency, and cost of AI-assisted incident investigation. Evaluate complete workflows as well as retrieval and generation separately. Prefer deterministic checks wherever correctness can be verified without a model. Keep benchmark cases versioned and representative, and never allow a high aggregate score to conceal a critical safety failure.

## Evaluation layers

| Layer | What to measure |
|---|---|
| Input normalization | Parsing, timestamps, service identifiers, tenant scope, missing fields |
| Retrieval | Recall@k, precision@k, source coverage, freshness, tenant exclusion |
| Grounded generation | Claim support, citation validity, contradiction and unsupported-claim rates |
| Diagnosis | Top-k accuracy where labels are defensible, reciprocal rank, uncertainty calibration |
| Reports | Required-field completeness, factual consistency, actionability |
| Reliability | Timeouts, retries, malformed output, provider outages, partial evidence |
| Safety | Prompt-injection resistance, secret exposure, unsafe recommendations, authorization failures |
| Operations | Latency percentiles, token usage when available, cost, retry and failure rates |

## Benchmark dataset

Maintain a versioned, access-controlled benchmark covering confirmed incidents, similar symptoms with different causes, incomplete or contradictory telemetry, stale runbooks, noisy and duplicated events, clock skew, prompt injection embedded in source data, cross-tenant isolation cases, provider failures, rate limits, and malformed structured output.

Each case should include an immutable ID, scenario, approved fixtures, expected evidence references, accepted diagnosis criteria, prohibited conclusions, and dataset version. Sanitize secrets and personal data. Restrict production-derived data and document its approval, access, and retention policy.

## Metrics and release gates

Choose metrics appropriate to each task. Measure retrieval quality, evidence-supported claims, invalid citations, diagnosis ranking, uncertainty and abstention quality, report completeness, critical safety failures, latency, and cost. Define numeric thresholds in versioned configuration after establishing a baseline; do not invent thresholds after observing results.

A release gate should require no critical safety regression, no cross-tenant disclosure, valid output against required schemas, and acceptable quality, latency, and cost relative to the current baseline. A critical security failure blocks release regardless of aggregate score.

## Experiment protocol

1. Pin dataset, code, prompt, retrieval settings, provider/model, and evaluator versions.
2. Run deterministic unit and contract checks.
3. Evaluate baseline and candidate on the same cases.
4. Report aggregate metrics and slices by incident type, evidence completeness, severity, and ambiguity.
5. Review material regressions against original source evidence.
6. Record results, limitations, and reproducible configuration.
7. Promote gradually, monitor production signals, and retain rollback capability.

For nondeterministic models, repeat selected cases and report variance. Record model identifiers, prompt hashes, generation settings, retrieval configuration, timestamps, and sanitized outputs.

## Human review and failure taxonomy

Review evidence relevance, claim support, uncertainty, diagnosis usefulness, and proportionality of recommendations. Reviewers must be able to inspect source evidence. User feedback is a signal, not automatically ground truth; require adjudication before changing benchmark labels.

Classify failures as retrieval miss, unsupported inference, hidden contradiction, poor calibration, schema violation, unsafe instruction following, data disclosure, authorization breach, or provider/orchestration failure. Record reproducible case, severity, suspected cause, remediation owner, and retest result.

## Reporting and implementation checklist

Evaluation reports should contain dataset and code versions, provider/model identifiers, prompt and retrieval versions, metric definitions, aggregate and slice results, critical failures, latency/cost, reviewer notes, and release recommendation.

- [ ] Versioned benchmark fixtures and schemas.
- [ ] Deterministic metrics and regression tests.
- [ ] Retrieval and citation evaluators.
- [ ] Human-review rubric and adjudication process.
- [ ] Bounded CI smoke benchmark and scheduled full evaluation.
- [ ] Redacted, access-controlled evaluation artifacts.
- [ ] Explicit release gates and rollback procedure.

These are recommendations until verified in application code and CI configuration.
