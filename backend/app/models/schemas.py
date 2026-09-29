from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class IncomingWhatsAppWebhook(BaseModel):
    sender_phone: str
    sender_name: str = "Client"
    message_text: str
    timestamp: Optional[str] = None
    media_url: Optional[str] = None

class AgentChatRequest(BaseModel):
    session_id: str = "demo-session-001"
    user_phone: str = "+12065550142"
    user_name: str = "Sarah Jenkins (Director of Ops)"
    message: str
    channel: str = "WHATSAPP"  # WHATSAPP | SMS | WEB

class AgentToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None

class AgentTraceStep(BaseModel):
    step_number: int
    thought: str
    tool_calls: List[AgentToolCall] = []
    output_message: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class AgentChatResponse(BaseModel):
    session_id: str
    response_text: str
    channel: str
    traces: List[AgentTraceStep] = []
    cds_dispatches: List[Dict[str, Any]] = []

class ServiceTicket(BaseModel):
    ticket_id: str
    customer_name: str
    customer_phone: str
    customer_email: str
    category: str  # e.g., "Field Outage", "Equipment Replacement", "VIP Billing"
    priority: str  # "CRITICAL", "HIGH", "NORMAL"
    status: str    # "DISPATCHED", "RESOLVED", "PENDING_APPROVAL"
    summary: str
    details: str
    created_at: str
    updated_at: str

class SystemAuditLog(BaseModel):
    id: str
    event_type: str  # "BEDROCK_INFERENCE", "CDS_WHATSAPP_SEND", "CDS_SES_SEND", "CDS_SMS_SEND"
    description: str
    metadata: Dict[str, Any]
    timestamp: str
