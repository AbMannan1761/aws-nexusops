"""
Amazon Simple Email Service (SES v2) Client Integration
Adheres to AWS Hackathon Official Requirements:
  - Uses `boto3.client('sesv2')`
  - Invokes `send_email`
"""

import logging
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError
from app.config import settings

logger = logging.getLogger(__name__)

class SESClient:
    def __init__(self):
        self.mock_mode = settings.MOCK_AWS_SERVICES
        self.sender_email = settings.SES_SENDER_EMAIL
        self.client = None

        if not self.mock_mode:
            try:
                self.client = boto3.client(
                    "sesv2",
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN
                )
                logger.info("Amazon SES v2 client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize live sesv2 client: {e}. Falling back to sandbox mode.")
                self.mock_mode = True

    def send_audit_or_report_email(
        self,
        recipient_emails: List[str],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends an executive summary, audit report, or incident escalation email via Amazon SES v2.
        """
        if not text_body:
            text_body = "NexusOps Autonomous Concierge Audit Notice. Please view in an HTML-compatible client."

        if self.mock_mode or not self.client:
            logger.info(f"[SANDBOX] Amazon SES v2.send_email to {recipient_emails}: '{subject}'")
            return {
                "status": "SUCCESS",
                "mode": "SANDBOX_MOCK",
                "service": "Amazon SES (Simple Email Service v2)",
                "operation": "send_email",
                "recipients": recipient_emails,
                "sender": self.sender_email,
                "subject": subject,
                "htmlBody": html_body,
                "messageId": f"ses-msg-{str(abs(hash(subject + str(recipient_emails))))[:12]}"
            }

        try:
            # Official AWS SDK Call: sesv2.send_email
            response = self.client.send_email(
                FromEmailAddress=self.sender_email,
                Destination={
                    "ToAddresses": recipient_emails
                },
                Content={
                    "Simple": {
                        "Subject": {
                            "Data": subject,
                            "Charset": "UTF-8"
                        },
                        "Body": {
                            "Html": {
                                "Data": html_body,
                                "Charset": "UTF-8"
                            },
                            "Text": {
                                "Data": text_body,
                                "Charset": "UTF-8"
                            }
                        }
                    }
                }
            )
            message_id = response.get("MessageId")
            logger.info(f"Amazon SES v2 email dispatched: {message_id}")
            return {
                "status": "SUCCESS",
                "mode": "LIVE_AWS",
                "service": "Amazon SES (Simple Email Service v2)",
                "operation": "send_email",
                "recipients": recipient_emails,
                "subject": subject,
                "messageId": message_id,
                "rawResponse": response
            }
        except ClientError as ce:
            logger.error(f"Amazon SES v2 ClientError: {ce.response['Error']['Message']}")
            return {
                "status": "ERROR",
                "service": "Amazon SES (v2)",
                "operation": "send_email",
                "error": ce.response["Error"]["Message"]
            }
        except Exception as ex:
            logger.error(f"Unexpected error in SES client: {ex}")
            return {
                "status": "ERROR",
                "service": "Amazon SES (v2)",
                "operation": "send_email",
                "error": str(ex)
            }

ses_client = SESClient()
