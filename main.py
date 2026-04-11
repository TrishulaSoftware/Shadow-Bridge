"""
MAIN v1.0 — SHADOW-BRIDGE API
FastAPI Gateway for Institutional NLP Ingestion.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import time
from logic.veto_engine import VetoEngine, NLPSentimentSchema, AbstractExecutionArm, ExecutionOrderSchema
from logic.exceptions import SentimentThresholdException, BrokerTimeoutError

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [SHADOW-BRIDGE] %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Shadow-Bridge API", version="1.0.0")

# --- CONCRETE BROKER IMPLEMENTATION ---

class OandaExecutionArm(AbstractExecutionArm):
    def __init__(self, token, account_id):
        self.token = token
        self.account_id = account_id

    def execute_strike(self, order: ExecutionOrderSchema) -> dict:
        """Simulated Oanda execution for commercial draft."""
        start = time.time()
        # Simulated Network Latency
        time.sleep(0.1) 
        
        if (time.time() - start) > 0.4:
            raise BrokerTimeoutError("Oanda response exceeded 400ms threshold.")
            
        return {
            "status": "SUCCESS",
            "broker": "OANDA",
            "order_id": f"SB-{int(time.time())}",
            "instrument": order.pair,
            "latency_ms": int((time.time() - start) * 1000)
        }

# Initializing Engine
# Token/Account should be env vars in production
broker = OandaExecutionArm(token="MASKED", account_id="MASKED")
engine = VetoEngine(broker=broker)

# --- ROUTES ---

@app.post("/ingest/nlp")
async def ingest_nlp(payload: NLPSentimentSchema):
    """Primary ingestion path for institutional sentiment."""
    try:
        result = engine.process_nlp_ingestion(payload)
        return {"status": "AUTHORIZED", "execution": result}
    except SentimentThresholdException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BrokerTimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    except Exception as e:
        logger.error(f"Internal Bridge Fault: {e}")
        raise HTTPException(status_code=500, detail="Internal Sovereign Error")

@app.get("/status")
async def get_status():
    return {"status": "ONLINE", "version": "1.0.0", "core": "TRISHULA_DOCTRINE"}

# --- EXCEPTION HANDLERS ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred in the Shadow-Bridge."},
    )
