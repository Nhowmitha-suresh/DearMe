Backend — FastAPI Folder Structure (Clean Architecture)

Suggested structure:

app/
- api/
  - v1/
    - routers/
      - auth.py
      - users.py
      - health.py
      - goals.py
      - tasks.py
      - ai.py
      - placements.py
    - deps.py
- core/
  - config.py
  - security.py
  - celery_utils.py
- services/
  - auth_service.py
  - user_service.py
  - health_service.py
  - ai_service.py
  - placement_service.py
- repositories/
  - user_repo.py
  - health_repo.py
  - goal_repo.py
- models/          # SQLAlchemy models
- schemas/         # Pydantic schemas
- db/
  - base.py
  - session.py
  - migrations/    # Alembic
- ai/              # RAG, ChromaDB helpers
- notifications/   # FCM integration
- tests/
- main.py

Key features
- JWT Authentication
- Dependency injection via FastAPI `Depends`
- Async SQLAlchemy (1.4+) with Alembic
- Background tasks for reminders, AI processing
