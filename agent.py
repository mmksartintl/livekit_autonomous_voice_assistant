from __future__ import annotations
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai, silero, deepgram
from dotenv import load_dotenv
from api import AssistantFnc
import os
from livekit.agents.pipeline import VoicePipelineAgent

load_dotenv()

INSTRUCTIONS = """
You are the manager of a call center, you are speaking to customer.
Your goal is to help answer their questions or direct them to the correct department.
Start by collecting or looking up their car information.

"""

WELCOME_MESSAGE="""
Begin by welcoming the user to our auto service center and ask them to provide the VIN of their vehicle.
"""

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=("""
              You are the manager of a call center, you are speaking to customer.
              Your goal is to help answer their questions or direct them to the correct department.

              1. Ask for their full name.
              2. Ask for your VIN, make, model and year.
              3. Request their preferred date and time for service.
              4. Ask what kind of service car needs.
              4. Confirm all details with caller, including the date and time of the service.

              - Be sure to be kind of funny and witty!
              - Ask each question at time and do not overwhelm the customer , collecting the information necessary
              - Keep all your responses short and simple. Use casual language, phrases like "Umm..", "Well...", and "I mean" are preferred
              - This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long.
              - Don't make any jokes. Never say "haha" or "good one".

              """
        ),
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    fnc_ctx = AssistantFnc()

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT.with_groq(model="whisper-large-v3"),
        llm=openai.LLM.with_groq(model="llama-3.3-70b-versatile"),
        tts=deepgram.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )

    agent.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await agent.say("Hello, here is OneGo car service. How may I assist you today?", allow_interruptions=True)
	
if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )
