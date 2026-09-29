"""
Executable tool functions invoked by the Amazon Bedrock Agent.
Directly routes calls to AWS CDS services (WhatsApp, SES, Pinpoint SMS v2) and DB.
"""

import logging
from typing import Dict, Any
from datetime import datetime
from app.cds.whatsapp_client import whatsapp_client
from app.cds.ses_client import ses_client
from app.cds.sms_client import sms_client
from app.services.db_service import db

logger = logging.getLogger(__name__)

def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatcher for tools requested by the Agent.
    """
    logger.info(f"Executing Agent Tool: {tool_name} with args: {args}")

    if tool_name == "send_whatsapp_message":
        recipient = args.get("recipient_phone")
        body = args.get("message_body")
        res = whatsapp_client.send_text_message(recipient, body)
        db.add_audit_log(
            "CDS_WHATSAPP_SEND",
            f"WhatsApp message dispatched to {recipient}",
            {"body": body, "result": res}
        )
        return res

    elif tool_name == "send_ses_audit_email":
        recipients = args.get("recipient_emails", [])
        subject = args.get("subject", "NexusOps Incident Report")
        html_body = args.get("html_body", "<p>NexusOps Incident Summary</p>")
        res = ses_client.send_audit_or_report_email(recipients, subject, html_body)
        db.add_audit_log(
            "CDS_SES_SEND",
            f"SES v2 email '{subject}' sent to {recipients}",
            {"subject": subject, "result": res}
        )
        return res

    elif tool_name == "send_sms_urgent_alert":
        phone = args.get("destination_phone")
        body = args.get("message_body")
        res = sms_client.send_urgent_sms(phone, body)
        db.add_audit_log(
            "CDS_SMS_SEND",
            f"Pinpoint SMS v2 alert sent to {phone}",
            {"body": body, "result": res}
        )
        return res

    elif tool_name == "get_ticket_details":
        ticket_id = args.get("ticket_id")
        ticket = db.get_ticket(ticket_id)
        if ticket:
            return {"status": "FOUND", "ticket": ticket.dict()}
        else:
            return {"status": "NOT_FOUND", "message": f"No ticket found matching {ticket_id}."}

    elif tool_name == "update_ticket_status":
        ticket_id = args.get("ticket_id")
        new_status = args.get("new_status")
        notes = args.get("resolution_notes")
        ticket = db.get_ticket(ticket_id)
        if ticket:
            ticket.status = new_status
            ticket.details += f"\n[Update {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}]: {notes}"
            ticket.updated_at = datetime.utcnow().isoformat()
            db.create_or_update_ticket(ticket)
            db.add_audit_log(
                "TICKET_STATUS_UPDATED",
                f"Ticket {ticket_id} updated to {new_status}",
                {"notes": notes}
            )
            return {"status": "UPDATED", "ticket": ticket.dict()}
        else:
            return {"status": "ERROR", "message": f"Ticket {ticket_id} not found."}

    else:
        return {"status": "ERROR", "message": f"Unknown tool: {tool_name}"}
