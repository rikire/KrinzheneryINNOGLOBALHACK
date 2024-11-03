from fastapi import FastAPI
import app.api.endpoints as endpoints
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Подключаем роуты
app.include_router(endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

