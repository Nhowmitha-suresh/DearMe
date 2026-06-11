from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title='DearMe API', version='0.1.0')

app.include_router(api_router)

@app.get('/')
async def root():
    return {'status': 'DearMe API', 'version': '0.1.0'}
