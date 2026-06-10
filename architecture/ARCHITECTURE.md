DearMe - High-level Architecture

Overview
- Frontend: Flutter (Clean Architecture, MVVM, Feature-based)
- Backend: FastAPI (Controllers -> Services -> Repos -> DB)
- DB: PostgreSQL
- Cache: Redis
- AI: Gemini API
- Memory: ChromaDB (RAG)
- Auth & Notifications: Firebase Auth + FCM

Key Components
- Mobile App (Flutter): UI, ViewModels, Repositories
- API Server (FastAPI): Auth, User, Health, Goals, Tasks, AI, Analytics
- Long-term Memory (ChromaDB): Semantic vectors and user memories
- Redis: sessions, ai context cache, reminder queue
- PostgreSQL: source of truth for structured data

Integration Flow
1. User interacts via Flutter app.
2. App authenticates with Firebase; uses JWT to call FastAPI.
3. FastAPI validates, uses services and repositories to read/write Postgres.
4. For AI responses, FastAPI composes context from Postgres + Redis + ChromaDB, then calls Gemini.
5. AI outputs are persisted and optionally written to ChromaDB as memory records.
6. Redis handles reminders, active sessions, and quick dashboard caching.

Security & Privacy
- GDPR-aware: data minimization, opt-in for memory storage
- Strong encryption at rest (DB) and in transit (TLS)
- Role-based access controls for API
