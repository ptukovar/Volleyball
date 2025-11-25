from fastapi import FastAPI
from app.api.routes import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Volejbal API", version="0.1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)