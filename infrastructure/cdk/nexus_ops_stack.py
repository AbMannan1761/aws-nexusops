"""
AWS Cloud Development Kit (CDK) Stack for NexusOps
Deploys DynamoDB, Lambda Function, API Gateway, and IAM permissions for AWS CDS and Bedrock.
"""

# AWS CDK Python Stack definition
# To deploy: cdk deploy

from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
)
from constructs import Construct

class NexusOpsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. DynamoDB Tables for Sessions and Incident Tickets
        tickets_table = dynamodb.Table(
            self, "NexusOpsTicketsTable",
            partition_key=dynamodb.Attribute(name="ticket_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        audit_table = dynamodb.Table(
            self, "NexusOpsAuditTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # 2. NexusOps Backend Lambda Function
        backend_lambda = _lambda.Function(
            self, "NexusOpsHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="app.main.handler",
            code=_lambda.Code.from_asset("backend"),
            timeout=Duration.seconds(60),
            memory_size=1024,
            environment={
                "TICKETS_TABLE": tickets_table.table_name,
                "AUDIT_TABLE": audit_table.table_name,
                "MOCK_AWS_SERVICES": "false"
            }
        )

        # 3. Grant Permissions for DynamoDB
        tickets_table.grant_read_write_data(backend_lambda)
        audit_table.grant_read_write_data(backend_lambda)

        # 4. Grant IAM Permissions for AWS CDS Services and Amazon Bedrock
        backend_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=[
                # Amazon Bedrock
                "bedrock:InvokeModel",
                "bedrock:Converse",
                # AWS End User Messaging Social (WhatsApp)
                "social-messaging:SendWhatsAppMessage",
                "social-messaging:GetWhatsAppMessageSubmissionStatus",
                # Amazon SES v2
                "ses:SendEmail",
                "ses:SendRawEmail",
                # AWS End User Messaging (SMS v2)
                "sms-voice:SendTextMessage"
            ],
            resources=["*"]
        ))

        # 5. REST API Gateway
        api = apigw.LambdaRestApi(
            self, "NexusOpsApi",
            handler=backend_lambda,
            proxy=True,
            description="NexusOps Omnichannel Concierge API Gateway"
        )
