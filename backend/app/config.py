import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "NexusOps - Autonomous Omnichannel CDS Agent"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # AWS Region and Credentials
    AWS_REGION: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY", None)
    AWS_SESSION_TOKEN: Optional[str] = os.getenv("AWS_SESSION_TOKEN", None)
    
    # Bedrock Agent / Runtime Settings
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    BEDROCK_AGENT_ID: Optional[str] = os.getenv("BEDROCK_AGENT_ID", None)
    BEDROCK_AGENT_ALIAS_ID: Optional[str] = os.getenv("BEDROCK_AGENT_ALIAS_ID", None)

    # AWS End User Messaging Social (WhatsApp)
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "phone-num-arn-demo")
    WHATSAPP_WABA_ID: str = os.getenv("WHATSAPP_WABA_ID", "waba-account-demo")

    # Amazon SES v2
    SES_SENDER_EMAIL: str = os.getenv("SES_SENDER_EMAIL", "ops-concierge@nexusops.aws")
    SES_AUDIT_RECIPIENT_EMAIL: str = os.getenv("SES_AUDIT_RECIPIENT_EMAIL", "stakeholders@nexusops.aws")

    # AWS End User Messaging (SMS / RCS)
    PINPOINT_SMS_ORIGINATION_IDENTITY: str = os.getenv("PINPOINT_SMS_ORIGINATION_IDENTITY", "+18005550199")

    # Mock / Sandbox Mode (allows offline local demonstration and interactive test runs)
    MOCK_AWS_SERVICES: bool = os.getenv("MOCK_AWS_SERVICES", "true").lower() in ("true", "1", "yes")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
