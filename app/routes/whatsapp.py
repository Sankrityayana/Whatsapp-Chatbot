import os
from fastapi import APIRouter, Form, Depends
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

from app.services import rasa_client, booking
from app.models.schemas import BookingData
from app.utils import cache
from app.services.qr_generator import generate_qr_code_in_memory

load_dotenv()

router = APIRouter()

# Twilio client initialization
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to: str, message: str, media_url: str = None):
    """Sends a message via Twilio WhatsApp API."""
    try:
        message_args = {
            'from_': TWILIO_PHONE_NUMBER,
            'body': message,
            'to': to
        }
        if media_url:
            message_args['media_url'] = media_url
        
        client.messages.create(**message_args)
    except Exception as e:
        print(f"Error sending Twilio message: {e}")

@router.post("/whatsapp")
def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    """
    Webhook endpoint for receiving WhatsApp messages from Twilio.
    """
    user_id = From
    user_message = Body

    # Get NLU response from Rasa
    nlu_data = rasa_client.get_rasa_nlu_response(user_message)

    if not nlu_data:
        send_whatsapp_message(user_id, "Sorry, I'm having trouble understanding. Please try again later.")
        return MessagingResponse().to_xml()

    intent_name = nlu_data.intent.name
    response_message = ""

    if intent_name == 'book_ticket' or (nlu_data.intent.confidence < 0.8 and not cache.get_cache(user_id)):
        response_message = booking.handle_booking_intent(user_id, nlu_data)
    else:
        response_message = booking.handle_other_intents(user_id, intent_name)

    send_whatsapp_message(user_id, response_message)

    # Check if payment was successful and send QR code
    booking_data = cache.get_cache(user_id)
    if booking_data and booking_data.payment_status == 'success':
        # This is a simplified version. In a real app, you'd likely use a more robust way 
        # to handle media URLs, perhaps by uploading the QR to a cloud storage service.
        # For this example, we assume a publicly accessible URL can be constructed.
        ticket_info = f"From:{booking_data.source},To:{booking_data.destination},Date:{booking_data.date},Seats:{booking_data.seats}"
        
        # We can't directly send an in-memory file. A real implementation would need to:
        # 1. Save the QR code to a file.
        # 2. Upload it to a service like S3 or a temporary public folder.
        # 3. Get a public URL for the image.
        # 4. Send that URL in the media_url parameter.
        # For this example, we will just send another text message as a placeholder.
        send_whatsapp_message(user_id, f"[Placeholder for QR Code for ticket: {ticket_info}]")
        cache.clear_cache(user_id) # Clean up after successful booking

    return MessagingResponse().to_xml()
