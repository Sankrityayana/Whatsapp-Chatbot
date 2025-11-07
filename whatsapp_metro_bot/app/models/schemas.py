from pydantic import BaseModel
from typing import List, Optional

class TwilioMessage(BaseModel):
    """
    Pydantic model to validate incoming Twilio webhook data.
    """
    From: str  # e.g., 'whatsapp:+14155238886'
    To: str
    Body: str
    MessageSid: str
    AccountSid: str

class RasaNLURequest(BaseModel):
    """
    Pydantic model for the request sent to Rasa NLU.
    """
    text: str
    message_id: Optional[str] = None

class RasaIntent(BaseModel):
    """
    Pydantic model for a single intent from Rasa NLU response.
    """
    name: str
    confidence: float

class RasaEntity(BaseModel):
    """
    Pydantic model for a single entity from Rasa NLU response.
    """
    entity: str
    start: int
    end: int
    confidence_entity: Optional[float] = None
    value: str
    extractor: str

class RasaNLUResponse(BaseModel):
    """
    Pydantic model for the full response from Rasa NLU.
    """
    text: str
    intent: RasaIntent
    entities: List[RasaEntity] = []
    intent_ranking: List[RasaIntent] = []

class BookingData(BaseModel):
    """
    Pydantic model for storing temporary booking information in the cache.
    """
    source: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seats: Optional[int] = None
    confirmed: bool = False
    payment_status: Optional[str] = None
