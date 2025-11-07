import os
import requests
from typing import Optional
from dotenv import load_dotenv
from app.models.schemas import RasaNLUResponse

load_dotenv()

RASA_API_URL = os.getenv("RASA_API_URL", "http://localhost:5005/model/parse")

def get_rasa_nlu_response(text: str) -> Optional[RasaNLUResponse]:
    """
    Sends a text message to the Rasa NLU server to get intent and entities.

    Args:
        text (str): The user's message.

    Returns:
        Optional[RasaNLUResponse]: A Pydantic model of the Rasa response, or None on error.
    """
    try:
        response = requests.post(RASA_API_URL, json={"text": text})
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return RasaNLUResponse(**data)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing Rasa response: {e}")
        return None
