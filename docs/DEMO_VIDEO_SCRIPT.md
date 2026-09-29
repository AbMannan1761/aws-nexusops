# AWS NexusOps — 3-Minute Hackathon Demo Video Script

**Target Duration:** Exactly 2 minutes 50 seconds (Judges rule: "around three (3) minutes. Judges are not required to watch beyond three minutes").

---

### [0:00 - 0:30] Scene 1: The Problem & Solution Overview
* **Visual:** Full-screen title card with AWS NexusOps logo, followed by screen capture showing the Operations Command Center.
* **Narration:**
  > "Welcome to AWS NexusOps. In enterprise field operations and logistics, critical infrastructure disruptions often cause communication breakdowns. Operations leads, field engineers, and executive stakeholders are scattered across disjointed chat apps, email chains, and SMS pagers.
  > Today, we introduce NexusOps: an autonomous omnichannel operations concierge powered by Amazon Bedrock AgentCore and AWS Communication Developer Services (CDS). NexusOps bridges WhatsApp, Amazon SES, and AWS Pinpoint SMS v2 into a unified cognitive system."

---

### [0:30 - 1:15] Scene 2: Interactive WhatsApp Interaction (AWS EUM Social)
* **Visual:** Zoom in on the left column (WhatsApp Field Device simulator). Click the quick scenario: **"⚡ Node 4B Failure"** or type: *"Check status of Substation Node 4B telemetry failure."* Hit Send.
* **Narration:**
  > "Let's observe a real-world scenario. Sarah, our Operations Director, sends an urgent message over WhatsApp via AWS End User Messaging Social. 
  > Notice how the agent acknowledges the message. Incoming messages are processed by our backend calling `boto3.client('socialmessaging')`. The agent analyzes the telemetry disruption on Substation Node 4B and immediately identifies the active incident ticket."

---

### [1:15 - 2:00] Scene 3: Bedrock Agent Reasoning & Multi-CDS Execution
* **Visual:** Pan to the center column (Bedrock Agent Reasoning Traces). Highlight Step 1 and Step 2. Expand the tool invocation boxes.
* **Narration:**
  > "Look at the center column: this is Amazon Bedrock AgentCore running Anthropic Claude 3.5 Sonnet.
  > In Step 1, Bedrock evaluates the intent and autonomously calls `get_ticket_details`. 
  > In Step 2, upon finding the disruption, the agent resolves the ticket by triggering satellite failover and autonomously orchestrates all three AWS CDS channels:
  > First, it calls `send_whatsapp_message` to update Sarah in real time.
  > Second, it calls `send_ses_audit_email` using `boto3.client('sesv2')` to dispatch a formal executive digest.
  > And third, it calls `send_sms_urgent_alert` via `boto3.client('pinpoint-sms-voice-v2')` for high-priority mobile broadcast."

---

### [2:00 - 2:30] Scene 4: Stakeholder SES Inbox & SMS Verification
* **Visual:** Click on the right column tabs. Show the **SES Email Inbox** with styled HTML incident digest. Then switch to the **SMS / RCS Monitor** showing the dispatched SMS card.
* **Narration:**
  > "On the right panel, we see the immediate results. Under the SES Email tab, a styled, responsive HTML audit report has been delivered to executive stakeholders with exact incident metrics.
  > Switching to the SMS Monitor tab, the field team receives the urgent SMS alert dispatched through AWS Pinpoint SMS v2."

---

### [2:30 - 2:50] Scene 5: Architecture & Closing
* **Visual:** Display the Architecture Diagram (SVG). Pan across Bedrock AgentCore, AWS CDS clients, and DynamoDB.
* **Narration:**
  > "NexusOps is built with a serverless architecture designed for planetary scale, leveraging Amazon Bedrock, AWS Lambda, DynamoDB, and AWS CDS.
  > By combining the conversational agility of WhatsApp, the formal accountability of Amazon SES, and the immediacy of SMS, NexusOps redefines enterprise operational resilience.
  > Thank you!"
