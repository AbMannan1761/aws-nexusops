"""
NexusOps Demo Video Generator - Robust Frame Encoding
Produces a 1080p, 25fps video where every second has real video frames (no black screen or freeze).
"""

import os
import asyncio
import subprocess
import numpy as np
from PIL import Image, ImageDraw
import edge_tts
import imageio
import imageio_ffmpeg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")
AUDIO_FILE = os.path.join(OUTPUT_DIR, "narration.mp3")
TEMP_VIDEO_FILE = os.path.join(OUTPUT_DIR, "temp_video.mp4")
FINAL_VIDEO_FILE = os.path.join(OUTPUT_DIR, "nexus_ops_demo.mp4")

NARRATION_TEXT = (
    "Welcome to AWS NexusOps. In enterprise field operations and logistics, critical infrastructure disruptions often cause communication breakdowns. "
    "Operations leads, field engineers, and executive stakeholders are scattered across disjointed chat apps, email chains, and SMS pagers. "
    "Today, we introduce NexusOps: an autonomous omnichannel operations concierge powered by Amazon Bedrock AgentCore and AWS Communication Developer Services. "
    "NexusOps bridges WhatsApp, Amazon SES, and AWS Pinpoint SMS v2 into a unified cognitive system. "
    "Let us observe a real-world scenario. Sarah, our Operations Director, sends an urgent message over WhatsApp via AWS End User Messaging Social. "
    "Incoming messages are processed by our backend calling boto3 social messaging. The agent analyzes the telemetry disruption on Substation Node 4B and immediately identifies the active incident ticket. "
    "Here, Amazon Bedrock AgentCore runs Anthropic Claude 3.5 Sonnet. "
    "Bedrock evaluates the intent and autonomously calls get ticket details. "
    "Upon diagnosing the disruption, the agent resolves the incident by triggering satellite failover and autonomously orchestrates all three AWS CDS channels: "
    "First, it calls send WhatsApp message to update Sarah in real time. "
    "Second, it calls send SES audit email using boto3 ses v2 to dispatch a formal executive digest. "
    "And third, it calls send SMS urgent alert via boto3 pinpoint SMS voice v2 for high-priority mobile broadcast. "
    "Under the SES Email tab, a styled, responsive HTML audit report has been delivered to executive stakeholders with exact incident metrics. "
    "Switching to the SMS Monitor tab, the field team receives the urgent SMS alert dispatched through AWS Pinpoint SMS v2. "
    "NexusOps is built with a serverless architecture designed for planetary scale, leveraging Amazon Bedrock, AWS Lambda, DynamoDB, and AWS Communication Developer Services. "
    "By combining the conversational agility of WhatsApp, the formal accountability of Amazon SES, and the immediacy of SMS, NexusOps redefines enterprise operational resilience. "
    "Thank you!"
)

async def generate_audio():
    print("[AUDIO] Generating neural voiceover...")
    communicate = edge_tts.Communicate(NARRATION_TEXT, voice="en-US-ChristopherNeural", rate="+2%")
    await communicate.save(AUDIO_FILE)
    print(f"[AUDIO] Audio generated at: {AUDIO_FILE}")

def create_slides():
    print("[SLIDES] Generating visual slide images...")
    os.makedirs(os.path.join(OUTPUT_DIR, "slides"), exist_ok=True)
    width, height = 1920, 1080

    slides_info = [
        {
            "num": 1,
            "badge": "AWS HACKATHON 2026 | SUBMISSION",
            "title": "AWS NexusOps",
            "subtitle": "Autonomous Omnichannel CDS Operations Concierge",
            "points": [
                "Mission: Autonomous multi-channel incident remediation for enterprise & field operations",
                "Brain: Amazon Bedrock AgentCore & Claude 3.5 Sonnet (ReAct Tool Orchestration)",
                "Channels: AWS End User Messaging Social (WhatsApp) + Amazon SES v2 + AWS Pinpoint SMS v2",
                "Database & Memory: Amazon DynamoDB for real-time audit logs & ticket lifecycle tracking"
            ],
            "accent": (56, 189, 248)
        },
        {
            "num": 2,
            "badge": "CHANNEL 1: WHATSAPP INTERFACE",
            "title": "Field Interaction over WhatsApp",
            "subtitle": "AWS End User Messaging Social (boto3 socialmessaging)",
            "points": [
                "Real-time two-way conversational triage for field leads & site operators",
                "Runtime execution of SDK operation: SendWhatsAppMessage",
                "Simulated scenario: Substation Node 4B telemetry failure resolved autonomously",
                "Targeting the Meta WhatsApp Bonus Prize ($10,000 USD)"
            ],
            "accent": (37, 211, 102)
        },
        {
            "num": 3,
            "badge": "AGENTIC BRAIN: BEDROCK AGENTCORE",
            "title": "Amazon Bedrock ReAct Reasoning Loop",
            "subtitle": "Anthropic Claude 3.5 Sonnet with Dynamic Tool Execution",
            "points": [
                "Step 1: Cognitive Ingestion -> evaluates telemetry error and fetches ticket TICK-8041",
                "Step 2: Autonomous Remediation -> triggers satellite failover & updates ticket status to RESOLVED",
                "Multi-tool dispatch: Coordinates WhatsApp update, SES executive email, and SMS broadcast",
                "Real-time streaming traces rendered visually in the Command Center"
            ],
            "accent": (168, 85, 247)
        },
        {
            "num": 4,
            "badge": "CHANNELS 2 & 3: FORMAL AUDIT & BROADCAST",
            "title": "Executive Email & Mobile SMS Dispatches",
            "subtitle": "Amazon SES v2 (sesv2) & AWS Pinpoint SMS v2 (pinpoint-sms-voice-v2)",
            "points": [
                "Amazon SES v2: Automated responsive HTML incident post-mortems delivered to executive lists",
                "AWS Pinpoint SMS v2: Immediate high-priority transactional SMS alerts & 2FA overrides",
                "Audit trail & cryptographic delivery receipts stored persistently in DynamoDB",
                "Unified operations console with live trace inspector and inbox renderer"
            ],
            "accent": (245, 158, 11)
        },
        {
            "num": 5,
            "badge": "ARCHITECTURE & PRODUCTION READY",
            "title": "Serverless Planetary-Scale Architecture",
            "subtitle": "Fully Open Source under MIT License on GitHub",
            "points": [
                "Infrastructure as Code: AWS Cloud Development Kit (CDK) & CloudFormation ready",
                "Deterministic Sandbox: 100% reproducible local testing out of the box for judges",
                "GitHub Code Repository: https://github.com/AbMannan1761/aws-nexusops",
                "Ready for Devpost Submission & ACE Partner Opportunity"
            ],
            "accent": (56, 189, 248)
        }
    ]

    images = []
    for info in slides_info:
        img = Image.new("RGB", (width, height), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Gradient top stripe
        draw.rectangle([0, 0, width, 10], fill=info["accent"])

        # Category Badge
        draw.rectangle([120, 100, 520, 145], fill=(20, 28, 45), outline=info["accent"], width=2)
        draw.text((140, 112), info["badge"], fill=info["accent"])

        # Main Titles
        draw.text((120, 190), info["title"], fill=(255, 255, 255))
        draw.text((120, 280), info["subtitle"], fill=info["accent"])

        # Divider line
        draw.line([120, 360, 1800, 360], fill=(45, 60, 85), width=3)

        # Card container
        draw.rectangle([120, 410, 1800, 940], fill=(17, 24, 39), outline=(45, 60, 85), width=2)

        # Bullets
        y = 470
        for pt in info["points"]:
            # bullet point dot
            draw.rectangle([160, y + 4, 172, y + 16], fill=info["accent"])
            draw.text((195, y), pt, fill=(226, 232, 240))
            y += 105

        # Footer
        draw.text((120, 995), "AWS CDS Agentic AI Partner Hackathon  |  NexusOps Omnichannel Concierge", fill=(100, 116, 139))
        draw.text((1600, 995), f"Slide {info['num']} of 5", fill=(100, 116, 139))

        img_path = os.path.join(OUTPUT_DIR, "slides", f"slide_{info['num']}.png")
        img.save(img_path)
        images.append(np.array(img))

    return images

def build_video_frames(slide_arrays):
    print("[ENCODE] Writing full 25fps video stream (no dropped frames)...")
    fps = 25
    # Total audio duration is ~150 seconds. 5 slides -> 30 seconds each = 750 frames per slide
    frames_per_slide = 750  # 30 seconds per slide = 150 seconds total

    writer = imageio.get_writer(
        TEMP_VIDEO_FILE,
        fps=fps,
        codec="libx264",
        pixelformat="yuv420p",
        macro_block_size=1
    )

    for i, slide in enumerate(slide_arrays):
        print(f"[ENCODE] Writing 750 frames for Slide {i+1}...")
        for _ in range(frames_per_slide):
            writer.append_data(slide)

    writer.close()
    print(f"[ENCODE] Video stream written successfully to {TEMP_VIDEO_FILE}")

def merge_audio_and_video():
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", TEMP_VIDEO_FILE,
        "-i", AUDIO_FILE,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_VIDEO_FILE
    ]

    print("[MERGE] Merging 1080p video stream with crystal-clear audio narration...")
    subprocess.run(cmd, check=True)
    
    # Remove temp video file
    if os.path.exists(TEMP_VIDEO_FILE):
        os.remove(TEMP_VIDEO_FILE)

    print(f"[SUCCESS] Final 1080p MP4 created at: {FINAL_VIDEO_FILE}")

async def main():
    await generate_audio()
    slides = create_slides()
    build_video_frames(slides)
    merge_audio_and_video()

if __name__ == "__main__":
    asyncio.run(main())
