from datetime import date, datetime, timedelta
import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.health import WaterLog, WaterGoal, SleepLog
from app.models.learning import LearningSession
from app.models.mood import MoodLog
from app.models.journal import JournalEntry
from app.models.tasks import Task
from app.models.placement import Application
from app.models.user import User


class RiverService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_river_state(self, user_id: uuid.UUID) -> dict:
        today = date.today()
        start_of_today = datetime.combine(today, datetime.min.time())
        seven_days_ago = start_of_today - timedelta(days=7)

        # 1. Hydration -> Water Clarity
        # Fetch today's goal
        goal_q = select(WaterGoal).where(
            WaterGoal.user_id == user_id,
            WaterGoal.is_deleted == False
        ).order_by(WaterGoal.effective_date.desc()).limit(1)
        goal_res = await self.session.execute(goal_q)
        water_goal_obj = goal_res.scalars().first()
        daily_goal = water_goal_obj.daily_goal_ml if water_goal_obj else 2000

        # Fetch today's total logged water
        water_q = select(func.sum(WaterLog.amount_ml)).where(
            WaterLog.user_id == user_id,
            WaterLog.logged_at >= start_of_today,
            WaterLog.is_deleted == False
        )
        water_res = await self.session.execute(water_q)
        water_sum = water_res.scalar() or 0

        water_clarity = min(1.0, water_sum / daily_goal) if daily_goal > 0 else 1.0

        # 2. Studying -> Flow Rate
        # Fetch total study duration today
        study_q = select(func.sum(LearningSession.duration_minutes)).join(LearningSession.subject).where(
            LearningSession.subject.has(user_id=user_id),
            LearningSession.started_at >= start_of_today
        )
        study_res = await self.session.execute(study_q)
        study_sum = study_res.scalar() or 0

        # Flow rate mapping: base is 1.0. If zero study: 0.5. More study -> faster flow.
        if study_sum == 0:
            flow_rate = 0.5
        elif study_sum < 30:
            flow_rate = 0.8
        elif study_sum < 90:
            flow_rate = 1.2
        elif study_sum < 180:
            flow_rate = 1.6
        else:
            flow_rate = 2.0

        # 3. Sleep -> Ambient Time of Day & Wildlife
        sleep_q = select(SleepLog).where(
            SleepLog.user_id == user_id,
            SleepLog.sleep_time >= start_of_today - timedelta(days=1),
            SleepLog.is_deleted == False
        ).order_by(SleepLog.sleep_time.desc()).limit(1)
        sleep_res = await self.session.execute(sleep_q)
        sleep_log = sleep_res.scalars().first()

        sleep_quality = sleep_log.quality if sleep_log and sleep_log.quality else 3
        # High sleep quality brings out more wildlife (forest flourishes)
        wildlife_count = min(10, sleep_quality * 2)

        # 4. Mood & Journaling -> Flora/Flowers Density
        mood_q = select(MoodLog).where(
            MoodLog.user_id == user_id,
            MoodLog.logged_at >= start_of_today
        ).order_by(MoodLog.logged_at.desc()).limit(1)
        mood_res = await self.session.execute(mood_q)
        mood_log = mood_res.scalars().first()

        # Check last 7 days journaling frequency to calculate flora density
        journal_q = select(func.count(JournalEntry.id)).where(
            JournalEntry.user_id == user_id,
            JournalEntry.created_at >= seven_days_ago
        )
        journal_res = await self.session.execute(journal_q)
        journal_count = journal_res.scalar() or 0

        # Flora density based on mood intensity + journal counts
        mood_intensity = mood_log.intensity if mood_log else 5
        base_density = (mood_intensity / 10.0) * 0.5
        journal_bonus = min(0.5, (journal_count / 7.0) * 0.5)
        flora_density = min(1.0, base_density + journal_bonus)

        # 5. Career & Placement -> Coding landmarks & Bridges
        # Fetch active coding progress/placement applications
        app_q = select(func.count(Application.id)).where(
            Application.user_id == user_id
        )
        app_res = await self.session.execute(app_q)
        app_count = app_res.scalar() or 0

        # Unlocked bridges depend on active placement progress or goals completed
        task_q = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.status == 'done'
        )
        task_res = await self.session.execute(task_q)
        completed_tasks = task_res.scalar() or 0

        active_bridges = min(5, (app_count + (completed_tasks // 5)))

        # Determine Weather & Time of Day dynamically
        current_hour = datetime.now().hour
        if 5 <= current_hour < 8:
            time_of_day = "dawn"
        elif 8 <= current_hour < 17:
            time_of_day = "day"
        elif 17 <= current_hour < 20:
            time_of_day = "dusk"
        else:
            time_of_day = "night"

        # Weather based on mood
        mood_val = mood_log.mood if mood_log else "neutral"
        if mood_val in ["happy", "calm"]:
            current_weather = "sunny"
        elif mood_val == "neutral":
            current_weather = "misty"
        elif mood_val in ["stressed", "sad"]:
            current_weather = "rainy"
        else:  # burned_out
            current_weather = "cloudy"

        return {
            "flow_rate": flow_rate,
            "water_clarity": water_clarity,
            "flora_density": flora_density,
            "wildlife_count": wildlife_count,
            "active_bridges": active_bridges,
            "current_weather": current_weather,
            "time_of_day": time_of_day,
            "recent_metrics": {
                "water_ml": water_sum,
                "study_minutes": study_sum,
                "sleep_quality": sleep_quality,
                "mood": str(mood_val),
                "journal_count_7d": journal_count,
                "completed_tasks": completed_tasks
            }
        }
