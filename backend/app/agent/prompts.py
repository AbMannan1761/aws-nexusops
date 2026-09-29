"""
System prompts and Bedrock Agent Tool specifications for NexusOps.
"""

NEXUS_OPS_SYSTEM_PROMPT = """
You are NexusOps, an elite Autonomous Enterprise Operations and Dispatch Concierge powered by Amazon Bedrock and AWS Communication Developer Services (CDS).

Your core mission is to autonomously resolve high-stakes customer, field engineering, and enterprise operations incidents across multiple communication channels:
1. WhatsApp (AWS End User Messaging Social): Direct, immediate interaction with customers, field teams, or directors.
2. Amazon SES v2 (Simple Email Service): Formal audit trails, PDF/HTML incident executive summaries, and stakeholder escalation reports.
3. SMS / RCS (AWS End User Messaging SMS v2): High-priority transactional alerts, urgent OTPs, and field broadcast notices.

When responding to an incoming request:
1. Analyze the customer's identity, issue urgency, and business context.
2. Determine required autonomous actions:
   - Does a ticket exist? (Call `get_ticket_details` or `create_service_ticket`).
   - If resolving or updating an incident, send a formatted WhatsApp message back (`send_whatsapp_message`).
   - If an official record, invoice, or stakeholder notification is required, send an HTML email via SES (`send_ses_audit_email`).
   - If the situation is CRITICAL or requires instant verification, send an urgent SMS via Pinpoint SMS v2 (`send_sms_urgent_alert`).
3. Always maintain a professional, reassuring, and precise executive tone.
"""

BEDROCK_TOOLS_SPEC = [
    {
        "toolSpec": {
            "name": "send_whatsapp_message",
            "description": "Dispatches a rich conversational update to a customer or field engineer using AWS End User Messaging Social (WhatsApp) via boto3 socialmessaging SendWhatsAppMessage.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "recipient_phone": {
                            "type": "string",
                            "description": "Recipient international phone number (e.g., +12065550142)."
                        },
                        "message_body": {
                            "type": "string",
                            "description": "Interactive, clearly formatted message text to send to WhatsApp."
                        }
                    },
                    "required": ["recipient_phone", "message_body"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "send_ses_audit_email",
            "description": "Sends a formal HTML audit report, executive summary, or stakeholder incident notice using Amazon SES v2 via boto3 sesv2 send_email.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "recipient_emails": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of stakeholder emails."
                        },
                        "subject": {
                            "type": "string",
                            "description": "Subject line of the email."
                        },
                        "html_body": {
                            "type": "string",
                            "description": "Rich HTML content including incident overview, actions taken, and resolution metrics."
                        }
                    },
                    "required": ["recipient_emails", "subject", "html_body"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "send_sms_urgent_alert",
            "description": "Sends an urgent high-priority SMS alert or OTP verification to field operators via AWS End User Messaging SMS v2 (boto3 pinpoint-sms-voice-v2 SendTextMessage).",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "destination_phone": {
                            "type": "string",
                            "description": "The destination mobile number."
                        },
                        "message_body": {
                            "type": "string",
                            "description": "Short, high-priority transactional SMS text (under 160 chars)."
                        }
                    },
                    "required": ["destination_phone", "message_body"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "get_ticket_details",
            "description": "Fetches current operational status, logs, and telemetry history for a specific ticket ID.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ticket identifier, e.g. TICK-8041."
                        }
                    },
                    "required": ["ticket_id"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "update_ticket_status",
            "description": "Updates the operational state, notes, and priority of an ongoing incident.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ticket ID."
                        },
                        "new_status": {
                            "type": "string",
                            "enum": ["RESOLVED", "ESCALATED", "DISPATCHED", "PENDING_APPROVAL"],
                            "description": "New status for the ticket."
                        },
                        "resolution_notes": {
                            "type": "string",
                            "description": "Detailed notes on what actions were taken to remediate the issue."
                        }
                    },
                    "required": ["ticket_id", "new_status", "resolution_notes"]
                }
            }
        }
    }
]
