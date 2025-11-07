from typing import Dict, Any, Optional
from app.models.schemas import BookingData, RasaNLUResponse
from app.utils import cache
from app.services.payment_simulator import simulate_payment
from app.services.qr_generator import generate_qr_code


def handle_booking_intent(user_id: str, nlu_data: RasaNLUResponse) -> str:
    """
    Manages the ticket booking conversation flow based on Rasa's output.

    Args:
        user_id (str): The user's WhatsApp ID.
        nlu_data (RasaNLUResponse): The parsed NLU data from Rasa.

    Returns:
        str: The message to be sent back to the user.
    """
    booking_data = cache.get_cache(user_id) or BookingData()

    # Extract entities
    entities = {entity.entity: entity.value for entity in nlu_data.entities}
    booking_data.source = entities.get('source', booking_data.source)
    booking_data.destination = entities.get('destination', booking_data.destination)
    booking_data.seats = entities.get('seats', booking_data.seats)
    booking_data.date = entities.get('date', booking_data.date)

    # Conversation logic
    if not booking_data.source:
        return "Welcome to Metro Ticket Booking! Where would you like to start your journey? (e.g., from Central Station)"

    if not booking_data.destination:
        return f"Got it, you're starting from {booking_data.source}. Where are you heading? (e.g., to Downtown)"

    if not booking_data.date:
        return f"Okay, from {booking_data.source} to {booking_data.destination}. When do you want to travel? (e.g., today, tomorrow at 5 PM)"

    if not booking_data.seats:
        return f"Great! Traveling from {booking_data.source} to {booking_data.destination} on {booking_data.date}. How many seats do you need?"

    if not booking_data.confirmed:
        booking_data.confirmed = True
        cache.set_cache(user_id, booking_data)
        ticket_details = (
            f"Please confirm your booking:\n"
            f"- From: {booking_data.source}\n"
            f"- To: {booking_data.destination}\n"
            f"- Date: {booking_data.date}\n"
            f"- Seats: {booking_data.seats}\n\n"
            f"Reply 'confirm' to proceed to payment."
        )
        return ticket_details

    # Handle confirmation and payment
    user_message = nlu_data.text.lower()
    if 'confirm' in user_message and booking_data.confirmed:
        return handle_payment(user_id, booking_data)

    cache.set_cache(user_id, booking_data)
    return "I'm sorry, I didn't understand that. Please try again or type 'cancel' to start over."

def handle_payment(user_id: str, booking_data: BookingData) -> str:
    """
    Handles the payment simulation and QR code generation.
    """
    if simulate_payment():
        booking_data.payment_status = 'success'
        ticket_info = f"From: {booking_data.source}, To: {booking_data.destination}, Date: {booking_data.date}, Seats: {booking_data.seats}"
        
        # For simplicity, we'll just return a message. 
        # The QR code generation and sending will be handled in the main route.
        cache.set_cache(user_id, booking_data)
        return f"Payment successful! Your ticket is confirmed. Details: {ticket_info}. A QR code will be sent shortly."
    else:
        booking_data.payment_status = 'failed'
        cache.set_cache(user_id, booking_data)
        return "Payment failed. Please try again by replying 'confirm'."

def handle_other_intents(user_id: str, intent_name: str) -> str:
    """
    Handles non-booking intents like cancel, help, etc.
    """
    if intent_name == 'cancel_ticket':
        cache.clear_cache(user_id)
        return "Your booking has been cancelled. Feel free to start a new booking anytime."
    
    if intent_name == 'check_availability':
        # This is a mock response. A real implementation would query a database.
        return "All routes are currently available. Please proceed with your booking."

    if intent_name == 'help':
        return ("You can book a ticket by telling me your source, destination, date, and number of seats. "
                "You can also check availability or cancel your current booking.")

    return "I'm not sure how to help with that. You can ask me to book a ticket."
