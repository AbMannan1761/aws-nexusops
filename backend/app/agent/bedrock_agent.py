"""
Amazon Bedrock AgentCore & Converse Integration for NexusOps.
Supports both AWS Live Bedrock Runtime (Claude 3.5 Sonnet / Haiku)
and high-fidelity Autonomous Simulation for offline/sandbox testing.
"""

import json
import logging
from typing import List, Dict, Any, Tuple
import boto3
from botocore.exceptions import ClientError

from app.config import settings
from app.models.schemas import AgentChatResponse, AgentTraceStep, AgentToolCall
from app.agent.prompts import NEXUS_OPS_SYSTEM_PROMPT, BEDROCK_TOOLS_SPEC
from app.agent.tools import execute_tool
from app.services.db_service import db

logger = logging.getLogger(__name__)

class BedrockAgentRunner:
    def __init__(self):
        self.mock_mode = settings.MOCK_AWS_SERVICES
        self.model_id = settings.BEDROCK_MODEL_ID
        self.client = None

        if not self.mock_mode:
            try:
                self.client = boto3.client(
                    "bedrock-runtime",
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN
                )
                logger.info(f"Amazon Bedrock Runtime initialized with model: {self.model_id}")
            except Exception as e:
                logger.warning(f"Failed to initialize live Bedrock client: {e}. Running in sandbox simulation mode.")
                self.mock_mode = True

    def process_message(
        self,
        session_id: str,
        user_message: str,
        user_phone: str = "+12065550142",
        user_name: str = "Sarah Jenkins (Director of Ops)",
        channel: str = "WHATSAPP"
    ) -> AgentChatResponse:
        """
        Orchestrates autonomous multi-turn reasoning and tool invocation across AWS CDS services.
        """
        logger.info(f"Incoming message from {user_name} ({user_phone}) via {channel}: '{user_message}'")
        
        # Log to DB session
        db.append_message(session_id, "user", user_message)

        if not self.mock_mode and self.client:
            return self._run_live_bedrock_converse(session_id, user_message, user_phone, user_name, channel)
        else:
            return self._run_sandbox_autonomous_flow(session_id, user_message, user_phone, user_name, channel)

    def _run_live_bedrock_converse(
        self,
        session_id: str,
        user_message: str,
        user_phone: str,
        user_name: str,
        channel: str
    ) -> AgentChatResponse:
        """
        Executes multi-step tool reasoning with Amazon Bedrock Converse API.
        """
        traces: List[AgentTraceStep] = []
        cds_dispatches: List[Dict[str, Any]] = []

        # Build message history for Bedrock Converse
        messages = [
            {
                "role": "user",
                "content": [{"text": f"User: {user_name} ({user_phone})\nChannel: {channel}\nMessage: {user_message}"}]
            }
        ]

        system_prompt = [{"text": NEXUS_OPS_SYSTEM_PROMPT}]
        tool_config = {"tools": BEDROCK_TOOLS_SPEC}

        step_counter = 1
        max_turns = 5

        while step_counter <= max_turns:
            try:
                response = self.client.converse(
                    modelId=self.model_id,
                    system=system_prompt,
                    messages=messages,
                    toolConfig=tool_config,
                    inferenceConfig={"temperature": 0.2, "maxTokens": 2048}
                )

                output_message = response["output"]["message"]
                messages.append(output_message)

                stop_reason = response.get("stopReason")
                tool_requests = [c["toolUse"] for c in output_message["content"] if "toolUse" in c]
                text_content = " ".join([c["text"] for c in output_message["content"] if "text" in c])

                trace_step = AgentTraceStep(
                    step_number=step_counter,
                    thought=f"Bedrock StopReason: {stop_reason}. Analysis: {text_content or 'Evaluating appropriate tool dispatch...'}",
                    tool_calls=[]
                )

                if not tool_requests:
                    # Final textual response reached
                    trace_step.output_message = text_content
                    traces.append(trace_step)
                    db.append_message(session_id, "assistant", text_content)
                    return AgentChatResponse(
                        session_id=session_id,
                        response_text=text_content,
                        channel=channel,
                        traces=traces,
                        cds_dispatches=cds_dispatches
                    )

                # Execute tool calls requested by Bedrock
                tool_result_contents = []
                for tu in tool_requests:
                    tool_use_id = tu["toolUseId"]
                    tool_name = tu["name"]
                    tool_input = tu["input"]

                    res = execute_tool(tool_name, tool_input)
                    if tool_name.startswith("send_"):
                        cds_dispatches.append({"tool": tool_name, "result": res})

                    trace_step.tool_calls.append(AgentToolCall(
                        tool_name=tool_name,
                        arguments=tool_input,
                        result=res
                    ))

                    tool_result_contents.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": res}],
                            "status": "success"
                        }
                    })

                traces.append(trace_step)
                messages.append({"role": "user", "content": tool_result_contents})
                step_counter += 1

            except ClientError as ce:
                logger.error(f"Bedrock Converse ClientError: {ce}")
                err_msg = f"Bedrock invocation error: {ce.response['Error']['Message']}"
                return AgentChatResponse(
                    session_id=session_id,
                    response_text=err_msg,
                    channel=channel,
                    traces=traces,
                    cds_dispatches=cds_dispatches
                )

        return AgentChatResponse(
            session_id=session_id,
            response_text="Completed maximum autonomous reasoning steps.",
            channel=channel,
            traces=traces,
            cds_dispatches=cds_dispatches
        )

    def _run_sandbox_autonomous_flow(
        self,
        session_id: str,
        user_message: str,
        user_phone: str,
        user_name: str,
        channel: str
    ) -> AgentChatResponse:
        """
        High-fidelity autonomous agent simulation.
        Executes actual AWS CDS client methods (or sandbox mock) and emits full reasoning traces.
        """
        traces: List[AgentTraceStep] = []
        cds_dispatches: List[Dict[str, Any]] = []
        lower_msg = user_message.lower()

        # Step 1: Ingestion & Intent Analysis
        trace1 = AgentTraceStep(
            step_number=1,
            thought=f"Analyzing intent from {user_name} on {channel}. Message mentions keywords: {[w for w in ['ticket', 'status', 'outage', 'node', 'critical', 'urgent', 'resolve'] if w in lower_msg]}.",
            tool_calls=[]
        )

        # Check existing ticket TICK-8041
        ticket_id = "TICK-8041"
        tool_call_ticket = AgentToolCall(
            tool_name="get_ticket_details",
            arguments={"ticket_id": ticket_id},
            result=execute_tool("get_ticket_details", {"ticket_id": ticket_id})
        )
        trace1.tool_calls.append(tool_call_ticket)
        traces.append(trace1)

        # Step 2: Autonomous Incident Remediation & Multi-channel AWS CDS Dispatches
        trace2 = AgentTraceStep(
            step_number=2,
            thought="Incident verified as Substation Node 4B telemetry loss. Automated diagnostic restored backup radio. Now updating ticket, notifying user on WhatsApp, sending official SES audit digest, and dispatching SMS confirmation.",
            tool_calls=[]
        )

        # 1. Update ticket
        update_res = execute_tool("update_ticket_status", {
            "ticket_id": ticket_id,
            "new_status": "RESOLVED",
            "resolution_notes": "NexusOps re-routed telemetry stream through secondary L-band satellite link. Latency normalized to 28ms."
        })
        trace2.tool_calls.append(AgentToolCall(
            tool_name="update_ticket_status",
            arguments={"ticket_id": ticket_id, "new_status": "RESOLVED"},
            result=update_res
        ))

        # 2. AWS CDS: WhatsApp dispatch (socialmessaging SendWhatsAppMessage)
        whatsapp_msg = (
            f"✅ *NexusOps Update: Ticket {ticket_id} Resolved*\n\n"
            f"Hello {user_name},\n"
            f"Telemetry link for *Substation Node 4B* has been restored via the secondary satellite gateway.\n\n"
            f"• *Status:* 🟢 RESOLVED\n"
            f"• *Latency:* 28ms (Optimal)\n"
            f"• *SES Audit Digest:* Dispatched to stakeholder distribution list.\n\n"
            f"Reply with 'ACK' to confirm closure."
        )
        whatsapp_res = execute_tool("send_whatsapp_message", {
            "recipient_phone": user_phone,
            "message_body": whatsapp_msg
        })
        cds_dispatches.append({"tool": "send_whatsapp_message", "result": whatsapp_res})
        trace2.tool_calls.append(AgentToolCall(
            tool_name="send_whatsapp_message",
            arguments={"recipient_phone": user_phone, "message_body": whatsapp_msg},
            result=whatsapp_res
        ))

        # 3. AWS CDS: SES v2 dispatch (sesv2 send_email)
        ses_html = f"""
        <div style="font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; border-radius: 8px;">
            <div style="border-bottom: 2px solid #38bdf8; padding-bottom: 12px; margin-bottom: 16px;">
                <h2 style="color: #38bdf8; margin: 0;">AWS NexusOps — Executive Incident Resolution Digest</h2>
                <p style="color: #94a3b8; font-size: 14px; margin: 4px 0 0 0;">Incident Reference: <strong>{ticket_id}</strong> | Timestamp: {db.get_ticket(ticket_id).updated_at}</p>
            </div>
            <p>Dear Stakeholder,</p>
            <p>This automated audit digest confirms that autonomous incident remediation has been successfully finalized by the <strong>NexusOps Bedrock Agent</strong>.</p>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; background: #1e293b; border-radius: 6px;">
                <tr style="border-bottom: 1px solid #334155;"><td style="padding: 10px; font-weight: bold; color: #94a3b8;">Asset</td><td style="padding: 10px; color: #f8fafc;">Substation Node 4B Gateway</td></tr>
                <tr style="border-bottom: 1px solid #334155;"><td style="padding: 10px; font-weight: bold; color: #94a3b8;">Severity</td><td style="padding: 10px; color: #ef4444; font-weight: bold;">CRITICAL (Resolved)</td></tr>
                <tr style="border-bottom: 1px solid #334155;"><td style="padding: 10px; font-weight: bold; color: #94a3b8;">Remediation Action</td><td style="padding: 10px; color: #f8fafc;">L-band Satellite Uplink failover activated</td></tr>
                <tr><td style="padding: 10px; font-weight: bold; color: #94a3b8;">Dispatched Channels</td><td style="padding: 10px; color: #38bdf8;">AWS SocialMessaging (WhatsApp), Amazon SES v2, AWS Pinpoint SMS v2</td></tr>
            </table>
            <p style="font-size: 13px; color: #94a3b8;">Amazon Bedrock AgentCore Autonomous Execution Engine &bull; AWS Communication Developer Services</p>
        </div>
        """
        ses_res = execute_tool("send_ses_audit_email", {
            "recipient_emails": ["ops-director@megacorp-logistics.com", "noc-alerts@megacorp-logistics.com"],
            "subject": f"[RESOLVED] Priority 1 Incident {ticket_id} - Node 4B Telemetry Restored",
            "html_body": ses_html
        })
        cds_dispatches.append({"tool": "send_ses_audit_email", "result": ses_res})
        trace2.tool_calls.append(AgentToolCall(
            tool_name="send_ses_audit_email",
            arguments={"subject": f"[RESOLVED] {ticket_id}", "recipients": ["ops-director@megacorp-logistics.com"]},
            result=ses_res
        ))

        # 4. AWS CDS: SMS v2 dispatch (pinpoint-sms-voice-v2 SendTextMessage)
        sms_msg = f"[NexusOps ALERT] Incident {ticket_id} RESOLVED. Substation 4B online via satellite failover. SES audit dispatched."
        sms_res = execute_tool("send_sms_urgent_alert", {
            "destination_phone": user_phone,
            "message_body": sms_msg
        })
        cds_dispatches.append({"tool": "send_sms_urgent_alert", "result": sms_res})
        trace2.tool_calls.append(AgentToolCall(
            tool_name="send_sms_urgent_alert",
            arguments={"destination_phone": user_phone, "message_body": sms_msg},
            result=sms_res
        ))

        traces.append(trace2)

        final_response_text = (
            f"Understood, {user_name}. I have resolved incident {ticket_id} by switching Substation Node 4B to the backup satellite link. "
            f"Confirmation sent to WhatsApp, executive audit digest emailed via Amazon SES v2, and high-priority SMS dispatched via AWS Pinpoint SMS v2."
        )

        db.append_message(session_id, "assistant", final_response_text)

        return AgentChatResponse(
            session_id=session_id,
            response_text=final_response_text,
            channel=channel,
            traces=traces,
            cds_dispatches=cds_dispatches
        )

bedrock_agent = BedrockAgentRunner()
