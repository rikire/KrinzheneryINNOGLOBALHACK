from fastapi import FastAPI
import app.api.endpoints as endpoints
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Подключаем роуты
app.include_router(endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Change to specific methods as needed
    allow_headers=["*"],  # Change to specific headers as needed
    allow_params=["*"],
)