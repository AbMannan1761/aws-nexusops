# AWS NexusOps — Autonomous Omnichannel Enterprise CDS Concierge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AWS Bedrock](https://img.shields.io/badge/Amazon%20Bedrock-AgentCore%20%7C%20Claude%203.5-purple.svg)](https://aws.amazon.com/bedrock/)
[![AWS EUM Social](https://img.shields.io/badge/AWS%20EUM%20Social-WhatsApp%20(boto3%20socialmessaging)-25D366.svg)](https://aws.amazon.com/end-user-messaging/)
[![Amazon SES v2](https://img.shields.io/badge/Amazon%20SES-v2%20(boto3%20sesv2)-38bdf8.svg)](https://aws.amazon.com/ses/)
[![AWS EUM SMS v2](https://img.shields.io/badge/AWS%20EUM%20SMS-Pinpoint%20SMS%20v2%20(boto3)-f59e0b.svg)](https://aws.amazon.com/end-user-messaging/)

> **Submission for the AWS Communication Developer Services (CDS) Agentic AI Partner Hackathon**  
> *Eligible for Overall Grand Prizes and the Meta WhatsApp Bonus Prize ($10,000).*

---

## 🌟 Executive Summary

**AWS NexusOps** is an autonomous, omnichannel incident remediation and enterprise operations concierge powered by **Amazon Bedrock AgentCore** and **AWS Communication Developer Services (CDS)**.

When critical infrastructure, utility telemetry, or logistics nodes experience disruptions, NexusOps autonomously orchestrates resolution across three distinct communication channels:
1. **Interactive WhatsApp Mobile Chat (AWS End User Messaging Social):** Real-time conversational triage and command execution for field engineers and operations directors.
2. **Executive Audit Digests (Amazon SES v2):** Automated generation and dispatch of responsive HTML incident post-mortems and stakeholder summaries.
3. **Emergency Broadcasts (AWS End User Messaging SMS v2):** Immediate, high-priority SMS alerts and 2FA site-override credentials dispatched to mobile devices.

---

## 🏛️ System Architecture

![NexusOps Architecture](docs/architecture_diagram.svg)

---

## 🚀 Proof of AWS CDS Runtime Integration

Per the Hackathon Official Submission Requirements, NexusOps imports and executes the official AWS SDK clients at runtime:

| AWS CDS Service | SDK Client & Operation | Implementation File | Purpose in Solution |
| :--- | :--- | :--- | :--- |
| **AWS End User Messaging Social (WhatsApp)** | `boto3.client('socialmessaging')`<br>`send_whatsapp_message` | [`backend/app/cds/whatsapp_client.py`](backend/app/cds/whatsapp_client.py) | Two-way interactive incident management on WhatsApp |
| **Amazon Simple Email Service (SES v2)** | `boto3.client('sesv2')`<br>`send_email` | [`backend/app/cds/ses_client.py`](backend/app/cds/ses_client.py) | Formal HTML audit reports delivered to stakeholder lists |
| **AWS End User Messaging (SMS v2)** | `boto3.client('pinpoint-sms-voice-v2')`<br>`send_text_message` | [`backend/app/cds/sms_client.py`](backend/app/cds/sms_client.py) | High-priority transactional mobile SMS alerts |
| **Amazon Bedrock AgentCore** | `boto3.client('bedrock-runtime')`<br>`converse` | [`backend/app/agent/bedrock_agent.py`](backend/app/agent/bedrock_agent.py) | Multi-step reasoning loop (Claude 3.5 Sonnet) & tool calling |

---

## 💡 Key Features & Workflow

* **Autonomous Tool Invocations:** The Bedrock Agent autonomously evaluates incident urgency and selects the appropriate CDS channel tools defined in [`backend/app/agent/prompts.py`](backend/app/agent/prompts.py).
* **Live ReAct Reasoning Traces:** Full visibility into the model's thoughts, tool arguments, and execution outputs displayed in real time in the Operations Command Center.
* **Deterministic Sandbox Mode:** Zero-friction local testing out of the box! Allows judges to experience the complete end-to-end agentic workflow immediately without requiring pre-configured AWS WABA/phone numbers.
* **Interactive Operations Command Center:** Built with vanilla modern CSS glassmorphism, responsive smartphone emulator, live Bedrock trace inspector, and an SES inbox renderer.

---

## 🛠️ Quick Start & Local Run

### Prerequisites
* Python 3.10+ (Tested on Python 3.12 and Python 3.14)
* pip & virtualenv

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/your-org/aws-nexusops.git
cd aws-nexusops

# Create and activate virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment (Optional for Live AWS)
Create a `.env` file in the root directory (or leave default for Sandbox Simulation Mode):
```ini
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Set to false to invoke live AWS Bedrock and CDS endpoints
MOCK_AWS_SERVICES=true
```

### 3. Launch the Application
```bash
python backend/run.py
```

Open your browser to:
👉 **`http://127.0.0.1:8000`**

---

## 📂 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── bedrock_agent.py    # Bedrock Converse & AgentCore runtime
│   │   │   ├── prompts.py          # System prompts & Bedrock Tool specifications
│   │   │   └── tools.py            # Executable CDS tool dispatcher
│   │   ├── cds/
│   │   │   ├── whatsapp_client.py  # boto3 socialmessaging (SendWhatsAppMessage)
│   │   │   ├── ses_client.py       # boto3 sesv2 (send_email)
│   │   │   └── sms_client.py       # boto3 pinpoint-sms-voice-v2 (SendTextMessage)
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic data schemas
│   │   ├── services/
│   │   │   └── db_service.py       # In-memory & DynamoDB incident store
│   │   ├── config.py               # Environment configuration
│   │   └── main.py                 # FastAPI server & static file host
│   ├── requirements.txt
│   └── run.py                      # Local runner script
├── frontend/                       # Operations Command Center Dashboard
│   ├── css/styles.css              # Custom glassmorphism design system
│   ├── js/app.js                   # Trace visualizer & WhatsApp simulator
│   └── index.html                  # Main UI
├── infrastructure/
│   └── cdk/
│       └── nexus_ops_stack.py      # AWS CDK deployment stack
├── docs/
│   ├── ARCHITECTURE.md             # Detailed architectural specification
│   ├── architecture_diagram.svg    # Scalable vector architecture diagram
│   ├── DEVPOST_SUBMISSION.md       # Devpost submission form draft
│   └── DEMO_VIDEO_SCRIPT.md        # 3-minute video presentation script
├── LICENSE                         # MIT License
└── README.md
```

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
