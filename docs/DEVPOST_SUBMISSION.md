# Devpost Submission Text: AWS NexusOps

## Project Title
**AWS NexusOps — Autonomous Omnichannel Enterprise Concierge & Operations Agent**

## Elevator Pitch
NexusOps is an autonomous AI operations concierge powered by Amazon Bedrock AgentCore and AWS Communication Developer Services (CDS). It monitors mission-critical incidents, interacts with field engineers over WhatsApp, dispatches executive audit digests via Amazon SES v2, and broadcasts emergency failover alerts over AWS End User Messaging SMS v2.

---

## Inspiration
Enterprise field operations, utility grids, and mission-critical logistics networks often suffer from fragmented communication. When a critical substation or supply-chain gateway fails, operations managers are forced to manually switch between fragmented chat apps, formal email threads, and emergency SMS alerts. 

We set out to eliminate these communication silos by creating a unified autonomous intelligence: an agent that can actively listen, reason, remediate, and synchronize across **WhatsApp**, **Amazon SES**, and **SMS/RCS** simultaneously.

---

## What It Does
**NexusOps** serves as an autonomous cognitive concierge that unifies three core AWS Communication Developer Services with Amazon Bedrock:
1. **Interactive WhatsApp Interface (AWS End User Messaging Social):**
   Field engineers, operations leads, and clients converse naturally with NexusOps via WhatsApp. NexusOps uses Claude 3.5 Sonnet to understand telemetry issues, queries incident databases, and provides instant status updates.
2. **Executive Audit Digests (Amazon SES v2):**
   Once an incident is remediated, NexusOps autonomously compiles a formal incident report in styled HTML and sends it via Amazon SES v2 to executive and regulatory stakeholder distribution lists.
3. **High-Priority Critical SMS (AWS End User Messaging SMS v2):**
   For critical Tier-1 incidents and site-access security overrides, NexusOps triggers high-priority SMS alerts directly to mobile devices with cryptographic confirmation IDs.
4. **Operations Command Center Dashboard:**
   An operations console offering real-time visibility into Bedrock reasoning traces, ReAct tool invocations, and live delivery status across all three CDS channels.

---

## How We Built It
* **Agentic AI Core:** Built with **Amazon Bedrock AgentCore** and the Bedrock Converse API utilizing **Anthropic Claude 3.5 Sonnet**. The agent evaluates conversation history and autonomously decides which CDS tools to invoke.
* **AWS End User Messaging Social (WhatsApp):** Integrated using `boto3.client('socialmessaging')` with runtime calls to `send_whatsapp_message`.
* **Amazon SES v2:** Integrated using `boto3.client('sesv2')` calling `send_email` with responsive HTML email templates.
* **AWS End User Messaging (SMS v2):** Integrated using `boto3.client('pinpoint-sms-voice-v2')` calling `send_text_message`.
* **Backend:** FastAPI with Pydantic data schemas, asynchronous event routing, and state persistence.
* **Frontend:** A dark-mode Command Center with mobile smartphone simulator, live Bedrock trace inspector, and SES inbox viewer.

---

## How AWS End User Messaging Social (WhatsApp) Was Used (Meta WhatsApp Prize)
AWS End User Messaging Social serves as the primary conversational interaction channel for NexusOps. Using `boto3.client('socialmessaging')`, our solution:
* Receives real-time incoming webhook events when a field engineer or client messages the registered WhatsApp Business Account.
* Dynamically formats rich, formatted text updates (including status emojis, key-value telemetry metrics, and actionable reply prompts).
* Calls the `send_whatsapp_message` SDK operation with origin phone numbers and structured payloads to maintain continuous two-way communication.

---

## Challenges We Overcame
1. **Synchronizing Multi-Channel State:** Orchestrating an action across WhatsApp, SES, and SMS without duplicate notifications required strict idempotent state management in the agent tool layer.
2. **Real-time Trace Visualization:** Capturing Bedrock Converse API tool-use steps and streaming them to the web UI in sub-second latency required asynchronous tool event hooks.

---

## Accomplishments We're Proud Of
* **True Multi-CDS Integration:** Fully implemented and executed all 3 major AWS CDS services in a single coherent business scenario.
* **Zero-friction Testing:** Developed both live AWS SDK execution and a deterministic sandbox mode, allowing judges and developers to test the complete workflow locally with zero configuration.
* **Enterprise-grade Polish:** Designed a Command Center with real-time trace inspection and interactive simulators.

---

## What's Next for AWS NexusOps
* Implementing Rich Communication Services (RCS) via `pinpoint-sms-voice-v2` for interactive carousels and rich cards on Android devices.
* Integrating Amazon Bedrock Knowledge Bases with vector search over engineering standard operating procedures (SOPs).
* Publishing NexusOps as an AWS Marketplace solution for utility and logistics providers.
