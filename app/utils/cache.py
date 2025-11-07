import sqlite3
import json
from typing import Optional
from app.models.schemas import BookingData

DB_PATH = './whatsapp_metro_bot_cache.db'

def init_cache():
    """
    Initializes the SQLite database and creates the cache table if it doesn't exist.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS booking_cache (
                user_id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def set_cache(user_id: str, data: BookingData):
    """
    Saves or updates booking data for a given user_id in the cache.

    Args:
        user_id (str): The user's WhatsApp number.
        data (BookingData): The booking data to cache.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO booking_cache (user_id, data) VALUES (?, ?)",
            (user_id, data.json())
        )
        conn.commit()

def get_cache(user_id: str) -> Optional[BookingData]:
    """
    Retrieves booking data for a given user_id from the cache.

    Args:
        user_id (str): The user's WhatsApp number.

    Returns:
        Optional[BookingData]: The cached booking data, or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM booking_cache WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return BookingData(**json.loads(row[0]))
    return None

def clear_cache(user_id: str):
    """
    Deletes booking data for a given user_id from the cache.

    Args:
        user_id (str): The user's WhatsApp number.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM booking_cache WHERE user_id = ?", (user_id,))
        conn.commit()
