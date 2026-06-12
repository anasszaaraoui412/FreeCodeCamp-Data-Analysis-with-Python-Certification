import logging
import asyncio
from typing import Annotated

from livekit import agents, rtc
from livekit.agents import JobContext, JobRequest, WorkerOptions, cli, llm
from livekit.plugins import openai
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

logger = logging.getLogger("unoya-agent")
logger.setLevel(logging.INFO)

class AssistantTools(llm.FunctionContext):
    """
    Tools for the AI Concierge to interact with the Workplace Backend.
    """

    @llm.ai_callable(description="Check if a host (employee) is available at a specific time.")
    async def check_availability(
        self,
        host_name: Annotated[str, llm.TypeInfo(description="Name of the employee to visit")],
        time: Annotated[str, llm.TypeInfo(description="Requested time for the visit")]
    ):
        logger.info(f"Checking availability for {host_name} at {time}")
        async with httpx.AsyncClient() as client:
            try:
                # First find the user by name
                users_resp = await client.get(f"{BACKEND_URL}/users/", headers={"X-Mock-Role": "tenant_admin", "X-Mock-User-Email": "admin@example.com"})
                users = users_resp.json()
                host = next((u for u in users if host_name.lower() in f"{u['first_name']} {u['last_name']}".lower()), None)

                if not host:
                    return f"I couldn't find an employee named {host_name}."

                # In a real app we'd check their bookings here
                return f"{host['first_name']} {host['last_name']} appears to be available at {time}."
            except Exception as e:
                logger.error(f"Error checking availability: {e}")
                return "I'm having trouble accessing the calendar right now."

    @llm.ai_callable(description="Schedule an appointment for a visitor with a host.")
    async def schedule_appointment(
        self,
        visitor_name: Annotated[str, llm.TypeInfo(description="Name of the visitor")],
        host_name: Annotated[str, llm.TypeInfo(description="Name of the host")],
        time: Annotated[str, llm.TypeInfo(description="Time of the appointment, e.g. 2023-10-27T10:00:00")]
    ):
        logger.info(f"Scheduling appointment for {visitor_name} with {host_name} at {time}")
        async with httpx.AsyncClient() as client:
            try:
                users_resp = await client.get(f"{BACKEND_URL}/users/", headers={"X-Mock-Role": "tenant_admin", "X-Mock-User-Email": "admin@example.com"})
                users = users_resp.json()
                host = next((u for u in users if host_name.lower() in f"{u['first_name']} {u['last_name']}".lower()), None)

                if not host:
                    return f"I couldn't find an employee named {host_name}."

                payload = {
                    "host_id": host['id'],
                    "start_time": time,
                    "end_time": time # simplified for MVP
                }
                resp = await client.post(
                    f"{BACKEND_URL}/bookings/",
                    json=payload,
                    headers={"X-Mock-Role": "employee", "X-Mock-User-Email": host['email']}
                )

                if resp.status_code == 409:
                    return f"I'm sorry, {host_name}'s schedule is full at {time}. Would you like to try another time?"

                return f"Great, I've scheduled your appointment with {host['first_name']} for {time}."
            except Exception as e:
                logger.error(f"Error scheduling: {e}")
                return "I encountered an error while trying to book that appointment."

    @llm.ai_callable(description="Leave a message for a host if they are unavailable.")
    async def leave_message(
        self,
        host_name: Annotated[str, llm.TypeInfo(description="Name of the host")],
        message_content: Annotated[str, llm.TypeInfo(description="Content of the message")]
    ):
        logger.info(f"Leaving message for {host_name}: {message_content}")
        async with httpx.AsyncClient() as client:
            try:
                users_resp = await client.get(f"{BACKEND_URL}/users/", headers={"X-Mock-Role": "tenant_admin", "X-Mock-User-Email": "admin@example.com"})
                users = users_resp.json()
                host = next((u for u in users if host_name.lower() in f"{u['first_name']} {u['last_name']}".lower()), None)

                if not host:
                    return f"I couldn't find an employee named {host_name} to leave a message for."

                payload = {
                    "host_id": host['id'],
                    "content": message_content
                }
                await client.post(
                    f"{BACKEND_URL}/messages/",
                    json=payload,
                    headers={"X-Mock-Role": "tenant_admin", "X-Mock-User-Email": "admin@example.com"}
                )
                return f"I've sent that message to {host['first_name']} for you."
            except Exception as e:
                logger.error(f"Error leaving message: {e}")
                return "I'm sorry, I couldn't deliver your message at this time."

async def entrypoint(ctx: JobContext):
    logger.info("Starting AI Agent for Unoya")

    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are the UNOYA AI Workplace Concierge. Your job is to welcome visitors, "
            "help them find employees, schedule appointments, and take messages. "
            "Be professional, warm, and efficient. If a host's schedule is full, suggest a later time."
        ),
    )

    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)

    agent = agents.multimodal.MultimodalAgent(
        model=openai.realtime.RealtimeModel(
            instructions="You are a helpful office concierge.",
            modalities=["audio", "text"],
        ),
        fnc_ctx=AssistantTools(),
        chat_ctx=initial_ctx,
    )

    agent.start(ctx.room)

    @agent.on("user_speech_committed")
    def on_speech_committed(msg: llm.ChatMessage):
        logger.info(f"User said: {msg.content}")

    await agent.say("Welcome to the office. How can I help you today?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
