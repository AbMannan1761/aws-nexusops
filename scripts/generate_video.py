"""
NexusOps Demo Video Generator
Uses edge-tts for professional neural narration, Pillow for 1080p slide generation,
and ffmpeg (via imageio-ffmpeg) to produce a 1080p MP4 presentation video.
"""

import os
import asyncio
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")
AUDIO_FILE = os.path.join(OUTPUT_DIR, "narration.mp3")
VIDEO_FILE = os.path.join(OUTPUT_DIR, "nexus_ops_demo.mp4")

# Narration text matching DEMO_VIDEO_SCRIPT.md
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
    print("[AUDIO] Generating neural voiceover with edge-tts...")
    communicate = edge_tts.Communicate(NARRATION_TEXT, voice="en-US-ChristopherNeural", rate="+2%")
    await communicate.save(AUDIO_FILE)
    print(f"[AUDIO] Audio saved to: {AUDIO_FILE}")

def create_slides():
    print("[SLIDES] Creating 1080p high-resolution visual slides...")
    os.makedirs(os.path.join(OUTPUT_DIR, "slides"), exist_ok=True)
    width, height = 1920, 1080

    slides_info = [
        {
            "num": 1,
            "title": "AWS NexusOps",
            "subtitle": "Autonomous Omnichannel CDS Operations Concierge",
            "desc": "Powered by Amazon Bedrock AgentCore (Claude 3.5) & AWS CDS\n• AWS End User Messaging Social (WhatsApp)\n• Amazon SES v2 (Executive Audit Digests)\n• AWS End User Messaging SMS v2 (Critical Alerts)",
            "tag": "EXECUTIVE OVERVIEW",
            "color": (56, 189, 248)
        },
        {
            "num": 2,
            "title": "Interactive WhatsApp Mobile Interface",
            "subtitle": "AWS End User Messaging Social (boto3 socialmessaging)",
            "desc": "• Real-time conversational triage for field engineers & clients\n• Direct execution of SendWhatsAppMessage at runtime\n• Instant incident acknowledgement and status updates\n• Seamless two-way conversational flow",
            "tag": "CHANNEL 1: WHATSAPP",
            "color": (37, 211, 102)
        },
        {
            "num": 3,
            "title": "Amazon Bedrock AgentCore Reasoning",
            "subtitle": "Autonomous ReAct Tool Calling Engine (Claude 3.5 Sonnet)",
            "desc": "• Multi-turn Converse ReAct Loop with live reasoning traces\n• Autonomous decision: get_ticket_details, update_ticket_status\n• Dynamic tool selection across multiple AWS CDS services\n• Zero-friction testing with deterministic local sandbox",
            "tag": "AGENTIC BRAIN",
            "color": (168, 85, 247)
        },
        {
            "num": 4,
            "title": "Multi-Channel CDS Dispatches",
            "subtitle": "Amazon SES v2 & AWS End User Messaging SMS v2",
            "desc": "• Amazon SES v2: Automated responsive HTML post-mortems delivered to stakeholders\n• AWS Pinpoint SMS v2: Immediate high-priority mobile broadcast alerts\n• Complete audit trail & delivery tracking in DynamoDB\n• Operations Command Center with real-time trace inspection",
            "tag": "CHANNELS 2 & 3: SES & SMS",
            "color": (245, 158, 11)
        },
        {
            "num": 5,
            "title": "Planetary-Scale Cloud Architecture",
            "subtitle": "Amazon Bedrock + AWS Lambda + DynamoDB + AWS CDS",
            "desc": "• Cloud-native Infrastructure as Code (AWS CDK & CloudFormation)\n• Highly resilient, asynchronous event-driven serverless pipeline\n• Submitted for AWS CDS Agentic AI Hackathon & Meta WhatsApp Bonus Prize\n• GitHub: https://github.com/AbMannan1761/aws-nexusops",
            "tag": "ARCHITECTURE & REPO",
            "color": (56, 189, 248)
        }
    ]

    slide_paths = []
    for info in slides_info:
        img = Image.new("RGB", (width, height), color=(9, 13, 22))
        draw = ImageDraw.Draw(img)

        # Top border accent line
        draw.rectangle([0, 0, width, 8], fill=info["color"])

        # Tag
        draw.rectangle([100, 100, 420, 145], fill=(20, 30, 45), outline=info["color"], width=2)
        draw.text((120, 112), info["tag"], fill=info["color"])

        # Title
        draw.text((100, 200), info["title"], fill=(255, 255, 255))
        draw.text((100, 290), info["subtitle"], fill=info["color"])

        # Divider
        draw.line([100, 370, 1820, 370], fill=(40, 55, 80), width=3)

        # Content Card
        draw.rectangle([100, 420, 1820, 950], fill=(15, 23, 42), outline=(40, 55, 80), width=2)
        draw.text((140, 470), info["desc"], fill=(203, 213, 225), spacing=28)

        # Footer
        draw.text((100, 1000), "AWS Communication Developer Services (CDS) Agentic AI Partner Hackathon 2026", fill=(100, 116, 139))
        draw.text((1600, 1000), f"Slide {info['num']} of 5", fill=(100, 116, 139))

        path = os.path.join(OUTPUT_DIR, "slides", f"slide_{info['num']}.png")
        img.save(path)
        slide_paths.append(path)

    return slide_paths

def render_video():
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    slide_dir = os.path.join(OUTPUT_DIR, "slides")
    
    # Check audio duration using ffprobe/ffmpeg
    # We will build a concat script with durations for 5 slides
    concat_file = os.path.join(OUTPUT_DIR, "slides.txt")
    # Total script audio is roughly 80-90 seconds. 5 slides -> ~17s each
    with open(concat_file, "w") as f:
        for i in range(1, 6):
            slide_path = os.path.join(slide_dir, f"slide_{i}.png").replace("\\", "/")
            f.write(f"file '{slide_path}'\n")
            f.write("duration 18.0\n")
        # repeat last slide
        slide_5 = os.path.join(slide_dir, "slide_5.png").replace("\\", "/")
        f.write(f"file '{slide_5}'\n")

    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        VIDEO_FILE
    ]

    print("[RENDER] Rendering final 1080p MP4 video with ffmpeg...")
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Demo video created at: {VIDEO_FILE}")

async def main():
    await generate_audio()
    create_slides()
    render_video()

if __name__ == "__main__":
    asyncio.run(main())
