from fastapi import FastAPI
from app.api import auth, users, health, goals, tasks, journal, notifications, ai

app = FastAPI(title='DearMe API', version='0.1.0')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(goals.router)
app.include_router(tasks.router)
app.include_router(journal.router)
app.include_router(notifications.router)
app.include_router(ai.router)

@app.get('/')
async def root():
    return {'status': 'DearMe API', 'version': '0.1.0'}
