"""
Entry script to run the NexusOps application locally.
"""

import sys
import os
import uvicorn

# Ensure the backend directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 65)
    print("🚀 Starting NexusOps: Autonomous Omnichannel CDS Agent")
    print("📡 AWS CDS Services: WhatsApp (socialmessaging) | SES v2 | SMS v2")
    print("🧠 Powered by Amazon Bedrock AgentCore")
    print("🌐 Dashboard URL: http://127.0.0.1:8000")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
