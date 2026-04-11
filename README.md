# 🛡️ SHADOW-BRIDGE API v1.0
### The Deterministic Ingestion Middleware

The **Shadow-Bridge API** is a high-density commercial middleware designed to translate institutional NLP sentiment into deterministic broker execution. By enforcing the **Trishula Doctrine (SQA_v5)**, it eliminates probabilistic drift in agency-based trading.

## █ THE GUILLOTINE (Veto Logic)
The core of the Shadow-Bridge is the **Sentiment Threshold**. All inbound payloads are subjected to a absolute magnitude audit:

- **Authorized Strike**: `abs(sentiment_score) >= 0.75`
- **VETOed Strike**: `abs(sentiment_score) < 0.75`

Any payload falling below this threshold triggers an immediate `SentimentThresholdException` (HTTP 422), halting execution before any broker calls are initiated.

## █ ARCHITECTURE
- **Ingress**: FastAPI (Asynchronous, High-Performance)
- **Validation**: Pydantic v2 (Hard-Typed Schemas)
- **Logic**: Stateless Veto Engine with Abstract Execution Interface
- **latency**: < 400ms Hard-Cap for Broker calls

## █ DEPLOYMENT

### Docker (Commercial Standard)
```bash
docker build -t trishula-shadow-bridge .
docker run -p 8000:8000 trishula-shadow-bridge
```

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## █ SQA_v5 VERIFICATION
The bridge includes a deterministic test suite proving the threshold logic under adversarial inputs.

```bash
pytest tests/test_veto_engine.py
```

## █ API USAGE

### POST `/ingest/nlp`
**Payload Schema**:
```json
{
  "source": "Bloomberg",
  "pair": "EUR_USD",
  "sentiment_score": 0.85
}
```

**Response (Success)**:
```json
{
  "status": "AUTHORIZED",
  "execution": {
    "status": "SUCCESS",
    "broker": "OANDA",
    "order_id": "SB-123456789",
    "latency_ms": 112
  }
}
```

---
**PROPERTY OF TRISHULA SOFTWARE — LEVEL 5 SOVEREIGNTY ENFORCED**
