from __future__ import annotations
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from dotenv import load_dotenv
from api import AssistantFnc
import os

load_dotenv()

INSTRUCTIONS = """
You are the manager of a call center, you are speaking to customer.
Your goal is to help answer their questions or direct them to the correct department.
Start by collecting or looking up their car information.

"""

WELCOME_MESSAGE="""
Begin by welcoming the user to our auto service center and ask them to provide the VIN of their vehicle.
"""

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()
	
    model = openai.realtime.RealtimeModel(
       instructions=INSTRUCTIONS,
       voice="shimmer",
       temperature=0.8,
       modalities=["audio","text"]
    )
    assistant_fnc = AssistantFnc()
    assistant = MultimodalAgent(model=model, fnc_ctx=assistant_fnc)
    assistant.start(ctx.room)

    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content=WELCOME_MESSAGE
        )
    )
    session.response.create()
	
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
