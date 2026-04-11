"""
SHADOW-BRIDGE EXCEPTIONS
Deterministic Error Definitions.
"""

class TrishulaException(Exception):
    """Base exception for all Shadow-Bridge faults."""
    pass

class SentimentThresholdException(TrishulaException):
    """Raised when absolute sentiment score is below 0.75."""
    pass

class BrokerTimeoutError(TrishulaException):
    """Raised when broker API response exceeds 400ms constraint."""
    pass

class DataDissonanceError(TrishulaException):
    """Raised when inbound parity check fails."""
    pass
