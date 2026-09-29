"""
AWS End User Messaging (SMS & RCS) Client Integration
Adheres to AWS Hackathon Official Requirements:
  - Uses `boto3.client('pinpoint-sms-voice-v2')`
  - Invokes `SendTextMessage` (send_text_message)
"""

import logging
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from app.config import settings

logger = logging.getLogger(__name__)

class PinpointSMSClient:
    def __init__(self):
        self.mock_mode = settings.MOCK_AWS_SERVICES
        self.origination_identity = settings.PINPOINT_SMS_ORIGINATION_IDENTITY
        self.client = None

        if not self.mock_mode:
            try:
                self.client = boto3.client(
                    "pinpoint-sms-voice-v2",
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN
                )
                logger.info("AWS Pinpoint SMS and Voice v2 client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize live pinpoint-sms-voice-v2 client: {e}. Falling back to sandbox mode.")
                self.mock_mode = True

    def send_urgent_sms(
        self,
        destination_phone: str,
        message_body: str,
        message_type: str = "TRANSACTIONAL"
    ) -> Dict[str, Any]:
        """
        Sends high-priority OTP or dispatch alert via AWS End User Messaging (SMS v2).
        """
        if self.mock_mode or not self.client:
            logger.info(f"[SANDBOX] AWS PinpointSMSVoiceV2.SendTextMessage to {destination_phone}: {message_body}")
            return {
                "status": "SUCCESS",
                "mode": "SANDBOX_MOCK",
                "service": "AWS End User Messaging (Pinpoint SMS v2)",
                "operation": "SendTextMessage",
                "destinationPhoneNumber": destination_phone,
                "message": message_body,
                "messageId": f"sms-v2-{str(abs(hash(destination_phone + message_body)))[:10]}"
            }

        try:
            # Official AWS SDK Call: pinpoint-sms-voice-v2.send_text_message
            response = self.client.send_text_message(
                DestinationPhoneNumber=destination_phone,
                OriginationIdentity=self.origination_identity,
                MessageBody=message_body,
                MessageType=message_type
            )
            message_id = response.get("MessageId")
            logger.info(f"AWS Pinpoint SMS v2 dispatched: {message_id}")
            return {
                "status": "SUCCESS",
                "mode": "LIVE_AWS",
                "service": "AWS End User Messaging (Pinpoint SMS v2)",
                "operation": "SendTextMessage",
                "destinationPhoneNumber": destination_phone,
                "messageId": message_id,
                "rawResponse": response
            }
        except ClientError as ce:
            logger.error(f"AWS Pinpoint SMS v2 ClientError: {ce.response['Error']['Message']}")
            return {
                "status": "ERROR",
                "service": "AWS End User Messaging (SMS v2)",
                "operation": "SendTextMessage",
                "error": ce.response["Error"]["Message"]
            }
        except Exception as ex:
            logger.error(f"Unexpected error in SMS client: {ex}")
            return {
                "status": "ERROR",
                "service": "AWS End User Messaging (SMS v2)",
                "operation": "SendTextMessage",
                "error": str(ex)
            }

sms_client = PinpointSMSClient()
