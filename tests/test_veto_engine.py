"""
SQA_v5 TEST SUITE — SHADOW-BRIDGE
Deterministic Verification of the Veto Engine.
"""

import pytest
from logic.veto_engine import VetoEngine, NLPSentimentSchema, AbstractExecutionArm, ExecutionOrderSchema
from logic.exceptions import SentimentThresholdException

# --- MOCK BROKER ---

class MockExecutionArm(AbstractExecutionArm):
    def __init__(self):
        self.executed = False
        self.last_order = None

    def execute_strike(self, order: ExecutionOrderSchema) -> dict:
        self.executed = True
        self.last_order = order
        return {"status": "MOCK_SUCCESS", "pair": order.pair}

# --- TESTS ---

def test_veto_guillotine_rejects_weak_sentiment():
    """Verify abs(score) < 0.75 is REJECTED."""
    mock_broker = MockExecutionArm()
    engine = VetoEngine(broker=mock_broker)
    
    # 0.74 should fail
    payload = NLPSentimentSchema(source="Bloomberg", pair="EUR_USD", sentiment_score=0.74)
    
    with pytest.raises(SentimentThresholdException):
        engine.process_nlp_ingestion(payload)
    
    assert mock_broker.executed is False

def test_veto_guillotine_accepts_strong_sentiment():
    """Verify abs(score) >= 0.75 is AUTHORIZED."""
    mock_broker = MockExecutionArm()
    engine = VetoEngine(broker=mock_broker)
    
    # +0.75 should pass (BUY)
    payload = NLPSentimentSchema(source="Bloomberg", pair="EUR_USD", sentiment_score=0.75)
    result = engine.process_nlp_ingestion(payload)
    
    assert result["status"] == "MOCK_SUCCESS"
    assert mock_broker.executed is True
    assert mock_broker.last_order.action == "BUY"

def test_veto_guillotine_bearish_strike():
    """Verify negative high sentiment results in SELL."""
    mock_broker = MockExecutionArm()
    engine = VetoEngine(broker=mock_broker)
    
    # -0.80 should pass (SELL)
    payload = NLPSentimentSchema(source="Reuters", pair="GBP_USD", sentiment_score=-0.80)
    result = engine.process_nlp_ingestion(payload)
    
    assert mock_broker.last_order.action == "SELL"
    assert mock_broker.last_order.sentiment_audit == -0.80

def test_pydantic_validation_fails_on_bad_data():
    """Verify schema level validation."""
    with pytest.raises(ValueError):
        # Invalid pair pattern
        NLPSentimentSchema(source="Bloomberg", pair="NOT_A_PAIR", sentiment_score=0.85)

if __name__ == "__main__":
    pytest.main([__file__])
