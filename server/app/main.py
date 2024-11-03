from fastapi import FastAPI
import app.api.endpoints as endpoints
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Подключаем роуты
app.include_router(endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:8000", 
        "http://localhost:4200",
        "http://localhost:5173", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:8000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Change to specific methods as needed
    allow_headers=["*"],  # Change to specific headers as needed
    allow_params=["*"],
)
