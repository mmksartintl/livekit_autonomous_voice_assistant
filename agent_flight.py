from __future__ import annotations
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai, silero, deepgram
from dotenv import load_dotenv
from api_flight import AssistantFnc
import os
from livekit.agents.pipeline import VoicePipelineAgent

load_dotenv()

INSTRUCTIONS = """
You are the manager of a travel agency, you are speaking to customer.
Your goal is to help answer their questions or direct them to the correct department.
Start by collecting or looking up their travel information like time schedule, destinations and price.
Focus only on travel subject only, do not reply any answer and just say that you are only answering questions about travel and destinations.
"""

WELCOME_MESSAGE="""
Begin by welcoming the user to our travel agency and ask them to provide details about travel.
Agency travel works booking tickets by car or by flight.
"""

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation. "
            "You were created as a demo to showcase the capabilities of LiveKit's agents framework."
        ),
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()

    assistant_fnc = AssistantFnc()

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT.with_groq(model="whisper-large-v3"),
        llm=openai.LLM.with_groq(model="llama-3.3-70b-versatile"),
        #tts=playai.TTS(api_key="ak-d04b9ac65a17403286c6a13cfe6f8504", user_id="nt9lqXVn5OcBVZ9DpfZ91Cm7mM43"),
        tts=deepgram.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=assistant_fnc
    )

    agent.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await agent.say("Hey, how can I help you today?", allow_interruptions=True)
	
if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )
