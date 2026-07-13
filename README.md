# NADHI – The AI River of Life (Ecosystem Companion)

Nadhi is a premium, nature-inspired AI life companion designed for students. By blending focus tracking, academic planners, career trackers, wellness logs, and financial budgets into a singular living world, Nadhi shifts productivity from checklists to a beautiful interactive river ecosystem.

---

## 1. Project Architecture

The backend is built using FastAPI following a decoupled **Clean Architecture** (Repository + Service Layer) design, separating concerns between controllers, logic services, and persistence layers.

<img width="1915" height="910" alt="image" src="https://github.com/user-attachments/assets/ffe0198c-a94f-49a2-a542-59bc2370c086" />


---

## 2. Database Schema Diagram

Below is the database entity-relationship diagram containing all normalized tables (including the new Finance and Coding trackers):

```mermaid
erDiagram
    users {
        uuid id PK
        text email UK
        text password_hash
        text firebase_uid UK
        boolean is_active
        timestamp created_at
    }

    expenses {
        uuid id PK
        uuid user_id FK
        numeric amount
        text category
        text description
        timestamp logged_at
    }

    savings_goals {
        uuid id PK
        uuid user_id FK
        text title
        numeric target_amount
        numeric current_amount
        date target_date
    }

    coding_profiles {
        uuid id PK
        uuid user_id FK
        text leetcode_username
        text github_username
        boolean is_active
    }

    coding_activities {
        uuid id PK
        uuid user_id FK
        integer commits_count
        integer problems_solved
        date logged_date
    }

    learning_sessions {
        uuid id PK
        uuid user_id FK
        uuid subject_id FK
        timestamp start_time
        timestamp end_time
        integer focus_duration_minutes
        text notes
    }

    users ||--o{ expenses : owns
    users ||--o{ savings_goals : tracks
    users ||--o{ coding_profiles : registers
    users ||--o{ coding_activities : logs
    users ||--o{ learning_sessions : focus
```

---

## 3. Core API Documentation

### Authentication `/api/v1/auth`
*   `POST /signup`: Register a new email/password account.
*   `POST /login`: Log in with email/password and obtain a native JWT token.
*   `POST /firebase`: Exchange a Firebase ID Token for a session token.
*   `GET /me`: Fetch the current authenticated user's profile.

### River Engine `/api/v1/river`
*   `GET /state`: Retrieves the calculated physical parameters of the user's river ecosystem (`flow_rate`, `water_clarity`, `flora_density`, `active_bridges`, `current_weather`, `time_of_day`).

### Student Academic Hub `/api/v1/student`
*   `POST /subjects` / `GET /subjects`: Create and list academic subjects.
*   `POST /sessions` / `GET /sessions`: Log Pomodoro study focus time blocks.
*   `POST /events` / `GET /events`: Manage timetable schedules and exams.
*   `GET /attendance`: Retrieve overall subject attendance percentages.

### Coding Hub `/api/v1/coding`
*   `POST /profile` / `GET /profile`: Register GitHub and LeetCode usernames.
*   `POST /activity` / `GET /activity`: Log daily commits or solved problems.
*   `GET /stats`: Retrieve streaks and aggregate counts.

### Career Hub `/api/v1/career`
*   `POST /companies` / `GET /companies`: Register hiring companies.
*   `POST /applications` / `GET /applications`: Track placement pipelines (applied, screening, interview, offered).
*   `GET /stats`: Fetch application-to-interview conversion ratios.

### Health & Finance Hubs
*   `POST /health/cycle` / `GET /cycle/prediction`: Predict next period timelines.
*   `POST /finance/expenses` / `GET /finance/summary`: Log expenditures and track savings targets.

---

## 4. Installation & Local Startup

### Backend Prerequisites
1. Python 3.10+
2. PostgreSQL (with `pgcrypto` extension)

### Startup Commands

1. **Navigate to the backend directory and activate the virtual environment**:
   ```powershell
   # Windows
   .venv\Scripts\activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment variables** in a `.env` file at the root:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/dearme
   SECRET_KEY=yoursecretjwtkeyhere
   GEMINI_API_KEY=AIzaSy...
   ```
4. **Start the FastAPI App**:
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Open Swagger API Docs**: Navigate to `http://localhost:8000/docs` in your browser.

---

## 5. Staging & Production Deployment (Docker)

To deploy the application inside Docker containers:

1. **Build and Run via Docker Compose**:
   ```bash
   docker-compose up --build -d
   ```
2. **Apply Alembic migrations inside the container**:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

---

## 6. Developer & Extension Guide

*   **Adding New River Renders**: Update the wave custom painter in [river_painter.dart](file:///c:/Users/Lenovo/Desktop/DearMe/frontend/lib/core/ui/widgets/river_painter.dart) to draw custom elements (like bridges or fish) based on values passed from the dashboard view state.
*   **Running Tests**: Run `.venv\Scripts\python -m pytest` to execute all automated test scenarios.
