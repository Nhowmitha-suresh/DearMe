import logging
import aiohttp
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.journal_repository import JournalRepository
from app.models.journal import JournalEntry, JournalAIAnalysis
from app.schemas.journal import JournalEntryCreate
from app.core.config import settings

logger = logging.getLogger(__name__)


class JournalService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = JournalRepository(session)

    async def create_entry(self, user, payload: JournalEntryCreate):
        if not payload.content or payload.content.strip() == '':
            raise ValueError('content is required')
        
        # Determine initial mood
        initial_mood = payload.mood

        # Create Journal Entry first
        je = JournalEntry(
            user_id=user.id,
            title=payload.title,
            content=payload.content,
            mood=initial_mood
        )
        await self.repo.create(je)
        await self.session.commit()

        # Run AI analysis
        ai_summary = "A quiet reflection of the day."
        ai_reflection = "Every step forward, no matter how small, is a current carving its way through the mountain."
        ai_suggestions = ["Stay hydrated", "Take a short walk in nature"]
        detected_mood = initial_mood or "neutral"

        if settings.GEMINI_API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            prompt = (
                "You are Nadhi, a wise, calming river spirit. Analyze this student journal entry:\n"
                f"Title: {payload.title or 'Untitled'}\nContent: {payload.content}\n\n"
                "Provide a JSON response with exactly these keys:\n"
                "- mood: string (one of 'happy', 'calm', 'neutral', 'stressed', 'sad', 'burned_out')\n"
                "- summary: string (a short 1-sentence summary)\n"
                "- reflection: string (a supportive, nature-themed reflection)\n"
                "- suggestions: list of strings (2 wellness suggestions)\n"
                "Return ONLY valid JSON, no markdown formatting blocks."
            )
            payload_data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            }
            try:
                async with aiohttp.ClientSession() as aio_session:
                    async with aio_session.post(url, json=payload_data, headers=headers, timeout=12) as response:
                        if response.status == 200:
                            data = await response.json()
                            text_resp = data['candidates'][0]['content']['parts'][0]['text'].strip()
                            # Clean up any potential markdown wrapper
                            if text_resp.startswith("```"):
                                lines = text_resp.split("\n")
                                if lines[0].startswith("```json") or lines[0].startswith("```"):
                                    text_resp = "\n".join(lines[1:-1])
                            
                            parsed = json.loads(text_resp)
                            ai_summary = parsed.get("summary", ai_summary)
                            ai_reflection = parsed.get("reflection", ai_reflection)
                            ai_suggestions = parsed.get("suggestions", ai_suggestions)
                            detected_mood = parsed.get("mood", detected_mood)
            except Exception as e:
                logger.error(f"Error calling Gemini in JournalService: {e}")

        # Update entry mood if it was not user-specified
        if not je.mood:
            je.mood = detected_mood
            await self.session.commit()

        # Save AI analysis
        analysis = JournalAIAnalysis(
            journal_entry_id=je.id,
            ai_summary=ai_summary,
            ai_reflection=ai_reflection,
            ai_suggestions={"items": ai_suggestions}
        )
        self.session.add(analysis)
        await self.session.commit()
        await self.session.refresh(je)
        return je

    async def list_entries(self, user, limit=50, offset=0):
        return await self.repo.list_by_user(user.id, limit=limit, offset=offset)

