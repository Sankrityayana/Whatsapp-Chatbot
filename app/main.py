from fastapi import FastAPI
from app.routes import whatsapp
from app.utils.cache import init_cache

app = FastAPI(
    title="WhatsApp Metro Ticket Chatbot",
    description="A chatbot for booking metro tickets via WhatsApp.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """
    Initialize the database cache on application startup.
    """
    init_cache()

# Include the WhatsApp webhook router
app.include_router(whatsapp.router, tags=["WhatsApp"])

@app.get("/", tags=["Health Check"])
async def root():
    """
    Health check endpoint to confirm the server is running.
    """
    return {"status": "ok", "message": "WhatsApp Chatbot is running"}
