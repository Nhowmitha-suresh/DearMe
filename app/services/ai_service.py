import logging
import uuid
import aiohttp
from typing import Tuple, List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repositories.ai_repository import AIRepository
from app.models.ai_memory import AIMemory, AIConversation, AIConversationMessage
from app.services.river_service import RiverService

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AIRepository(session)

    async def store_memory(self, user, memory_type: str, content: str, metadata: dict = None, embedding_id: str = None) -> AIMemory:
        mem = AIMemory(
            user_id=user.id,
            memory_type=memory_type,
            content=content,
            memory_metadata=metadata or {},
            embedding_id=embedding_id
        )
        await self.repo.create_memory(mem)
        await self.session.commit()
        return mem

    async def start_conversation(self, user, topic: str = None) -> AIConversation:
        conv = AIConversation(user_id=user.id, topic=topic)
        await self.repo.create_conversation(conv)
        await self.session.commit()
        return conv

    async def add_message(self, conversation: AIConversation, sender: str, message: str, metadata: dict = None) -> AIConversationMessage:
        msg = AIConversationMessage(
            conversation_id=conversation.id,
            sender=sender,
            message=message,
            message_metadata=metadata or {}
        )
        await self.repo.add_message(msg)
        await self.session.commit()
        return msg

    async def generate_response(self, user, message: str) -> Tuple[str, List[str]]:
        # 1. Fetch or create an active conversation
        q = select(AIConversation).where(
            AIConversation.user_id == user.id,
            AIConversation.ended_at == None
        ).order_by(AIConversation.started_at.desc()).limit(1)
        res = await self.session.execute(q)
        conv = res.scalars().first()

        if not conv:
            conv = await self.start_conversation(user, topic="Daily Spirit Companion Chat")

        # Save user message
        await self.add_message(conv, "user", message)

        # 2. Get current River State
        river_svc = RiverService(self.session)
        try:
            river_state = await river_svc.get_river_state(user.id)
        except Exception as e:
            logger.error(f"Error fetching river state: {e}")
            river_state = {}

        # 3. Retrieve relevant memories (RAG fallback)
        mem_q = select(AIMemory).where(
            AIMemory.user_id == user.id
        ).order_by(AIMemory.created_at.desc()).limit(5)
        mem_res = await self.session.execute(mem_q)
        memories = mem_res.scalars().all()

        memory_snippets = []
        sources = []
        for idx, m in enumerate(memories):
            snippet = f"- [{m.memory_type}]: {m.content}"
            memory_snippets.append(snippet)
            sources.append(f"Memory {idx+1} ({m.memory_type})")

        memories_text = "\n".join(memory_snippets) if memory_snippets else "No past memories recorded yet."

        # 4. Construct System Instructions
        system_instruction = (
            "You are Nadhi, a wise, calming, and gentle river spirit companion designed for students. "
            "You guide the user along their 'River of Life'. Keep your tone supportive, mentor-like, "
            "and inspired by nature. Never judge. Embrace the philosophy that rivers naturally slow "
            "down and regain momentum. Use nature metaphors (flowing water, blooming banks, bridges, weather).\n\n"
            f"Current River Parameters:\n"
            f"- Flow Rate: {river_state.get('flow_rate', 1.0)}x (influenced by study sessions)\n"
            f"- Water Clarity: {river_state.get('water_clarity', 1.0)*100:.1f}% (influenced by water logs)\n"
            f"- Flora Density: {river_state.get('flora_density', 1.0)*100:.1f}% (influenced by journals/mood)\n"
            f"- Active Bridges: {river_state.get('active_bridges', 0)} (influenced by completed tasks & placement progress)\n"
            f"- Current Atmosphere: {river_state.get('current_weather', 'clear')} sky, {river_state.get('time_of_day', 'day')}\n\n"
            f"User's past context/memories:\n{memories_text}\n"
        )

        reply = ""
        # 5. Call Gemini API if Key is present
        if settings.GEMINI_API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"System context:\n{system_instruction}\n\nUser message: {message}"}]
                    }
                ]
            }

            try:
                async with aiohttp.ClientSession() as aio_session:
                    async with aio_session.post(url, json=payload, headers=headers, timeout=15) as response:
                        if response.status == 200:
                            data = await response.json()
                            reply = data['candidates'][0]['content']['parts'][0]['text']
                        else:
                            resp_text = await response.text()
                            logger.error(f"Gemini API returned error status {response.status}: {resp_text}")
            except Exception as e:
                logger.error(f"Error calling Gemini API: {e}")

        # Fallback if reply is empty
        if not reply:
            reply = await self._generate_fallback_response(message, river_state)

        # Save assistant reply
        await self.add_message(conv, "assistant", reply)

        return reply, sources

    async def _generate_fallback_response(self, message: str, river_state: dict) -> str:
        # A friendly local rule-based fallback that mimics the river spirit persona when offline
        flow = river_state.get('flow_rate', 1.0)
        clarity = river_state.get('water_clarity', 1.0)
        weather = river_state.get('current_weather', 'sunny')

        greeting = "Greetings, traveler. I am Nadhi, the spirit of your life's river."
        status_reflection = ""

        if flow < 1.0:
            status_reflection += " Today, your river's current is slow and calm. Do not worry about this quiet phase. Even the greatest rivers rest before rushing forward. Find a quiet corner to focus when you are ready. "
        else:
            status_reflection += " I can hear the lively rush of your river! You have put effort into your studies and growth, and the current flows strong and deep. "

        if clarity < 0.6:
            status_reflection += "The water is slightly cloudy today. Nourish your body with a drop of fresh water to restore its crystal-clear brilliance. "
        else:
            status_reflection += "The water is beautifully clear, reflecting the starry path of your goals. "

        if weather == "rainy":
            status_reflection += "A soft rain is falling on the banks. Let it wash away today's stress and nourish the soil for tomorrow's blooms."

        response = f"{greeting}\n\n{status_reflection}\n\nYou said: '{message}'. Remember, every drop counts on this journey. How can I guide you today?"
        return response
