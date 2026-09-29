"""
Generates high-resolution PNG and PDF architecture diagrams for Devpost submission.
Avoids SVG mime-type issues on Devpost's file uploader.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PNG_PATH = os.path.join(DOCS_DIR, "architecture_diagram.png")
PDF_PATH = os.path.join(DOCS_DIR, "architecture_diagram.pdf")

def generate_diagram_image():
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(9, 13, 22))
    draw = ImageDraw.Draw(img)

    # Accent top border
    draw.rectangle([0, 0, width, 8], fill=(56, 189, 248))

    # Header
    draw.text((80, 50), "AWS NexusOps — System Architecture", fill=(248, 250, 252))
    draw.text((80, 95), "Autonomous Omnichannel Enterprise Concierge | Amazon Bedrock AgentCore & AWS CDS", fill=(148, 163, 184))
    draw.line([80, 135, width - 80, 135], fill=(40, 55, 80), width=2)

    # ================= COLUMN 1: CLIENT CHANNELS =================
    c1_x, c1_y, c1_w, c1_h = 80, 160, 400, 840
    draw.rectangle([c1_x, c1_y, c1_x + c1_w, c1_y + c1_h], fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.rectangle([c1_x, c1_y, c1_x + c1_w, c1_y + 50], fill=(20, 30, 48))
    draw.text((c1_x + 20, c1_y + 15), "1. CLIENT & FIELD CHANNELS", fill=(56, 189, 248))

    # Card 1.1: WhatsApp Mobile
    draw.rectangle([c1_x + 20, c1_y + 80, c1_x + c1_w - 20, c1_y + 240], fill=(17, 24, 39), outline=(34, 197, 94), width=2)
    draw.text((c1_x + 40, c1_y + 100), "WhatsApp Mobile (Field Engineers)", fill=(34, 197, 94))
    draw.text((c1_x + 40, c1_y + 140), "• Conversational incident intake\n• Telemetry alert triage\n• Ingress: AWS SocialMessaging Webhook", fill=(203, 213, 225), spacing=10)

    # Card 1.2: Executive Email
    draw.rectangle([c1_x + 20, c1_y + 270, c1_x + c1_w - 20, c1_y + 430], fill=(17, 24, 39), outline=(56, 189, 248), width=2)
    draw.text((c1_x + 40, c1_y + 290), "Executive Stakeholder Email", fill=(56, 189, 248))
    draw.text((c1_x + 40, c1_y + 330), "• Formal incident post-mortems\n• Executive regulatory summaries\n• Ingress: Amazon SES v2 notifications", fill=(203, 213, 225), spacing=10)

    # Card 1.3: Mobile SMS Device
    draw.rectangle([c1_x + 20, c1_y + 460, c1_x + c1_w - 20, c1_y + 620], fill=(17, 24, 39), outline=(245, 158, 11), width=2)
    draw.text((c1_x + 40, c1_y + 480), "Mobile SMS Handset", fill=(245, 158, 11))
    draw.text((c1_x + 40, c1_y + 520), "• Urgent high-priority broadcast\n• 2FA site-override credentials\n• Delivery via Pinpoint SMS v2", fill=(203, 213, 225), spacing=10)

    # Card 1.4: Web Operations Console
    draw.rectangle([c1_x + 20, c1_y + 650, c1_x + c1_w - 20, c1_y + 810], fill=(17, 24, 39), outline=(168, 85, 247), width=2)
    draw.text((c1_x + 40, c1_y + 670), "Operations Command Center", fill=(168, 85, 247))
    draw.text((c1_x + 40, c1_y + 710), "• Live 3-column power console\n• Real-time Bedrock ReAct trace visualizer\n• Interactive WhatsApp & SES inboxes", fill=(203, 213, 225), spacing=10)


    # ================= COLUMN 2: BEDROCK AGENTCORE BRAIN =================
    c2_x, c2_y, c2_w, c2_h = 540, 160, 780, 840
    draw.rectangle([c2_x, c2_y, c2_x + c2_w, c2_y + c2_h], fill=(15, 23, 42), outline=(124, 58, 237), width=2)
    draw.rectangle([c2_x, c2_y, c2_x + c2_w, c2_y + 50], fill=(30, 20, 60))
    draw.text((c2_x + 20, c2_y + 15), "2. AGENTIC BRAIN: AMAZON BEDROCK AGENTCORE", fill=(192, 132, 252))

    # Box 2.1: Cognitive ReAct Loop
    draw.rectangle([c2_x + 30, c2_y + 80, c2_x + c2_w - 30, c2_y + 260], fill=(17, 24, 39), outline=(71, 85, 105), width=1)
    draw.text((c2_x + 50, c2_y + 100), "Cognitive Reasoning Engine (Amazon Bedrock Converse API)", fill=(248, 250, 252))
    draw.text((c2_x + 50, c2_y + 140), "• Foundation Model: Anthropic Claude 3.5 Sonnet (anthropic.claude-3-5-sonnet-20240620-v1:0)\n• Multi-turn Converse Loop: Autonomous evaluation of intent, incident severity, and operational risk\n• ReAct Execution: Interleaved Thought-Action-Observation trace generation", fill=(203, 213, 225), spacing=12)

    # Box 2.2: Autonomous Tool Dispatcher
    draw.rectangle([c2_x + 30, c2_y + 290, c2_x + c2_w - 30, c2_y + 560], fill=(17, 24, 39), outline=(71, 85, 105), width=1)
    draw.text((c2_x + 50, c2_y + 310), "Autonomous Tool Orchestrator & Dispatch Layer", fill=(248, 250, 252))
    
    # Tool 1
    draw.rectangle([c2_x + 50, c2_y + 355, c2_x + c2_w - 50, c2_y + 405], fill=(20, 35, 30), outline=(34, 197, 94), width=1)
    draw.text((c2_x + 70, c2_y + 370), "Tool: send_whatsapp_message  ->  AWS SocialMessaging.SendWhatsAppMessage", fill=(34, 197, 94))

    # Tool 2
    draw.rectangle([c2_x + 50, c2_y + 420, c2_x + c2_w - 50, c2_y + 470], fill=(15, 30, 45), outline=(56, 189, 248), width=1)
    draw.text((c2_x + 70, c2_y + 435), "Tool: send_ses_audit_email  ->  Amazon SES v2.send_email", fill=(56, 189, 248))

    # Tool 3
    draw.rectangle([c2_x + 50, c2_y + 485, c2_x + c2_w - 50, c2_y + 535], fill=(35, 28, 15), outline=(245, 158, 11), width=1)
    draw.text((c2_x + 70, c2_y + 500), "Tool: send_sms_urgent_alert  ->  AWS Pinpoint SMS v2.SendTextMessage", fill=(245, 158, 11))

    # Box 2.3: State Store & Audit Table
    draw.rectangle([c2_x + 30, c2_y + 590, c2_x + c2_w - 30, c2_y + 800], fill=(17, 24, 39), outline=(71, 85, 105), width=1)
    draw.text((c2_x + 50, c2_y + 610), "Amazon DynamoDB Memory & Incident Store", fill=(248, 250, 252))
    draw.text((c2_x + 50, c2_y + 650), "• Tickets Table: Partition Key (ticket_id), lifecycle states (INVESTIGATING, RESOLVED)\n• System Audit Table: Immutable logs of all CDS dispatches & cryptographic receipts\n• Session Memory: Preserves conversational context across WhatsApp turns\n• Deterministic Sandbox Fallback: Local zero-friction execution for judges", fill=(203, 213, 225), spacing=12)


    # ================= COLUMN 3: AWS CDS RUNTIME LAYER =================
    c3_x, c3_y, c3_w, c3_h = 1380, 160, 460, 840
    draw.rectangle([c3_x, c3_y, c3_x + c3_w, c3_y + c3_h], fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    draw.rectangle([c3_x, c3_y, c3_x + c3_w, c3_y + 50], fill=(20, 35, 55))
    draw.text((c3_x + 20, c3_y + 15), "3. AWS CDS RUNTIME SERVICES", fill=(56, 189, 248))

    # CDS 1
    draw.rectangle([c3_x + 20, c3_y + 80, c3_x + c3_w - 20, c3_y + 280], fill=(17, 24, 39), outline=(34, 197, 94), width=2)
    draw.text((c3_x + 40, c3_y + 100), "AWS End User Messaging Social", fill=(34, 197, 94))
    draw.text((c3_x + 40, c3_y + 140), "• Service: WhatsApp Business Platform\n• SDK: boto3 socialmessaging\n• Operation: SendWhatsAppMessage\n• Bonus: Eligible for Meta $10k Prize", fill=(203, 213, 225), spacing=12)

    # CDS 2
    draw.rectangle([c3_x + 20, c3_y + 310, c3_x + c3_w - 20, c3_y + 510], fill=(17, 24, 39), outline=(56, 189, 248), width=2)
    draw.text((c3_x + 40, c3_y + 330), "Amazon Simple Email Service (SES v2)", fill=(56, 189, 248))
    draw.text((c3_x + 40, c3_y + 370), "• Service: Amazon SES v2\n• SDK: boto3 sesv2\n• Operation: send_email\n• Output: Responsive HTML Executive Post-Mortem", fill=(203, 213, 225), spacing=12)

    # CDS 3
    draw.rectangle([c3_x + 20, c3_y + 540, c3_x + c3_w - 20, c3_y + 740], fill=(17, 24, 39), outline=(245, 158, 11), width=2)
    draw.text((c3_x + 40, c3_y + 560), "AWS End User Messaging (SMS v2)", fill=(245, 158, 11))
    draw.text((c3_x + 40, c3_y + 600), "• Service: Pinpoint SMS and Voice v2\n• SDK: boto3 pinpoint-sms-voice-v2\n• Operation: SendTextMessage\n• Output: Critical Priority Mobile Alerts", fill=(203, 213, 225), spacing=12)

    # Footer note
    draw.text((c3_x + 20, c3_y + 770), "AWS CloudFormation & CDK Ready", fill=(100, 116, 139))

    # Connecting Arrows
    draw.line([480, 240, 540, 240], fill=(34, 197, 94), width=3)
    draw.line([480, 730, 540, 730], fill=(168, 85, 247), width=3)
    draw.line([1320, 380, 1380, 240], fill=(34, 197, 94), width=3)
    draw.line([1320, 445, 1380, 410], fill=(56, 189, 248), width=3)
    draw.line([1320, 510, 1380, 640], fill=(245, 158, 11), width=3)

    # Save PNG
    img.save(PNG_PATH, "PNG")
    print(f"[SUCCESS] PNG architecture diagram saved: {PNG_PATH}")

    # Save PDF
    img.save(PDF_PATH, "PDF", resolution=150.0)
    print(f"[SUCCESS] PDF architecture diagram saved: {PDF_PATH}")

if __name__ == "__main__":
    generate_diagram_image()
