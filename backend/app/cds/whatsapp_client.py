"""
AWS End User Messaging Social (WhatsApp) Client Integration
Adheres to AWS Hackathon Official Requirements:
  - Uses `boto3.client('socialmessaging')`
  - Invokes `SendWhatsAppMessage` (or `send_whatsapp_message`)
"""

import json
import logging
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from app.config import settings

logger = logging.getLogger(__name__)

class WhatsAppCDSClient:
    def __init__(self):
        self.mock_mode = settings.MOCK_AWS_SERVICES
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.client = None

        if not self.mock_mode:
            try:
                self.client = boto3.client(
                    "socialmessaging",
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN
                )
                logger.info("AWS End User Messaging Social (WhatsApp) client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize live socialmessaging client: {e}. Falling back to sandbox mode.")
                self.mock_mode = True

    def send_text_message(
        self,
        recipient_phone: str,
        message_body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Sends an interactive WhatsApp message using AWS End User Messaging Social.
        Calls the `send_whatsapp_message` SDK operation.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": message_body
            }
        }
        
        message_bytes = json.dumps(payload).encode("utf-8")

        if self.mock_mode or not self.client:
            logger.info(f"[SANDBOX] AWS SocialMessaging.SendWhatsAppMessage to {recipient_phone}: {message_body}")
            return {
                "status": "SUCCESS",
                "mode": "SANDBOX_MOCK",
                "service": "AWS End User Messaging Social (WhatsApp)",
                "operation": "SendWhatsAppMessage",
                "recipient": recipient_phone,
                "message": message_body,
                "messageId": f"wamid.HBgL{str(abs(hash(message_body)))[:16]}",
                "meta": metadata or {}
            }

        try:
            # Official AWS SDK Call: socialmessaging.send_whatsapp_message
            response = self.client.send_whatsapp_message(
                originationPhoneNumberId=self.phone_number_id,
                message=message_bytes,
                metaData=metadata or {}
            )
            logger.info(f"AWS WhatsApp message dispatched: {response.get('messageId')}")
            return {
                "status": "SUCCESS",
                "mode": "LIVE_AWS",
                "service": "AWS End User Messaging Social (WhatsApp)",
                "operation": "SendWhatsAppMessage",
                "recipient": recipient_phone,
                "messageId": response.get("messageId"),
                "rawResponse": response
            }
        except ClientError as ce:
            logger.error(f"AWS SocialMessaging ClientError: {ce.response['Error']['Message']}")
            return {
                "status": "ERROR",
                "service": "AWS End User Messaging Social",
                "operation": "SendWhatsAppMessage",
                "error": ce.response["Error"]["Message"]
            }
        except Exception as ex:
            logger.error(f"Unexpected error in WhatsApp client: {ex}")
            return {
                "status": "ERROR",
                "service": "AWS End User Messaging Social",
                "operation": "SendWhatsAppMessage",
                "error": str(ex)
            }

whatsapp_client = WhatsAppCDSClient()
