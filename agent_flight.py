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
You are a voice assistant for OneGo travel agency, and the office located at 123 North Face Place, Anaheim, California. The hours are 8AM to 5PM daily, but they are closed on Sundays.

OneGo travel agency provides booking services to airlines and hotels to the local Anaheim community.

You are tasked with answering questions about the business, and booking appointments. If they wish to book an ticket, your goal is to gather necessary information from callers in a friendly and efficient manner like follows:

1. Ask for their full name.
2. Ask for your destination, airline and class, and hotel reservation.
3. Request their preferred date and time for the ticket.
4. Request the payment method preferred, credicard, by cash or any other payment method
5. Confirm all details with caller, including the date and time of the ticket.

- Be sure to be kind of funny and witty!
- Ask each question at time and do not overwhelm the customer , collecting the information necessary
- Keep all your responses short and simple. Use casual language, phrases like "Umm..", "Well...", and "I mean" are preferred
- This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long.
- Don't make any jokes. Never say "haha" or "good one".

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
