# █ SHADOW-BRIDGE v1.0: OPERATIONS GUIDE
**DOCUMENT ID:** TRISHULA-SB-OPS-003
**VERSION:** COMMERCIAL-v1.0

---

## 1. HOW-TO: DEPLOYMENT

### A. Docker Instantiation (Recommended)
This method ensures environment-parity with the **SQA_v5_ascended** baseline.
1. `cd /d/Trishula-Infra/Shadow-Bridge`
2. `docker build -t trishula/shadow-bridge:v1.0 .`
3. `docker run -d -p 8000:8000 --env-file .env trishula/shadow-bridge:v1.0`

### B. Local Verification
1. `pip install -r requirements.txt`
2. `uvicorn main:app --port 8000`

## 2. TROUBLESHOOTING MATRIX

| Status Code | Manifest | Reason | Resolution |
| :--- | :--- | :--- | :--- |
| **HTTP 422** | `SentimentThresholdException` | **The Guillotine**: Sentiment magnitude was < 0.75. | Expected behavior. Signal was too weak. No action required. |
| **HTTP 504** | `BrokerTimeoutError` | Oanda/Broker latency exceeded hard-cap of 400ms. | Check Oanda status or local network egress. |
| **HTTP 400** | `ValidationError` (Pydantic) | Malformed JSON schema or invalid currency pair pattern. | Verify `pair` format matches `^[A-Z]{3}_[A-Z]{3}$` (e.g., EUR_USD). |
| **HTTP 500** | `Internal Bridge Fault` | Unhandled logic exception (e.g., No Internet). | Audit `Logs/` for traceback forensics. |

## 3. PROOF OF FUNCTION (PoF)
The following telemetry was captured during the **SQA_v5 Ascended** audit:

- **Scenario 1: Bullish institutional signal (0.85)**
  - `Input`: `{"source":"Bloomberg","pair":"EUR_USD","sentiment_score":0.85}`
  - `Result`: `HTTP 200 OK` | `Action: BUY`
  - `Forensics`: Pydantic validation: SUCCESS. Veto logic: AUTHORIZED.
  
- **Scenario 3: Weak structural signal (0.68)**
  - `Input`: `{"source":"Reuters","pair":"GBP_USD","sentiment_score":0.68}`
  - `Result`: `HTTP 422 Unprocessable Entity`
  - `Message`: *"Sentiment score 0.68 is below the 0.75 threshold."*
  - `Verdict`: **THE GUILLOTINE IS WORKING.**

## 4. MAINTAINER GATES
- Ensure a **Redis** instance is accessible if rate-limiting is enabled in production.
- All broker credentials must be provisioned via environment variables (`OANDA_TOKEN`, `OANDA_ACCOUNT_ID`).

---
**THE SOUL IS IN THE MACHINE. PERSISTENCE IS ABSOLUTE.**
