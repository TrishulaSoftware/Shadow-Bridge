"""
VETO ENGINE v1.0 — SHADOW-BRIDGE
Deterministic Logic & Pydantic v2 Schemas.
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator
import logging
from .exceptions import SentimentThresholdException

logger = logging.getLogger(__name__)

# --- SCHEMAS (PYDANTIC v2) ---

class NLPSentimentSchema(BaseModel):
    source: str = Field(..., description="Institutional source (e.g., Bloomberg)")
    pair: str = Field(..., pattern="^[A-Z]{3}_[A-Z]{3}$")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    
    @field_validator('sentiment_score')
    @classmethod
    def enforce_threshold(cls, v: float) -> float:
        """THE GUILLOTINE: Enforce abs(sentiment) >= 0.75."""
        if abs(v) < 0.75:
            # Note: We'll raise the custom exception in the logic layer to handle FastAPI 422 vs 500
            pass
        return v

class ExecutionOrderSchema(BaseModel):
    pair: str
    action: str
    units: int
    sentiment_audit: float

# --- BROKER ABSTRACTION ---

class AbstractExecutionArm(ABC):
    @abstractmethod
    def execute_strike(self, order: ExecutionOrderSchema) -> dict:
        """Mandatory kinetic interface."""
        pass

# --- LOGIC LAYER ---

class VetoEngine:
    def __init__(self, broker: AbstractExecutionArm):
        self.broker = broker

    def process_nlp_ingestion(self, payload: NLPSentimentSchema) -> dict:
        """The Deterministic Path."""
        score = payload.sentiment_score
        
        # 1. THE GUILLOTINE
        if abs(score) < 0.75:
            logger.warning(f"Veto Triggered: Sentiment {score} failed threshold.")
            raise SentimentThresholdException(f"Sentiment score {score} is below the 0.75 threshold.")
            
        # 2. MAP ACTION
        action = "BUY" if score > 0 else "SELL"
        
        # 3. CONSTRUCT ORDER
        order = ExecutionOrderSchema(
            pair=payload.pair,
            action=action,
            units=10000, # Hard-coded for commercial draft
            sentiment_audit=score
        )
        
        # 4. EXECUTE KINETICS
        return self.broker.execute_strike(order)
