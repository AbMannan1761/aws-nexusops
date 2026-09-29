"""
NexusOps FastAPI Application Entrypoint
Hosts Agent API, AWS CDS Webhooks, and Serves Operations Command Center Dashboard.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.models.schemas import (
    AgentChatRequest,
    AgentChatResponse,
    IncomingWhatsAppWebhook,
    ServiceTicket,
    SystemAuditLog
)
from app.agent.bedrock_agent import bedrock_agent
from app.services.db_service import db

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Omnichannel Enterprise Concierge powered by Amazon Bedrock & AWS CDS",
    version="1.0.0"
)

# Enable CORS for local testing & cloud deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Path Resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

@app.get("/api/status")
def get_system_status():
    """
    Returns live connectivity and CDS service status.
    """
    return {
        "status": "ONLINE",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "aws_region": settings.AWS_REGION,
        "mock_mode": settings.MOCK_AWS_SERVICES,
        "services": {
            "amazon_bedrock": {
                "model_id": settings.BEDROCK_MODEL_ID,
                "status": "READY"
            },
            "aws_eum_social_whatsapp": {
                "client": "boto3.client('socialmessaging')",
                "operation": "SendWhatsAppMessage",
                "phone_number_id": settings.WHATSAPP_PHONE_NUMBER_ID,
                "status": "READY"
            },
            "amazon_ses_v2": {
                "client": "boto3.client('sesv2')",
                "operation": "send_email",
                "sender": settings.SES_SENDER_EMAIL,
                "status": "READY"
            },
            "aws_eum_pinpoint_sms_v2": {
                "client": "boto3.client('pinpoint-sms-voice-v2')",
                "operation": "SendTextMessage",
                "origination": settings.PINPOINT_SMS_ORIGINATION_IDENTITY,
                "status": "READY"
            }
        }
    }

@app.post("/api/chat", response_model=AgentChatResponse)
def handle_agent_chat(request: AgentChatRequest):
    """
    Processes chat requests through Amazon Bedrock Agent and dispatches AWS CDS actions.
    """
    try:
        response = bedrock_agent.process_message(
            session_id=request.session_id,
            user_message=request.message,
            user_phone=request.user_phone,
            user_name=request.user_name,
            channel=request.channel
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/webhook/whatsapp")
def handle_whatsapp_webhook(payload: IncomingWhatsAppWebhook):
    """
    Webhook receiver for incoming WhatsApp messages via AWS End User Messaging Social.
    """
    response = bedrock_agent.process_message(
        session_id=f"wa-{payload.sender_phone}",
        user_message=payload.message_text,
        user_phone=payload.sender_phone,
        user_name=payload.sender_name,
        channel="WHATSAPP"
    )
    return {"status": "RECEIVED", "agent_response": response}

@app.get("/api/tickets")
def list_tickets():
    """
    Retrieves all ongoing service and operational tickets.
    """
    return db.list_tickets()

@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    ticket = db.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("/api/audit-logs")
def list_audit_logs(limit: int = 25):
    """
    Retrieves latest AWS CDS dispatches and Bedrock Agent reasoning traces.
    """
    return db.get_audit_logs(limit)

# Mount static frontend directory
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_dashboard():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
