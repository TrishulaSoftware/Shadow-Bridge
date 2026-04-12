# Shadow-Bridge: Core Definitions

This document establishes the deterministic terminology used within the Shadow-Bridge API and its sub-systems.

## █ TERMINOLOGY INDEX

### 1. The Guillotine
The **Guillotine** is the absolute magnitude sentiment filter. It is a deterministic threshold enforced by the `VetoEngine`.
- **Threshold**: `0.75`
- **Logic**: Any input where `abs(sentiment) < 0.75` is immediately "beheaded" (dropped) without further processing.

### 2. Kinetic Strike
A **Kinetic Strike** occurs when an inbound NLP payload survives the Guillotine and is successfully dispatched to the broker API.
- **Latency Target**: < 400ms.
- **Verification**: Order ID is captured and logged to the Paper Ledger.

### 3. Prose-Drift
**Prose-Drift** refers to any non-deterministic variation in the structure or data types of the API's ingestion layer. Shadow-Bridge utilizes **Pydantic v2** to enforce hard-typed schemas, effectively reaching zero-drift.

### 4. Institutional Magnitude
A metric of semantic force. Any sentiment score provided by a source (e.g., Bloomberg, Reuters) must represent a "High Conviction" signal, mapped to a -1.0 to 1.0 range, where only extremes are actionable.

### 5. Sovereign Egress
The process of synchronizing local execution state with the permanent GitHub upstream while ensuring bit-parity and auditability.

### 6. Veto Exception (`SentimentThresholdException`)
The standard error response (HTTP 422) returned when a sentiment payload fails the Guillotine. It is a non-retryable logical failure.

---
**PROPERTY OF TRISHULA SOFTWARE — LEVEL 5 SOVEREIGNTY ENFORCED**
