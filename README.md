# WhatsApp Metro Ticket Chatbot

This project is a complete, production-ready Python application that implements a WhatsApp-based Metro Ticket Booking Chatbot. It uses Twilio for WhatsApp communication, FastAPI for the backend, and Rasa for NLP.

## Features

- **Book Metro Tickets**: Users can book tickets through a conversational flow.
- **Simulated Payments**: A simulated payment process to confirm bookings.
- **QR Code Tickets**: Generates a QR code for the ticket (placeholder implementation).
- **Bilingual Support**: Easily extendable for bilingual messages.
- **Intent Recognition**: Uses Rasa for understanding user intents like `book_ticket`, `check_availability`, etc.

## Project Architecture

WhatsApp → Twilio Sandbox → FastAPI (webhook) → Rasa NLP → FastAPI logic → QR generation → Twilio reply → WhatsApp user

- **FastAPI**: Handles the main backend logic, including the Twilio webhook.
- **Rasa**: Provides NLU capabilities to understand user messages.
- **Twilio**: Manages the WhatsApp communication.
- **SQLite**: Used as a simple cache for booking data.
- **qrcode**: Python library for generating QR codes.

## Directory Structure

```
whatsapp_metro_bot/
│
├── app/                  # FastAPI application
│   ├── main.py           # Main FastAPI app file
│   ├── routes/           # API routes
│   │   └── whatsapp.py   # Webhook for Twilio
│   ├── services/         # Business logic
│   │   ├── rasa_client.py
│   │   ├── booking.py
│   │   ├── qr_generator.py
│   │   └── payment_simulator.py
│   ├── models/           # Pydantic schemas
│   │   └── schemas.py
│   └── utils/            # Utility functions
│       └── cache.py
│
├── rasa_server/          # Rasa NLU server configuration
│   ├── domain.yml
│   ├── config.yml
│   ├── credentials.yml
│   └── data/
│       ├── nlu.yml
│       └── stories.yml
│
├── requirements.txt      # Python dependencies
├── Procfile              # For Render deployment
├── runtime.txt           # Python runtime for Render
├── .env.example          # Example environment variables
├── README.md
└── LICENSE
```

## Setup and Deployment

### 1. Local Development

**Prerequisites:**
- Python 3.8+
- `ngrok` for exposing your local server to the internet.

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd whatsapp_metro_bot
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    - Copy `.env.example` to a new file named `.env`.
    - Fill in your Twilio Account SID, Auth Token, and Twilio WhatsApp phone number.

4.  **Train the Rasa NLU model:**
    ```bash
    cd rasa_server
    rasa train nlu
    cd ..
    ```

5.  **Run the Rasa server:**
    ```bash
    rasa run --enable-api --cors "*" --port 5005
    ```

6.  **Run the FastAPI server:**
    In a new terminal:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

7.  **Expose your local server with ngrok:**
    ```bash
    ngrok http 8000
    ```
    Copy the HTTPS forwarding URL provided by ngrok.

8.  **Configure Twilio Sandbox:**
    - Go to your Twilio console and navigate to the WhatsApp Sandbox.
    - In the sandbox configuration, set the webhook URL for "When a message comes in" to your ngrok URL, followed by `/whatsapp`.
      Example: `https://<your-ngrok-url>.ngrok.io/whatsapp`
    - Save the configuration.

9.  **Test the chatbot:**
    - Send a message to your Twilio WhatsApp number to start a conversation.

### 2. Deployment

#### Deploying the FastAPI Backend to Render

1.  **Push your code to a GitHub repository.**

2.  **Create a new Web Service on Render:**
    - Connect your GitHub repository.
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
    - **Environment Variables**:
        - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
        - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
        - `TWILIO_PHONE_NUMBER`: Your Twilio WhatsApp number.
        - `RASA_API_URL`: The URL of your deployed Rasa server (from the next step).

3.  **Deploy the service.** Render will provide you with a public URL for your backend.

#### Deploying the Rasa Server to Railway

1.  **Create a new project on Railway from your GitHub repository.**
    - When setting up the project, specify the `rasa_server` directory as the root.

2.  **Add a `Procfile` inside the `rasa_server` directory:**
    ```
    web: rasa run --enable-api --cors "*" --port $PORT
    ```

3.  **Add a `requirements.txt` inside the `rasa_server` directory:**
    ```
    rasa
    ```

4.  **Deploy the service.** Railway will provide a public URL for your Rasa server. Use this URL for the `RASA_API_URL` environment variable in your Render backend.

### 3. Final Configuration

- **Update Twilio Webhook**: Change the webhook URL in your Twilio Sandbox to your Render backend URL (`https://<your-render-app>.onrender.com/whatsapp`).
- **Uptime Monitoring**: Use a service like UptimeRobot to ping your Render and Railway URLs every 5-10 minutes to prevent them from sleeping on free tiers.
